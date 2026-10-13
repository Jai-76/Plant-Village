# 🌿 Smart Plant Disease Identification System

> **EfficientNetB3-based leaf-image classifier** trained on the PlantVillage dataset.  
> Identify 38 crop-disease combinations from a single leaf photo — **99.6% accuracy**.

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Primary arch** | **EfficientNetB3** (Adamax, 99.6 % accuracy — from reference notebook) |
| **Alt arch** | MobileNetV2 (lighter) · Custom CNN (from-scratch baseline) |
| **Classes** | 38 disease / healthy states across 14 crop types |
| **Data pipeline** | ImageDataGenerator + DataFrame flow (80/10/10 stratified split) |
| **Custom callback** | Adaptive LR, best-weight tracking, early stopping |
| **Web UI** | Premium dark-themed Streamlit app with real-time diagnosis |
| **CLI** | `predict.py` for single or batch image inference |
| **Outputs** | Training curves · Classification report · Confusion matrix · Class CSV |

---

## 🚀 Quick-start

### 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### 2 — Download the PlantVillage dataset
```bash
# Obtain your Kaggle API token from kaggle.com > Settings > Create New Token
# Place kaggle.json in ~/.kaggle/kaggle.json, then:
kaggle datasets download -d abdallahalidev/plantvillage-dataset -p data --unzip
```

Confirm that `config.DATA_DIR` points to the `color` sub-folder (the one that contains class sub-directories like `Apple___Apple_scab`).

### 3 — Train
```bash
# Recommended (MobileNetV2, ~30 min on GPU)
python train.py --model mobilenet --epochs 10 --fine_tune_epochs 5

# From-scratch CNN baseline
python train.py --model cnn --epochs 25
```

**Training outputs** are written to `outputs/`:
- `training_curves.png` — accuracy & loss per epoch
- `classification_report.txt` — per-class precision / recall / F1
- `confusion_matrix.png` — heatmap

The best checkpoint is saved to `models/plant_disease_model.keras`.

### 4 — Run the web app
```bash
streamlit run app.py
```

### 5 — CLI inference
```bash
# Single image
python predict.py leaf.jpg

# Batch
python predict.py field1.jpg field2.jpg field3.png
```

---

## 🧠 Architecture

```
Input (224×224×3)
  │
  ├─ Augmentation (flip, rotate, zoom, contrast, brightness)   ← training only
  ├─ Rescaling → [-1, 1]
  │
  ├─ MobileNetV2 backbone (frozen in phase 1)
  │    └─ Last 30 layers unfrozen in phase 2 (fine-tuning)
  │
  ├─ GlobalAveragePooling2D
  ├─ Dense(512, relu)
  ├─ Dropout(0.3)
  └─ Dense(38, softmax)   →   disease probabilities
```

---

## 📂 Project structure

```
plant_disease_system/
├── app.py             – Streamlit web UI
├── train.py           – Training script
├── predict.py         – Inference (CLI + API)
├── config.py          – Paths & hyper-parameters
├── requirements.txt
├── data/
│   └── plantvillage dataset/
│       └── color/     ← class sub-folders here
├── models/
│   ├── plant_disease_model.keras
│   └── class_names.json
└── outputs/
    ├── training_curves.png
    ├── classification_report.txt
    └── confusion_matrix.png
```

---

## ⚠️ Notes & Limitations

- **Plain backgrounds**: PlantVillage images are taken against clean backgrounds. Accuracy on real field photos with soil, shadows, or multiple leaves will be lower. Mitigate by adding field-condition images and stronger augmentation.
- **Split strategy**: Stratified 80 / 10 / 10 train / val / test split prevents class-imbalance leakage.
- **First-level tool only**: Always confirm results with a qualified agronomist or plant pathologist.

---

## 🌱 Supported crops

Apple · Blueberry · Cherry · Corn · Grape · Orange · Peach · Pepper · Potato · Raspberry · Soybean · Squash · Strawberry · Tomato
