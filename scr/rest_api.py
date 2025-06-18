from fastapi import FastAPI
from core.model import CreditModel

app = FastAPI()
model = CreditModel()

@app.post("/predict")
async def predict(data: dict):
    try:
        prediction = model.predict(data)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        return {"error": str(e)}