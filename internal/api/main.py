from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from internal.services.model_registry import MODEL_REGISTRY
from internal.services.classifier import predict
from internal.services.relevancy import search
from internal.services.explainer import generate_explanation


class TextRequest(BaseModel):
    text: str


app = FastAPI(title="Veritas")


@app.get("/")
def root():
    return {
        "message": "Veritas API Running",
        "models": list(MODEL_REGISTRY.keys()),
    }


@app.get("/models")
def get_models():
    return {
        name: {
            "model_path": spec.model_path,
            "collection_name": spec.collection_name,
            "labels": list(spec.labels),
            "similarity_threshold": spec.similarity_threshold,
        }
        for name, spec in MODEL_REGISTRY.items()
    }


@app.post("/classify/{model_name}")
def classify(model_name: str, request: TextRequest):
    if model_name not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail="Unknown model")

    relevancy = search(model_name, request.text)

    if not relevancy["relevant"]:
        return {
            "success": False,
            "reason": "out of domain input",
            "relevancy": relevancy,
        }

    prediction = predict(model_name, request.text)
    # explanation = build_explanation(
    #     model_name=model_name,
    #     user_text=request.text,
    #     prediction=prediction,
    #     relevancy=relevancy,
    # )

    agreement = False
    if relevancy["spam_neighbors"] > relevancy["ham_neighbors"] and prediction["label"] == "spam":
        agreement = True
    elif relevancy["ham_neighbors"] > relevancy["spam_neighbors"] and prediction["label"] == "ham":
        agreement = True

    explanation = generate_explanation(
        text=request.text,
        prediction=prediction,
        relevancy=relevancy,
        agreement=agreement
    )
    
    return {
        "success": True,
        "model_name": model_name,
        "user_text": request.text,
        "prediction": prediction,
        "relevancy": relevancy,
        "agreement": agreement,
        "model_response": explanation,
    }