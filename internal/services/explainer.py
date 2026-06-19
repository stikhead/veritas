from functools import lru_cache

from transformers import pipeline
import torch

from internal.services.model_registry import MODEL_REGISTRY

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
@lru_cache(maxsize=1)
def get_llm():
    return pipeline(
        "text-generation",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        device_map="auto",
        dtype=torch.bfloat16
    )


def _generate(prompt: str):
    llm = get_llm()
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

    response = llm(
        messages,
        max_new_tokens=150,
        do_sample=False
    )

    generated = response[0]["generated_text"]

    if isinstance(generated, list):
        return generated[-1]["content"]

    return str(generated)


def generate_explanation(model_name, text, prediction,relevancy, agreement):


    if model_name == "emotion":

        prompt = f"""
            You are an explainable AI assistant.

            Input:
            {text}

            Sentiment Prediction:
            {prediction["sentiment"]["label"]}
            (confidence={prediction["sentiment"]["confidence"]})

            7-Class Emotion Prediction:
            {prediction["emotion_7"]["label"]}
            (confidence={prediction["emotion_7"]["confidence"]})

            16-Class Emotion Prediction:
            {prediction["emotion_16"]["label"]}
            (confidence={prediction["emotion_16"]["confidence"]})

            Agreement:
            Sentiment: {agreement["sentiment"]}
            Emotion7: {agreement["emotion_7"]}
            Emotion16: {agreement["emotion_16"]}

            Write a short explanation:

            1. Overall sentiment.
            2. Dominant emotion.
            3. How the fine-grained emotion relates to the broader emotion.
            4. Keep it factual and concise.
            """
        return _generate(prompt)

    examples = "\n".join(
        [
            f"[{m['label']}] {m['text']}"
            for m in relevancy["matches"][:3]
        ]
    )

    spec = MODEL_REGISTRY[model_name]

    label_text = ", ".join(spec.labels)

    prompt = f"""
        You are an explainable AI assistant.

        Use ONLY the information below.

        Do NOT infer identities.
        Do NOT invent context.

        Label Set:
        {label_text}

        Input Message:
        {text}

        Classifier Prediction:
        {prediction["label"]}

        Confidence:
        {prediction["confidence"]}

        Evidence Agreement:
        {agreement}

        Top Retrieved Examples:
        {examples}

        Write 2-3 sentences explaining:

        1. Why the classifier predicted this label.
        2. Whether the retrieved examples support the prediction.
        """

    return _generate(prompt)