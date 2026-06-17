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
        collection_name="spam_relevancy",
        labels=("ham", "spam"),
        similarity_threshold=0.40
    ),
    
    "sentiment": ModelSpec(
        model_path="./internal/models/sentiment/sentiment_model",
        collection_name="sentiment_relevancy",
        labels=("negative", "neutral", "positive"),
        similarity_threshold=0.35
    ),

    "clickbait": ModelSpec(
        model_path="./internal/models/clickbait/clickbait_model",
        collection_name="clickbait_relevancy",
        labels=("not_clickbait", "clickbait"),
        similarity_threshold=0.35
    )
}