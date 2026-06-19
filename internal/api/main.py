from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from internal.services.model_registry import MODEL_REGISTRY
from internal.services.classifier import predict
from internal.services.relevancy import search
from internal.services.explainer import generate_explanation


class TextRequest(BaseModel):
    text: str


app = FastAPI(title="Veritas")


# ============================================================
# HELPERS
# ============================================================

def get_agreement(prediction, relevancy):

    if not relevancy["label_counts"]:
        return False

    retrieved_label = max(
        relevancy["label_counts"],
        key=relevancy["label_counts"].get,
    )

    return (
        retrieved_label.lower()
        ==
        prediction["label"].lower()
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Veritas API Running",
        "models": list(MODEL_REGISTRY.keys()),
    }


# ============================================================
# MODELS
# ============================================================

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
        raise HTTPException(
            status_code=404,
            detail=f"Unknown model: {model_name}"
        )

    relevancy = search(
        model_name=model_name,
        text=request.text,
    )

    if not relevancy["relevant"]:
        return {
            "success": False,
            "reason": "out_of_domain_input",
            "relevancy": relevancy,
        }

    prediction = predict(
        model_name=model_name,
        text=request.text,
    )

    agreement = get_agreement(
        prediction,
        relevancy,
    )

    explanation = generate_explanation(
        model_name=model_name,
        text=request.text,
        prediction=prediction,
        relevancy=relevancy,
        agreement=agreement,
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


@app.post("/emotion")
def emotion_analysis(request: TextRequest):

    sentiment_relevancy = search(
        model_name="sentiment",
        text=request.text,
    )

    emotion7_relevancy = search(
        model_name="emotion_7",
        text=request.text,
    )

    emotion16_relevancy = search(
        model_name="emotion_16",
        text=request.text,
    )

    sentiment_prediction = predict(
        model_name="sentiment",
        text=request.text,
    )

    emotion7_prediction = predict(
        model_name="emotion_7",
        text=request.text,
    )

    emotion16_prediction = predict(
        model_name="emotion_16",
        text=request.text,
    )

    sentiment_agreement = get_agreement(
        sentiment_prediction,
        sentiment_relevancy,
    )

    emotion7_agreement = get_agreement(
        emotion7_prediction,
        emotion7_relevancy,
    )

    emotion16_agreement = get_agreement(
        emotion16_prediction,
        emotion16_relevancy,
    )

    explanation = generate_explanation(
        model_name="emotion",
        text=request.text,
        prediction={
            "sentiment": sentiment_prediction,
            "emotion_7": emotion7_prediction,
            "emotion_16": emotion16_prediction,
        },
        relevancy={
            "sentiment": sentiment_relevancy,
            "emotion_7": emotion7_relevancy,
            "emotion_16": emotion16_relevancy,
        },
        agreement={
            "sentiment": sentiment_agreement,
            "emotion_7": emotion7_agreement,
            "emotion_16": emotion16_agreement,
        },
    )

    return {
        "success": True,
        "user_text": request.text,

        "sentiment": {
            "prediction": sentiment_prediction,
            "agreement": sentiment_agreement,
            "relevancy": sentiment_relevancy,
        },

        "emotion_7": {
            "prediction": emotion7_prediction,
            "agreement": emotion7_agreement,
            "relevancy": emotion7_relevancy,
        },

        "emotion_16": {
            "prediction": emotion16_prediction,
            "agreement": emotion16_agreement,
            "relevancy": emotion16_relevancy,
        },

        "model_response": explanation,
    }