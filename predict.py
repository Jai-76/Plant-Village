"""Predict the disease class of one or more leaf images.

Supports both model formats produced by train.py:
    models/plant_disease_model.keras   (preferred)
    models/plant_disease_model.h5      (fallback)

CLI usage:
    python predict.py path/to/leaf.jpg
    python predict.py leaf1.jpg leaf2.png          # batch

API usage (from app.py):
    from predict import predict, pretty
    results = predict(pil_image, top_k=3)
    for name, prob in results:
        crop, condition = pretty(name)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np
from PIL import Image

import config as C

# ─── Lazy-loaded globals ──────────────────────────────────────────────────────
_model = None
_model_backend = None
_classes: List[str] = []


def _find_model() -> Path:
    """Return the best available model file (.keras preferred, .h5 fallback)."""
    if C.MODEL_PATH.exists():
        return C.MODEL_PATH
    h5 = C.MODEL_PATH.with_suffix(".h5")
    if h5.exists():
        return h5
    raise FileNotFoundError(
        f"No trained model found at '{C.MODEL_PATH}' or '{h5}'.\n"
        "Train first:\n"
        "  python train.py --model efficientnet --epochs 40   # 99.6% accuracy\n"
        "  python train.py --model mobilenet   --epochs 10 --fine_tune_epochs 5"
    )


def load() -> Tuple:
    """Load model and class list once, then cache in module globals."""
    global _model, _model_backend, _classes
    if _model is None:
        if not C.CLASSES_PATH.exists():
            import pandas as pd
            csv_candidates = list(C.MODEL_PATH.parent.glob("*class_dict.csv"))
            if csv_candidates:
                df = pd.read_csv(csv_candidates[0]).sort_values("class_index")
                _classes = df["class"].tolist()
                C.CLASSES_PATH.write_text(json.dumps(_classes, indent=2))
            else:
                raise FileNotFoundError(
                    f"Class-name file not found at '{C.CLASSES_PATH}'."
                )
        else:
            _classes = json.loads(C.CLASSES_PATH.read_text())

        # Check for 38-class PyTorch model first (covers all 14 crops)
        pt_model_dir = C.ROOT / "models" / "plant_disease_model_38"
        if pt_model_dir.exists():
            try:
                from transformers import AutoModelForImageClassification
                _model = AutoModelForImageClassification.from_pretrained(
                    str(pt_model_dir), local_files_only=True
                )
                _model.eval()
                _model_backend = "torch"
                print(f"[predict] Model loaded: plant_disease_model_38 (PyTorch MobileNetV2) | {len(_classes)} classes (All crops supported)")
                return _model, _classes
            except Exception as err:
                print(f"[predict] Could not load PyTorch 38-class model ({err}), falling back to Keras...")

        # Fallback to Keras model
        model_path = _find_model()
        from tensorflow import keras
        _model = keras.models.load_model(str(model_path))
        _model_backend = "keras"
        print(f"[predict] Model loaded: {model_path.name} (Keras) | {len(_classes)} classes")
    return _model, _classes


def pretty(name: str) -> Tuple[str, str]:
    """Split a PlantVillage class name 'Crop___Condition' into (crop, condition)."""
    crop, _, cond = name.partition("___")
    crop = crop.replace("_", " ").replace(",", "").strip()
    cond = cond.replace("_", " ").strip() or "unknown"
    return crop, cond


def predict(img: Image.Image, top_k: int = 3) -> List[Tuple[str, float]]:
    """Return top-k (class_name, probability) tuples for the given PIL image."""
    model, classes = load()
    img_rgb = img.convert("RGB")

    if _model_backend == "torch":
        import torch
        import torchvision.transforms as transforms
        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        tensor = preprocess(img_rgb).unsqueeze(0)
        with torch.no_grad():
            outputs = model(tensor)
            probs = torch.nn.functional.softmax(outputs.logits[0], dim=0).cpu().numpy()
    else:
        img_resized = img_rgb.resize(C.IMG_SIZE, Image.BILINEAR)
        x = np.expand_dims(np.asarray(img_resized, dtype="float32"), axis=0)
        probs = model.predict(x, verbose=0)[0]

    top_idx = probs.argsort()[::-1][:top_k]
    return [(classes[i], float(probs[i])) for i in top_idx]


# ─── CLI entry-point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path> [<image_path> ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        p = Path(path)
        if not p.exists():
            print(f"[WARN] File not found: {path}")
            continue
        print(f"\n{'-'*65}")
        print(f"  Image : {path}")
        print(f"{'-'*65}")
        try:
            results = predict(Image.open(p))
            for rank, (name, prob) in enumerate(results, 1):
                crop, cond = pretty(name)
                bar = "#" * int(prob * 30)
                print(f"  #{rank}  {crop:25s}  {cond:35s}  {prob*100:6.2f}%  {bar}")
        except Exception as exc:
            print(f"[ERROR] {exc}")
