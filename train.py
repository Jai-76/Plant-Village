"""Train the plant disease classifier.

Incorporates the high-accuracy (99.6 %) approach from the reference notebook:
  - EfficientNetB3 backbone  (recommended, ~99 % accuracy)
  - MobileNetV2 backbone     (lighter alternative)
  - Custom CNN               (from-scratch baseline)

Usage:
    python train.py                                        # EfficientNetB3 (default)
    python train.py --model efficientnet --epochs 40
    python train.py --model mobilenet   --epochs 10 --fine_tune_epochs 5
    python train.py --model cnn         --epochs 25

Outputs saved to outputs/:
    training_curves.png        – accuracy & loss with best-epoch markers
    classification_report.txt  – per-class precision / recall / F1
    confusion_matrix.png       – heatmap

Model saved to:
    models/plant_disease_model.keras   (Keras native format)
    models/plant_disease_model.h5      (HDF5, for compatibility)
    models/class_dict.csv              (class index → name mapping)
"""
from __future__ import annotations

import argparse
import json
import os
import time
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.layers import (BatchNormalization, Dense, Dropout)
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

import config as C

tf.keras.utils.set_random_seed(C.SEED)


# ═══════════════════════════════════════════════════════════════════════════════
#  DATA HELPERS  (from notebook)
# ═══════════════════════════════════════════════════════════════════════════════

def define_paths(data_dir: str):
    """Walk each class sub-folder and collect (filepath, label) lists."""
    filepaths, labels = [], []
    for fold in os.listdir(data_dir):
        foldpath = os.path.join(data_dir, fold)
        if not os.path.isdir(foldpath):
            continue
        for file in os.listdir(foldpath):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                filepaths.append(os.path.join(foldpath, file))
                labels.append(fold)
    return filepaths, labels


def define_df(files: list, classes: list) -> pd.DataFrame:
    return pd.concat([
        pd.Series(files,   name="filepaths"),
        pd.Series(classes, name="labels"),
    ], axis=1)


def split_data(data_dir: str):
    """Stratified 80 / 10 / 10 train / valid / test split (notebook approach)."""
    files, classes = define_paths(data_dir)
    df = define_df(files, classes)

    train_df, dummy_df = train_test_split(
        df, train_size=0.8, shuffle=True, random_state=C.SEED, stratify=df["labels"]
    )
    valid_df, test_df = train_test_split(
        dummy_df, train_size=0.5, shuffle=True, random_state=C.SEED, stratify=dummy_df["labels"]
    )
    return train_df, valid_df, test_df


def create_gens(train_df, valid_df, test_df, batch_size: int):
    """Build ImageDataGenerator flows from DataFrames (notebook approach)."""
    img_size = C.IMG_SIZE

    ts_length = len(test_df)
    test_batch_size = max(
        sorted([ts_length // n for n in range(1, ts_length + 1)
                if ts_length % n == 0 and ts_length / n <= 80])
    )

    def scalar(img):           # pass-through; EfficientNet has built-in scaling
        return img

    tr_gen = ImageDataGenerator(preprocessing_function=scalar, horizontal_flip=True)
    ts_gen = ImageDataGenerator(preprocessing_function=scalar)

    train_gen = tr_gen.flow_from_dataframe(
        train_df, x_col="filepaths", y_col="labels",
        target_size=img_size, class_mode="categorical",
        color_mode="rgb", shuffle=True, batch_size=batch_size,
    )
    valid_gen = ts_gen.flow_from_dataframe(
        valid_df, x_col="filepaths", y_col="labels",
        target_size=img_size, class_mode="categorical",
        color_mode="rgb", shuffle=True, batch_size=batch_size,
    )
    test_gen = ts_gen.flow_from_dataframe(
        test_df, x_col="filepaths", y_col="labels",
        target_size=img_size, class_mode="categorical",
        color_mode="rgb", shuffle=False, batch_size=test_batch_size,
    )
    return train_gen, valid_gen, test_gen


# ═══════════════════════════════════════════════════════════════════════════════
#  CUSTOM CALLBACK  (from notebook — adaptive LR + best-weight tracking)
# ═══════════════════════════════════════════════════════════════════════════════

class MyCallback(keras.callbacks.Callback):
    """
    Adaptive learning-rate callback with:
      • LR reduction when monitored metric plateaus
      • Early stopping after `stop_patience` LR reductions
      • Best-weight restoration at end of training
      • Optional interactive halt prompts (disabled in non-interactive mode)
    """

    def __init__(self, model, patience, stop_patience, threshold,
                 factor, batches, epochs, ask_epoch, interactive=False):
        super().__init__()
        self._model          = model
        self.patience        = patience
        self.stop_patience   = stop_patience
        self.threshold       = threshold
        self.factor          = factor
        self.batches         = batches
        self.epochs          = epochs
        self.ask_epoch       = ask_epoch
        self.ask_epoch_init  = ask_epoch
        self.interactive     = interactive

        self.count           = 0
        self.stop_count      = 0
        self.best_epoch      = 1
        self.initial_lr      = float(model.optimizer.learning_rate)
        self.highest_tracc   = 0.0
        self.lowest_vloss    = np.inf
        self.best_weights    = model.get_weights()
        self.initial_weights = model.get_weights()

    def on_train_begin(self, logs=None):
        if self.interactive:
            ans = input("Do you want model to ask you to halt training [y/n]? ")
            self.ask_permission = 1 if ans.lower() == "y" else 0
        else:
            self.ask_permission = 0

        header = (f"{'Epoch':^8s}{'Loss':^10s}{'Accuracy':^9s}{'V_loss':^9s}"
                  f"{'V_acc':^9s}{'LR':^9s}{'Next LR':^9s}"
                  f"{'Monitor':^10s}{'% Improv':^10s}{'Duration':^8s}")
        print(header)
        self.start_time = time.time()

    def on_train_end(self, logs=None):
        elapsed = time.time() - self.start_time
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)
        s = elapsed % 60
        print(f"\nTraining elapsed: {h}h {m}m {s:.2f}s")
        self._model.set_weights(self.best_weights)   # restore best weights
        print(f"Best epoch: {self.best_epoch}  |  Best val_loss: {self.lowest_vloss:.4f}")

    def on_train_batch_end(self, batch, logs=None):
        acc  = logs.get("accuracy", 0) * 100
        loss = logs.get("loss", 0)
        batches = self.batches
        msg = f"\r  batch {batch+1:4d}/{batches}  acc={acc:6.2f}%  loss={loss:.4f}"
        print(msg, end="", flush=True)

    def on_epoch_end(self, epoch, logs=None):
        print()   # newline after batch progress
        ep_start = time.time()

        tr_acc   = logs.get("accuracy",     0)
        tr_loss  = logs.get("loss",         0)
        val_acc  = logs.get("val_accuracy", 0)
        val_loss = logs.get("val_loss",     0)
        cur_lr   = float(self._model.optimizer.learning_rate)

        # Decide whether to monitor train-acc or val-loss
        if tr_acc < self.threshold:
            monitor   = "train_acc"
            if tr_acc > self.highest_tracc:
                self.highest_tracc = tr_acc
                self.best_weights  = self._model.get_weights()
                self.count         = 0
                self.stop_count    = 0
                self.best_epoch    = epoch + 1
                improve            = (tr_acc - self.initial_lr) / self.initial_lr * 100
            else:
                self.count += 1
                improve = 0
        else:
            monitor = "val_loss"
            if val_loss < self.lowest_vloss:
                self.lowest_vloss = val_loss
                self.best_weights = self._model.get_weights()
                self.count        = 0
                self.stop_count   = 0
                self.best_epoch   = epoch + 1
                improve           = (self.lowest_vloss - val_loss) / self.lowest_vloss * 100
            else:
                self.count += 1
                improve = 0

        next_lr = cur_lr
        if self.count >= self.patience:
            next_lr = cur_lr * self.factor
            self._model.optimizer.learning_rate.assign(next_lr)
            self.count      = 0
            self.stop_count += 1

        duration = time.time() - ep_start
        print(
            f"  {epoch+1:^8d}{tr_loss:^10.4f}{tr_acc*100:^9.2f}"
            f"{val_loss:^9.4f}{val_acc*100:^9.2f}"
            f"{cur_lr:^9.2e}{next_lr:^9.2e}"
            f"{monitor:^10s}{improve:^10.2f}{duration:^8.2f}s"
        )

        # Check for early stop
        if self.stop_count >= self.stop_patience:
            print(f"\n  Early stopping triggered at epoch {epoch+1}")
            self._model.stop_training = True

        # Optional interactive halt
        if self.interactive and self.ask_permission == 1:
            self.ask_epoch -= 1
            if self.ask_epoch == 0:
                ans = input("\nContinue training? [y/n] ")
                if ans.lower() == "n":
                    self._model.stop_training = True
                else:
                    self.ask_epoch = self.ask_epoch_init


# ═══════════════════════════════════════════════════════════════════════════════
#  MODEL FACTORIES
# ═══════════════════════════════════════════════════════════════════════════════

def build_efficientnet(n_classes: int):
    """
    EfficientNetB3 transfer-learning model — matches the notebook's 99.6 % recipe.
    Architecture:
        EfficientNetB3 (imagenet, pooling='max')
        → BatchNorm → Dense(256, relu, L2+L1 reg) → Dropout(0.45)
        → Dense(n_classes, softmax)
    """
    base = tf.keras.applications.efficientnet.EfficientNetB3(
        include_top=False, weights="imagenet",
        input_shape=(*C.IMG_SIZE, 3), pooling="max",
    )
    base.trainable = False

    model = Sequential([
        base,
        BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001),
        Dense(256,
              kernel_regularizer=regularizers.l2(0.016),
              activity_regularizer=regularizers.l1(0.006),
              bias_regularizer=regularizers.l1(0.006),
              activation="relu"),
        Dropout(rate=0.45, seed=C.SEED),
        Dense(n_classes, activation="softmax"),
    ], name="efficientnetb3_classifier")
    return model, base


def build_mobilenet(n_classes: int):
    """MobileNetV2 transfer-learning model (lighter, faster to train)."""
    inp  = keras.Input((*C.IMG_SIZE, 3))
    x    = layers.Rescaling(1.0 / 127.5, offset=-1.0)(inp)
    base = keras.applications.MobileNetV2(
        include_top=False, weights="imagenet", input_shape=(*C.IMG_SIZE, 3)
    )
    base.trainable = False
    x   = base(x, training=False)
    x   = layers.GlobalAveragePooling2D()(x)
    x   = layers.Dense(512, activation="relu")(x)
    x   = layers.Dropout(0.3)(x)
    out = layers.Dense(n_classes, activation="softmax")(x)
    return keras.Model(inp, out, name="mobilenetv2_classifier"), base


def build_cnn(n_classes: int):
    """Custom CNN trained from scratch (simplest baseline)."""
    inp = keras.Input((*C.IMG_SIZE, 3))
    x   = layers.Rescaling(1.0 / 255.0)(inp)
    for f in (32, 64, 128, 256):
        x = layers.Conv2D(f, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPooling2D()(x)
    x   = layers.GlobalAveragePooling2D()(x)
    x   = layers.Dense(256, activation="relu")(x)
    x   = layers.Dropout(0.4)(x)
    out = layers.Dense(n_classes, activation="softmax")(x)
    return keras.Model(inp, out, name="custom_cnn"), None


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTTING  (enhanced notebook version)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_training(hist) -> None:
    """Plot training/validation curves with best-epoch markers (notebook style)."""
    tr_acc   = hist.history["accuracy"]
    tr_loss  = hist.history["loss"]
    val_acc  = hist.history["val_accuracy"]
    val_loss = hist.history["val_loss"]

    idx_loss = int(np.argmin(val_loss))
    idx_acc  = int(np.argmax(val_acc))
    Epochs   = list(range(1, len(tr_acc) + 1))

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    fig.patch.set_facecolor("#0f172a")
    plt.style.use("fivethirtyeight")

    for ax in axes:
        ax.set_facecolor("#1e293b")
        ax.tick_params(colors="#94a3b8")
        for spine in ax.spines.values():
            spine.set_color("#334155")

    # Loss
    axes[0].plot(Epochs, tr_loss,  "r",  label="Training loss",   linewidth=2)
    axes[0].plot(Epochs, val_loss, "g",  label="Validation loss",  linewidth=2)
    axes[0].scatter(idx_loss + 1, val_loss[idx_loss], s=150, c="cyan",
                    label=f"Best epoch = {idx_loss + 1}", zorder=5)
    axes[0].set_title("Training & Validation Loss", color="#e2e8f0", fontsize=14)
    axes[0].set_xlabel("Epochs", color="#94a3b8")
    axes[0].set_ylabel("Loss",   color="#94a3b8")
    axes[0].legend(facecolor="#0f172a", labelcolor="#e2e8f0")

    # Accuracy
    axes[1].plot(Epochs, tr_acc,  "r", label="Training Accuracy",   linewidth=2)
    axes[1].plot(Epochs, val_acc, "g", label="Validation Accuracy",  linewidth=2)
    axes[1].scatter(idx_acc + 1, val_acc[idx_acc], s=150, c="cyan",
                    label=f"Best epoch = {idx_acc + 1}", zorder=5)
    axes[1].set_title("Training & Validation Accuracy", color="#e2e8f0", fontsize=14)
    axes[1].set_xlabel("Epochs",   color="#94a3b8")
    axes[1].set_ylabel("Accuracy", color="#94a3b8")
    axes[1].legend(facecolor="#0f172a", labelcolor="#e2e8f0")

    fig.tight_layout()
    out = C.OUTPUT_DIR / "training_curves.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[✓] Training curves → {out}")


def evaluate(model, test_gen, classes: list) -> None:
    """Confusion matrix + classification report (notebook style)."""
    preds  = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(preds, axis=1)
    y_true = test_gen.classes

    report = classification_report(y_true, y_pred, target_names=classes, digits=4)
    print(report)
    rpt_path = C.OUTPUT_DIR / "classification_report.txt"
    rpt_path.write_text(report)
    print(f"[✓] Classification report → {rpt_path}")

    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(20, 18))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    sns.heatmap(cm, ax=ax, cmap="YlGn",
                xticklabels=classes, yticklabels=classes,
                cbar=False, linewidths=0.3, linecolor="#1e293b")
    ax.set_xlabel("Predicted", color="#94a3b8", fontsize=11)
    ax.set_ylabel("True",      color="#94a3b8", fontsize=11)
    ax.tick_params(colors="#94a3b8")
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(fontsize=6)
    plt.title("Confusion Matrix", color="#e2e8f0", fontsize=14, pad=12)
    plt.tight_layout()
    cm_path = C.OUTPUT_DIR / "confusion_matrix.png"
    fig.savefig(cm_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[✓] Confusion matrix      → {cm_path}")


def save_class_csv(train_gen, subject: str = "Plant Village Disease") -> None:
    """Save class-index CSV (notebook approach — for portability)."""
    class_dict = train_gen.class_indices
    img_size   = train_gen.image_shape
    df = pd.DataFrame({
        "class_index": list(class_dict.values()),
        "class":       list(class_dict.keys()),
        "height":      [img_size[0]] * len(class_dict),
        "width":       [img_size[1]] * len(class_dict),
    })
    csv_path = C.MODEL_PATH.parent / f"{subject.replace(' ', '_')}-class_dict.csv"
    df.to_csv(csv_path, index=False)
    print(f"[✓] Class CSV             → {csv_path}")

    # Also keep the JSON used by predict.py
    class_names = [k for k, _ in sorted(class_dict.items(), key=lambda x: x[1])]
    C.CLASSES_PATH.write_text(json.dumps(class_names, indent=2))
    print(f"[✓] class_names.json      → {C.CLASSES_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    ap = argparse.ArgumentParser(description="Train plant disease classifier")
    ap.add_argument("--model", choices=["efficientnet", "mobilenet", "cnn"],
                    default="efficientnet",
                    help="Backbone to use (default: efficientnet)")
    ap.add_argument("--epochs", type=int, default=40,
                    help="Max training epochs (default: 40)")
    ap.add_argument("--batch_size", type=int, default=40,
                    help="Batch size (default: 40, as in notebook)")
    ap.add_argument("--fine_tune_epochs", type=int, default=0,
                    help="Fine-tune epochs for mobilenet (ignored for efficientnet/cnn)")
    ap.add_argument("--patience", type=int, default=1,
                    help="LR patience epochs (default: 1)")
    ap.add_argument("--stop_patience", type=int, default=3,
                    help="Stop after N LR reductions (default: 3)")
    ap.add_argument("--threshold", type=float, default=0.9,
                    help="Train-acc threshold to switch monitor (default: 0.9)")
    ap.add_argument("--factor", type=float, default=0.5,
                    help="LR reduction factor (default: 0.5)")
    ap.add_argument("--ask_epoch", type=int, default=5,
                    help="Ask-to-halt interval in epochs (default: 5)")
    args = ap.parse_args()

    # ── Setup ─────────────────────────────────────────────────────────────────
    C.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    C.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{'═'*65}")
    print("  🌿  Smart Plant Disease Identification — Training")
    print(f"      Backbone : {args.model.upper()}")
    print(f"      Epochs   : {args.epochs}   Batch : {args.batch_size}")
    print(f"{'═'*65}\n")

    if not C.DATA_DIR.exists():
        raise FileNotFoundError(
            f"Data directory not found: {C.DATA_DIR}\n\n"
            "Download the dataset first:\n"
            "  kaggle datasets download -d abdallahalidev/plantvillage-dataset"
            " -p data --unzip\n"
            f"Then confirm config.DATA_DIR points to the 'color' folder."
        )

    t0 = time.time()

    # ── Data ──────────────────────────────────────────────────────────────────
    train_df, valid_df, test_df = split_data(str(C.DATA_DIR))
    print(f"[✓] Dataset split → train:{len(train_df):,}  "
          f"valid:{len(valid_df):,}  test:{len(test_df):,}")

    train_gen, valid_gen, test_gen = create_gens(
        train_df, valid_df, test_df, args.batch_size
    )
    n_classes = len(train_gen.class_indices)
    print(f"[✓] Classes: {n_classes}")

    # ── Build model ───────────────────────────────────────────────────────────
    if args.model == "efficientnet":
        model, base = build_efficientnet(n_classes)
        model.compile(
            optimizer=Adamax(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
    elif args.model == "mobilenet":
        model, base = build_mobilenet(n_classes)
        model.compile(
            optimizer=keras.optimizers.Adam(1e-3),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
    else:
        model, base = build_cnn(n_classes)
        model.compile(
            optimizer=keras.optimizers.Adam(1e-3),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

    model.summary()

    # ── Callbacks ─────────────────────────────────────────────────────────────
    batches = int(np.ceil(len(train_gen.labels) / args.batch_size))

    # Keras standard checkpoint (save best val_accuracy)
    ckpt = keras.callbacks.ModelCheckpoint(
        str(C.MODEL_PATH), monitor="val_accuracy",
        save_best_only=True, verbose=0,
    )

    my_cb = MyCallback(
        model=model,
        patience=args.patience,
        stop_patience=args.stop_patience,
        threshold=args.threshold,
        factor=args.factor,
        batches=batches,
        epochs=args.epochs,
        ask_epoch=args.ask_epoch,
        interactive=False,         # set True for notebook-style interactive halts
    )

    # ── Phase 1: train head ───────────────────────────────────────────────────
    print(f"\n[Phase 1] Training head for up to {args.epochs} epoch(s)…")
    history = model.fit(
        train_gen,
        epochs=args.epochs,
        verbose=0,
        callbacks=[my_cb, ckpt],
        validation_data=valid_gen,
        shuffle=False,
    )

    # ── Phase 2: fine-tune (MobileNet only) ──────────────────────────────────
    if base is not None and args.fine_tune_epochs > 0 and args.model == "mobilenet":
        print(f"\n[Phase 2] Fine-tuning last 30 MobileNet layers "
              f"for {args.fine_tune_epochs} epoch(s)…")
        base.trainable = True
        for layer in base.layers[:-30]:
            layer.trainable = False
        model.compile(
            optimizer=keras.optimizers.Adam(1e-5),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        batches2 = int(np.ceil(len(train_gen.labels) / args.batch_size))
        my_cb2 = MyCallback(
            model=model, patience=args.patience,
            stop_patience=args.stop_patience, threshold=args.threshold,
            factor=args.factor, batches=batches2,
            epochs=args.fine_tune_epochs, ask_epoch=args.ask_epoch,
            interactive=False,
        )
        model.fit(
            train_gen,
            epochs=args.fine_tune_epochs,
            verbose=0,
            callbacks=[my_cb2, ckpt],
            validation_data=valid_gen,
            shuffle=False,
        )

    # ── Reload best checkpoint & evaluate ────────────────────────────────────
    print(f"\n[✓] Loading best checkpoint…")
    model = keras.models.load_model(str(C.MODEL_PATH))

    # Evaluate on all three splits
    subject  = "Plant_Village_Disease"
    ts_length = len(test_df)
    test_batch = max(
        sorted([ts_length // n for n in range(1, ts_length + 1)
                if ts_length % n == 0 and ts_length / n <= 80])
    )

    for split_name, gen in [("Train", train_gen), ("Valid", valid_gen), ("Test", test_gen)]:
        steps = len(gen.labels) // gen.batch_size
        score = model.evaluate(gen, steps=steps, verbose=0)
        print(f"  {split_name:5s}  loss={score[0]:.4f}  acc={score[1]*100:.2f}%")

    # ── Save outputs ──────────────────────────────────────────────────────────
    # Also save as .h5 for broad compatibility (as notebook does)
    h5_path = C.MODEL_PATH.with_suffix(".h5")
    model.save(str(h5_path))
    print(f"[✓] H5 model saved        → {h5_path}")

    plot_training(history)

    classes = list(train_gen.class_indices.keys())
    evaluate(model, test_gen, classes)
    save_class_csv(train_gen, subject)

    elapsed = time.time() - t0
    print(f"\n{'═'*65}")
    print(f"  ✅  Done in {elapsed/60:.1f} min")
    print(f"     Keras model : {C.MODEL_PATH}")
    print(f"     H5 model    : {h5_path}")
    print(f"     Charts      : {C.OUTPUT_DIR}/")
    print(f"{'═'*65}\n")


if __name__ == "__main__":
    main()
