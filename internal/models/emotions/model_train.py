import evaluate
import pandas as pd
import numpy as np
import torch
from pathlib import Path
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, Trainer, TrainingArguments

from internal.services.relevancy import build_collection_from_dataframe

curr_dir = Path.cwd()
model_dir = curr_dir/"emotion_model_v2"

print("Loading GoEmotions...")

df1 = pd.read_csv("./internal/models/emotions/goemotions_1.csv")
df2 = pd.read_csv("./internal/models/emotions/goemotions_2.csv")
df3 = pd.read_csv("./internal/models/emotions/goemotions_3.csv")

df = pd.concat([df1, df2, df3], ignore_index=True)

print("Original Size:", len(df))

emotion_cols = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
    "neutral",
]


df["emotion_count"] = df[emotion_cols].sum(axis=1)

df = df[df["emotion_count"] == 1].copy()

print("Single Label Size:", len(df))

df["emotion"] = df[emotion_cols].idxmax(axis=1)

# emotion_map = {
#     "joy": "joy",
#     "amusement": "joy",
#     "excitement": "joy",
#     "optimism": "joy",
#     "love": "love",
#     "caring": "love",
#     "gratitude": "love",
#     "admiration": "love",
#     "anger": "anger",
#     "annoyance": "anger",
#     "disapproval": "anger",
#     "disgust": "anger",
#     "sadness": "sadness",
#     "disappointment": "sadness",
#     "grief": "sadness",
#     "remorse": "sadness",
#     "fear": "fear",
#     "nervousness": "fear",
#     "surprise": "surprise",
#     "realization": "surprise",
#     "confusion": "surprise",

#     "neutral": "neutral"
# }
emotion_map = {

    "love": "love",
    "caring": "love",
    "joy": "joy",
    "amusement": "amusement",
    "excitement": "joy",
    "optimism": "optimism",
    "gratitude": "gratitude",
    "admiration": "admiration",
    "approval": "admiration",
    "anger": "anger",
    "annoyance": "anger",
    "sadness": "sadness",
    "disappointment": "sadness",
    "fear": "fear",
    "nervousness": "fear",
    "disapproval": "anger",
    "disgust": "disgust",
    "remorse": "remorse",
    "embarrassment": "embarrassment",
    "confusion": "confusion",
    "curiosity": "curiosity",
    "realization": "surprise",
    "surprise": "surprise",
    "neutral": "neutral",
    "grief": None,
    "pride": None,
    "relief": None,
    "desire": None,
}

df["emotion"] = df["emotion"].map(emotion_map)

df = df.dropna(subset=["emotion"])

print("\nEmotion Distribution:")
print(df["emotion"].value_counts())

unique_emotions = sorted(df["emotion"].unique())

label2id = {
    label: idx
    for idx, label in enumerate(unique_emotions)
}

id2label = {
    idx: label
    for label, idx in label2id.items()
}

df["labels"] = df["emotion"].map(label2id)

df = df[["text", "labels"]]
# build_collection_from_dataframe(df=df, collection_name="emotion7_relevancy",)
print("\nClasses:")
print(label2id)

print("\nNum Classes:", len(label2id))
print("Final Dataset Size:", len(df))

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["labels"],
    random_state=42,
)

dataset = DatasetDict(
    {
        "train": Dataset.from_pandas(train_df),
        "test": Dataset.from_pandas(test_df),
    }
)

print(dataset)


if model_dir.exists():
    print("Loading existing checkpoint...")
    tokenizer = AutoTokenizer.from_pretrained("./internal/models/emotions/emotion_model_v2")
    model = AutoModelForSequenceClassification.from_pretrained('./internal/models/emotions/emotion_model_v2')
else:
    print("Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(label2id), id2label=id2label, label2id=label2id)

model.config.id2label =  id2label
model.config.label2id = label2id

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=256,
    )

tokenized_datasets = dataset.map(tokenize,batched=True)
tokenized_datasets = tokenized_datasets.remove_columns(["text"])
tokenized_datasets.set_format("torch")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

metric_accuracy = evaluate.load("accuracy")
metric_f1 = evaluate.load("f1")
metric_precision = evaluate.load("precision")
metric_recall = evaluate.load("recall")

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(
        logits,
        axis=-1
    )

    accuracy = metric_accuracy.compute(
        predictions=predictions,
        references=labels,
    )

    weighted_f1 = metric_f1.compute(
        predictions=predictions,
        references=labels,
        average="weighted",
    )

    macro_f1 = metric_f1.compute(
        predictions=predictions,
        references=labels,
        average="macro",
    )

    precision = metric_precision.compute(
        predictions=predictions,
        references=labels,
        average="weighted",
    )

    recall = metric_recall.compute(
        predictions=predictions,
        references=labels,
        average="weighted",
    )

    return {
        "accuracy": accuracy["accuracy"],
        "weighted_f1": weighted_f1["f1"],
        "macro_f1": macro_f1["f1"],
        "precision": precision["precision"],
        "recall": recall["recall"],
    }


training_args = TrainingArguments(
    output_dir="./internal/models/emotions/emotion_model_v2",
    load_best_model_at_end=True,
    metric_for_best_model="macro_f1",
    greater_is_better=True,
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=3,
    weight_decay=0.01,
    warmup_steps=500,
    seed=42,
    eval_strategy="epoch",
    save_strategy="epoch",
    fp16=torch.cuda.is_available(),
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
results = trainer.evaluate()
print(results)

trainer.save_model("./internal/models/emotions/emotion_model_v2")
tokenizer.save_pretrained("./internal/models/emotions/emotion_model_v2")
print("Training Complete.")