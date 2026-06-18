from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("./internal/models/sentiments/sentiment_model")
model = AutoModelForSequenceClassification.from_pretrained("./internal/models/sentiments/sentiment_model")

id2label = {
    0: "negative",
    1: "positive"
}

tests = [
    "I loved this movie",
    "Worst movie ever",
    "Movie bahut mast thi",
    "Ye movie bakwaas thi",
    "Mujhe ye product pasand aaya",
    "This service is terrible"
]

for text in tests:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)

    prediction = torch.argmax(probs, dim=1).item()

    confidence = probs[0][prediction].item()

    print({
        "label": id2label[prediction],
        "confidence": confidence
    })