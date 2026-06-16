import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct,VectorParams, Distance
from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "spam_relevancy"
SIMILARITY_THRESHOLD = 0.40

print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

embedding_size = (embedding_model.get_embedding_dimension())
print("Embedding Size:", embedding_size)

print("Loading dataset...")
df = pd.read_csv(
    "./models/sms_spam/spam.csv",
    encoding="utf-8-sig"
)

df = df[["v1", "v2"]]
df = df.rename(
    columns={
        "v1": "label",
        "v2": "text"
    }
)

df = df.dropna(subset=["text"])
df = df.drop_duplicates(subset=["text"])
print("Dataset Size:", len(df))

client = QdrantClient(path="./qdrant_database")

existing = [c.name for c in client.get_collections().collections]

if COLLECTION_NAME not in existing:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=embedding_size,
            distance=Distance.COSINE
        )
    )


    print("Creating embeddings...")

    points = []
    for idx, row in df.iterrows():
        vector = embedding_model.encode(row["text"]).tolist()

        points.append(
            PointStruct(
                id=int(idx),
                vector=vector,
                payload={"text": row["text"], "label": row["label"]
                }
            )
        )

    print("Uploading to Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Done.")
else: 
    print("using existing collection...")


def search(query, top_k=5):
    query_vector = embedding_model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    )


    top_score = (results.points[0].score if results.points else 0)
    scores = [p.score for p in results.points[:3]] 
    avg_score = sum(scores) / len(scores)
    spam_count = 0
    ham_count = 0

    for hit in results.points[:3]:

        if hit.payload["label"] == "spam":
            spam_count += 1
        else:
            ham_count += 1
    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)
    print("=" * 80)

    print(f"Average Top-3: {avg_score:.4f}")
    print( f"Top Similarity: {top_score:.4f}")
    if avg_score < SIMILARITY_THRESHOLD or top_score < SIMILARITY_THRESHOLD:
        print("\n❌ Out-of-domain input.")
        return {
            "relevant": False,
            "top_similarity": top_score,
            "avg_similarity": avg_score,
            "matches": []
        }

    print("\n✅ Relevant to Spam Classifier")

    print("\nTop Matches:\n")
    for hit in results.points:
        print(f"Score: {hit.score:.4f}")
        print(f"Label: {hit.payload['label']}")
        print(f"Text: {hit.payload['text']}")
        print("-" * 60)
        return {
            "spam_neighbors": spam_count,
            "ham_neighbors": ham_count,
            "relevant": True,
            "top_similarity": top_score,
            "avg_similarity": avg_score,
            "matches": [
                {
                    "score": hit.score,
                    "label": hit.payload["label"],
                    "text": hit.payload["text"]
                }
                for hit in results.points
            ]
        }


# tests = [
#     "Congratulations! You have won ₹5000. Click here to claim your reward.",
#     "URGENT: Your SBI account has been suspended. Verify your identity immediately using the link below.",
#     "How do I reverse a linked list in C++?",
#     "Write a Python function to sort a list.",
#     "Hey bro let's meet at 7pm near the station.",
#     "FREE AMAZON GIFT CARD. CLAIM NOW.",
#     "What is the capital of France?"
# ]

# for test in tests:
#     search(test)
    
# client.close()