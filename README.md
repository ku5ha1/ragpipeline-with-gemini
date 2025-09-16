# Gemini RAG Pipeline

A minimal RAG (Retrieval-Augmented Generation) backend using Google Gemini, FAISS, and MongoDB.

## Features

- Summarization
- Flashcard Generation
- Code Review
- Caching with FAISS & MongoDB
- Markdown-formatted responses

## Setup

virtual env creation:  python -m venv venv

activate virtual env:  venv/bin/activate
install requirements: pip install -r requirements.txt
```

Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_uri
```

Run the app:

```
uvicorn main:app --reload
```

## API

- `GET /` — API info
- `POST /summarize`
- `POST /generate_flashcards`
- `POST /code_review`

All POST endpoints accept:
```json
{ "prompt": "Your text here" }
```