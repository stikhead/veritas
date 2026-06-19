from functools import lru_cache
from typing import Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from internal.services.model_registry import MODEL_REGISTRY

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


@lru_cache(maxsize=8)
def load_model(model_name: str):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"unknown model: {model_name}")
    
    spec = MODEL_REGISTRY[model_name]
    tokenizer=AutoTokenizer.from_pretrained(spec.model_path)
    model = AutoModelForSequenceClassification.from_pretrained(spec.model_path)

    model.to(DEVICE)
    model.eval()

    return tokenizer, model

def predict(model_name: str, text: str):

    tokenizer, model = load_model(model_name)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits,dim=-1)[0]

    pred_id = int(torch.argmax(probs).item())

    if hasattr(model.config, "id2label"):
        label = model.config.id2label[pred_id]
    else:
        label = MODEL_REGISTRY[model_name].labels[pred_id]

    probability_map = {
        model.config.id2label[i]: round(float(p), 4)
        for i, p in enumerate(probs.cpu().tolist())
    }

    return {
        "label": label,
        "confidence": round(float(probs[pred_id]), 4),
        "probabilities": probability_map,
    }