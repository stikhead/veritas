import os
from functools import lru_cache
from typing import Dict, Any, List
from dotenv import load_dotenv
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct,VectorParams, Distance
from sentence_transformers import SentenceTransformer

from internal.services.model_registry import MODEL_REGISTRY

SIMILARITY_THRESHOLD_FALLBACK = 0.40
load_dotenv()

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@lru_cache(maxsize=1)
def get_qdrant_client():
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_path = os.getenv("QDRANT_PATH", "./internal/qdrant_database")

    if qdrant_url:
        return QdrantClient(url=qdrant_url)

    return QdrantClient(path=qdrant_path)


def ensure_collection(collection_name: str):
    client = get_qdrant_client()
    model = get_embedding_model()
    dim = model.get_embedding_dimension()
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

def build_collection_from_csv(csv_path: str, collection_name: str, text_col: str = "text", label_col: str = "label"):
    client = get_qdrant_client()
    model = get_embedding_model()

    ensure_collection(collection_name)

    df = pd.read_csv(csv_path)
    df = df.dropna(subset=[text_col])
    df = df.drop_duplicates(subset=[text_col])

    points: List[PointStruct] = []

    for idx, row in df.iterrows():
        text = str(row[text_col])
        label = str(row[label_col])

        vector = model.encode(text).tolist()

        points.append(
            PointStruct(
                id=int(idx),
                vector=vector,
                payload={
                    "text": text,
                    "label": label,
                },
            )
        )

    if points:
        client.upsert(collection_name=collection_name, points=points)

    return {"collection": collection_name, "points": len(points)}


def search(model_name: str, text: str, top_k: int = 5) -> Dict[str, Any]:
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_name}")

    spec = MODEL_REGISTRY[model_name]
    client = get_qdrant_client()
    model = get_embedding_model()

    ensure_collection(spec.collection_name)

    query_vector = model.encode(text).tolist()

    results = client.query_points(
        collection_name=spec.collection_name,
        query=query_vector,
        limit=top_k,
    )

    points = results.points or []

    if not points:
        return {
            "relevant": False,
            "top_similarity": 0.0,
            "avg_similarity": 0.0,
            "spam_neighbors": 0,
            "ham_neighbors": 0,
            "matches": [],
        }

    scores = [float(p.score) for p in points]
    top_similarity = scores[0]
    avg_similarity = sum(scores) / len(scores)

    spam_neighbors = 0
    ham_neighbors = 0

    matches = []
    for hit in points:
        payload = hit.payload or {}
        label = str(payload.get("label", "")).lower()
        if label == "spam":
            spam_neighbors += 1
        elif label == "ham":
            ham_neighbors += 1

        matches.append(
            {
                "score": round(float(hit.score), 4),
                "label": payload.get("label"),
                "text": payload.get("text"),
            }
        )

    threshold = spec.similarity_threshold or SIMILARITY_THRESHOLD_FALLBACK
    relevant = top_similarity >= threshold and avg_similarity >= threshold

    return {
        "relevant": relevant,
        "top_similarity": round(top_similarity, 4),
        "avg_similarity": round(avg_similarity, 4),
        "spam_neighbors": spam_neighbors,
        "ham_neighbors": ham_neighbors,
        "matches": matches,
    }