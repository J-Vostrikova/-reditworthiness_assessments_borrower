from fastapi import FastAPI
from src.model import CreditScoringModel

app = FastAPI(title="Credit Scoring API")  # Интерфейс для внешних систем (Задача 2.2)

@app.post("/predict")
async def predict(data: dict):
    """REST API для интеграции с CRM"""
    try:
        model = CreditScoringModel()
        prediction = model.predict(data)
        return {"decision": prediction, "status": "success"}
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return {"status": "error", "message": str(e)}