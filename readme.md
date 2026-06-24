# Veritas

Veritas is an explainable AI text classification platform that combines transformer-based classifiers, semantic retrieval, and LLM-generated explanations.

The system provides:

* Spam Detection
* Sentiment Analysis
* 7-Class Emotion Classification
* 16-Class Fine-Grained Emotion Classification
* Retrieval-Augmented Evidence Validation
* Natural Language Explanations

The goal of Veritas is not only to predict labels but also to provide supporting evidence and transparent reasoning behind each prediction.

---

## Features

### Spam Detection

Classifies SMS and short-form messages as:

* Ham
* Spam

Uses:

* Fine-tuned BERT classifier
* Qdrant retrieval validation
* Evidence agreement scoring

---

### Sentiment Analysis

Classifies text as:

* Positive
* Negative

Uses:

* Fine-tuned multilingual BERT
* Semantic retrieval layer
* Confidence scoring

---

### Emotion Classification (7 Classes)

Predicts:

* Anger
* Fear
* Joy
* Love
* Sadness
* Surprise
* Neutral

Built using the GoEmotions dataset.

---

### Emotion Classification (16 Classes)

Predicts:

* Admiration
* Amusement
* Anger
* Confusion
* Curiosity
* Disgust
* Embarrassment
* Fear
* Gratitude
* Joy
* Love
* Neutral
* Optimism
* Remorse
* Sadness
* Surprise

Built using a lightly merged version of Google's GoEmotions dataset.

---

## Explainability Layer

Veritas combines:

### Classification

Transformer model prediction

### Retrieval

Semantic search against previously seen examples using:

* Sentence Transformers
* Qdrant Vector Database

### Agreement Scoring

Verifies whether retrieved evidence supports the model prediction.

### Natural Language Explanation

A Qwen-based explanation engine generates human-readable reasoning for predictions.

---

## Architecture

Client
↓
FastAPI
↓
Classifier Layer
* Spam Model
* Sentiment Model
* Emotion 7 Model
* Emotion 16 Model
↓
Retrieval Layer
* SentenceTransformer
* Qdrant Vector Database
↓
Explanation Layer
* Qwen 2.5 Instruct

---

## Tech Stack

### Backend

* FastAPI
* Pydantic

### Machine Learning

* Transformers
* PyTorch
* Sentence Transformers
* Scikit-learn
* Hugging Face Datasets

### Vector Search

* Qdrant

### Explainability

* Qwen 2.5 Instruct

---

## Live Demo / Testing

**Note:** Due to active hosting constraints, currently only the **Spam Detection** endpoint is publicly live for testing. The sentiment and emotion models are configured for local execution.

You can test the classification pipeline via `curl`:

```bash
curl -X POST "https://enemstic-vertias.hf.space/classify/spam" \
     -H "Content-Type: application/json" \
     -d '{"user_text": "YOUR_TEXT_HERE"}'
```

---

## API Endpoints

### List Models

GET

```http
/models
```

Returns all registered models.

---

### Classify

POST

```http
/classify/{model_name}
```

Example:

```json
{
  "text": "Congratulations! You have won a free prize."
}
```

Response:

```json
{
  "prediction": {
    "label": "spam",
    "confidence": 0.99
  },
  "relevancy": {
    "top_similarity": 0.81
  },
  "agreement": true
}
```

---

### Emotion Analysis

POST

```http
/emotion
```

Returns:

* Sentiment
* Emotion (7-Class)
* Emotion (16-Class)
* Retrieval Evidence
* Explanation

---

## Models

| Model      | Base Architecture       |
| ---------- | ----------------------- |
| Spam       | BERT Multilingual Cased |
| Sentiment  | BERT Multilingual Cased |
| Emotion 7  | BERT Multilingual Cased |
| Emotion 16 | BERT Multilingual Cased |

---

## Datasets

### Spam Detection

* SMS Spam Collection
* Adversarial Spam Dataset

### Sentiment Analysis

* IMDB Reviews Dataset

### Emotion Classification

* Google GoEmotions Dataset

---

## Future Improvements

* Docker Deployment
* GPU Inference Support
* Multi-Language Emotion Recognition
* User Feedback Loop
* Active Learning Pipeline
* Dashboard UI
* Authentication & Rate Limiting

---

## Motivation

Most text classification systems provide only a label and confidence score.

Veritas attempts to make predictions more transparent by combining:

* Classification
* Retrieval-based evidence
* Agreement verification
* Natural language explanations

This creates a more interpretable and trustworthy AI pipeline.

---

## License

MIT License