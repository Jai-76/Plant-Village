"""HTTP inference API for deployment on Railway or another Python host."""

from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from disease_info import DISEASE_INFO
from predict import predict, pretty

app = FastAPI(title="PlantGuard AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
async def predict_leaf(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Upload a valid image file.")

    try:
        image = Image.open(BytesIO(await file.read()))
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="The uploaded file is not a readable image.") from exc

    try:
        results = predict(image, top_k=3)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    predictions = []
    for name, probability in results:
        crop, condition = pretty(name)
        details = DISEASE_INFO.get(name, {})
        predictions.append(
            {
                "class_name": name,
                "crop": crop,
                "condition": condition,
                "probability": round(float(probability), 6),
                "description": details.get("description", ""),
                "treatment": details.get("treatment", []),
            }
        )
    return {"predictions": predictions}
