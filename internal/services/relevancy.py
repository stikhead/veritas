import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "./models/sms_spam/sms_spam_model_v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

def predict(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(
        outputs.logits,
        dim=1
    )

    ham_prob = probs[0][0].item()
    spam_prob = probs[0][1].item()

    if spam_prob > ham_prob:
        label = "spam"
        confidence = spam_prob
    else:
        label = "ham"
        confidence = ham_prob

    return {
        "label": label,
        "confidence": round(confidence,4),
        "spam_probability": round(spam_prob,4),
        "ham_probability": round(ham_prob,4)
    }