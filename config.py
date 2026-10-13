"""Configuration for the Smart Plant Disease Identification System."""
from pathlib import Path

ROOT = Path(__file__).parent

# ── Data ──────────────────────────────────────────────────────────────────────
# After running: kaggle datasets download -d abdallahalidev/plantvillage-dataset -p data --unzip
# the color images will be at:  data/plantvillage dataset/color/<ClassName>/<image>.jpg
DATA_DIR = Path(r"D:\PlantVillage")

# ── Model artefacts ───────────────────────────────────────────────────────────
MODEL_PATH   = ROOT / "models" / "plant_disease_model.keras"
CLASSES_PATH = ROOT / "models" / "class_names.json"

# ── Training hyper-parameters ─────────────────────────────────────────────────
IMG_SIZE   = (224, 224)   # MobileNetV2 / custom-CNN input
BATCH_SIZE = 32
SEED       = 42

# ── Dataset split ratios (must sum ≤ 1.0) ────────────────────────────────────
TEST_SPLIT = 0.10
VAL_SPLIT  = 0.10

# ── Output directory (training curves, reports, confusion matrix) ─────────────
OUTPUT_DIR = ROOT / "outputs"
