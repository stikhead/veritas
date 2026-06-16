from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("./sms_spam_model_v2")
model = AutoModelForSequenceClassification.from_pretrained("./sms_spam_model_v2")

id2label = {
    0: "ham",
    1: "spam"
}

tests = [
    "Congratulations! You have won ₹5000. Click here to claim your reward.",
    
    "URGENT: Your SBI account has been suspended. Verify your identity immediately using the link below.",

    "Dear customer, your package is waiting for delivery. Pay ₹50 processing fee to release it.",

    "WINNER! You have been selected for a FREE Amazon Gift Card worth ₹10,000.",

    "Congratulations! Your KYC verification is pending. Update now to avoid account suspension.",

    "Sir, your parcel has arrived. Please call when available.",

    "Hey bro, let's meet at 7pm near the station.",

    "Hi Team, reminder to submit reimbursement claims by Friday."
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