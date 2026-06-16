from fastapi import FastAPI
from services.classifier import search
from services.relevancy import predict
from pydantic import BaseModel

class SpamRequest(BaseModel):
    text: str
app = FastAPI(title="Veritas")

@app.get("/")
def root():
    return {
        "message": "Veritas API Running"
    }

@app.post("/classify/spam")
def classify_spam(request: SpamRequest):
    relevancy = search(request.text)

    if not relevancy["relevant"]:
        return {
            "success": False,
            "reason": "out of domain input",
            "relevancy": relevancy
        }
    
    prediction = predict(request.text)

    return {
        "success": True,
        "prediction": prediction,
        "relevancy": relevancy
    }
