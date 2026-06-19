import pandas as pd
import evaluate
from sklearn.model_selection import train_test_split
from torch.optim import AdamW
from torch.utils.data import DataLoader
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, TrainingArguments, Trainer
import numpy as np
from pathlib import Path
import torch

# from internal.services.relevancy import build_collection_from_dataframe
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Version:", torch.version.cuda)
print("Device Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")

curr_dir = Path.cwd()
model_dir = "./internal/models/sms_spam/sms_spam_model"

# ==========================
# ORIGINAL DATASET
# ==========================

org_df = pd.read_csv("./internal/models/sms_spam/spam.csv",encoding="utf-8-sig")
org_df = org_df[["v1", "v2"]]
org_df = org_df.rename(
    columns={
        "v1": "labels",
        "v2": "text"
    }
)

org_df["labels"] = org_df["labels"].map(
    {
        "ham": 0,
        "spam": 1
    }
)

# ==========================
# ADVERSARIAL DATASET
# ==========================

adversarial_df = pd.read_csv("./internal/models/sms_spam/refined_adversarial_dataset.csv")

adversarial_df = adversarial_df.rename(
    columns={
        "label": "labels"
    }
)


adversarial_df["labels"] = (
    adversarial_df["labels"]
    .astype(int)
)

# ==========================
# COMBINE
# ==========================

df = pd.concat(
    [org_df, adversarial_df],
    ignore_index=True
)

df = df.dropna(subset=["text"])

df = df.drop_duplicates(
    subset=["text"]
)

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

print(df.head())

print("\nClass Distribution:")
print(df["labels"].value_counts())

print("\nRandom Samples:")
print(df.sample(20)["text"].tolist())

# build_collection_from_dataframe(df=df, collection_name="sms_relevancy",)
# df = pd.read_csv("spam.csv", encoding="utf-8-sig")
# df = df[["v1", "v2"]]
# df = df.rename(columns={"v1": "labels", "v2": "text"})
# df['labels'] = df['labels'].map({"ham": 0, "spam": 1})
# df = df.drop_duplicates(subset=["text"])
# df = df.sample(frac=1, random_state=42).reset_index(drop=True)
# print(df.head())
# print(df.sample(20)["text"].tolist())
# print(df["labels"].value_counts())
# print(df["text"].dtype)
# print(df["text"].isna().sum())
# bad_rows = df[~df["text"].apply(lambda x: isinstance(x, str))]
# print(bad_rows.head(20))
df = df.dropna(subset=["text"])
print(df["text"].isna().sum())

dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2)

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["labels"],
    random_state=42
)

dataset = DatasetDict({
    "train": Dataset.from_pandas(train_df),
    "test": Dataset.from_pandas(test_df)
})

if Path(model_dir).exists():
    print("using existing model..........")
    tokenizer = AutoTokenizer.from_pretrained("./internal/models/sms_spam/sms_spam_model")
    model = AutoModelForSequenceClassification.from_pretrained("./internal/models/sms_spam/sms_spam_model", num_labels=2)
else: 
    tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)
def tokenize(example):
    return tokenizer(
        example['text'],
        truncation=True
    )

tokenized_datasets = dataset.map(tokenize, batched=True)

# print(tokenized_dataset)

tokenized_datasets = tokenized_datasets.remove_columns(['text'])
tokenized_datasets.set_format("torch")
print(tokenized_datasets)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
# train_collator = DataLoader(tokenized_datasets, batch_size=2, shuffle=True, collate_fn=data_collator)

metric_accuracy = evaluate.load("accuracy")
metric_f1 = evaluate.load("f1")
metric_precision = evaluate.load("precision")
metric_recall = evaluate.load("recall")
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = metric_accuracy.compute(predictions=predictions, references=labels)
    f1 = metric_f1.compute(predictions=predictions, references=labels)
    precision = metric_precision.compute(predictions=predictions, references=labels)

    recall = metric_recall.compute(predictions=predictions,references=labels)

    return {
        "accuracy": accuracy["accuracy"],
        "f1": f1["f1"],
        "precision": precision["precision"],
        "recall": recall["recall"]
    }


training_args = TrainingArguments(
    output_dir="./sms_spam_model_v2",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    greater_is_better=True,
    learning_rate=1e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=1, 
    weight_decay=0.01,
    seed=42,
    eval_strategy="epoch", 
    save_strategy="epoch",
    fp16=torch.cuda.is_available()
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    compute_metrics=compute_metrics,
    data_collator=data_collator
)

trainer.train()
results = trainer.evaluate()
print(results)
trainer.save_model("./sms_spam_model_v2")
tokenizer.save_pretrained("./sms_spam_model_v2")