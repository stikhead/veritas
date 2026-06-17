from transformers import pipeline
import torch

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

llm = pipeline(
    "text-generation",
    model=MODEL_ID,
    device_map="auto",
    torch_dtype=torch.bfloat16
)


def generate_explanation(text, prediction, relevancy, agreement):
    examples = "\n".join(
        [
            f"[{m['label']}] {m['text']}"
            for m in relevancy["matches"][:3]
        ]
    )

    prompt = f"""
        You are an explainable AI assistant.

        Use ONLY the information provided below.

        Do NOT infer identities.
        Do NOT assume relationships.
        Do NOT invent context.
        Do NOT add facts not present in the message.

        Label Definitions:
        - ham = legitimate message
        - spam = unwanted promotional, phishing, or fraudulent message

        Input Message:
        {text}

        Classifier Prediction:
        {prediction['label']}

        Confidence:
        {prediction['confidence']}

        Evidence Agreement:
        {agreement}

        Top Retrieved Examples:
        {examples}

        Write 2-3 sentences explaining:
        1. Why the classifier predicted this label.
        2. Whether the retrieved examples support the prediction.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an explainable AI assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = llm(messages, max_new_tokens=120, do_sample=False)

    generated = response[0]["generated_text"]

    return generated[2]['content']