from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass(frozen=True)
class ModelSpec:
    model_path: str
    collection_name: str
    labels: Tuple[str, ...]
    similarity_threshold: float = 0.40


MODEL_REGISTRY: Dict[str, ModelSpec] = {
    "spam": ModelSpec(
        model_path="./internal/models/sms_spam/sms_spam_model_v2",
        collection_name="sms_relevancy",
        labels=("ham", "spam"),
        similarity_threshold=0.40
    ),
    
    "sentiment": ModelSpec(
        model_path="./internal/models/sentiments/sentiment_model",
        collection_name="sentiment_relevancy",
        labels=("negative", "positive"),
        similarity_threshold=0.50
    ),
    "emotion_7": ModelSpec(
        model_path="./internal/models/emotions/emotion_model",
        collection_name="emotion7_relevancy",
        labels=("anger","fear","joy","love","sadness","surprise","neutral",),
        similarity_threshold=0.55,
    ),
    "emotion_16": ModelSpec(
        model_path="./internal/models/emotions/emotion_model_v2",
        collection_name="emotion16_relevancy",
        labels=("admiration","amusement","anger","confusion","curiosity","disgust","embarrassment","fear","gratitude","joy","love","neutral","optimism","remorse","sadness","surprise"),
        similarity_threshold=0.55
    )
}