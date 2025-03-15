# Gemini RAG Pipeline

A FastAPI-based RAG (Retrieval-Augmented Generation) pipeline that uses Google's Gemini AI model for various text processing tasks. The system includes caching mechanisms using FAISS for similarity search and MongoDB for storage.

## Features

- **Text Summarization**: Generate concise summaries of input text
- **Flashcard Generation**: Create study flashcards from educational content
- **Code Review**: Get AI-powered code review suggestions
- **Caching System**: Efficient response caching using FAISS and MongoDB
- **Markdown Response**: All responses are formatted in Markdown for better readability

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini
- **Vector Database**: FAISS
- **Document Store**: MongoDB
- **Frontend Port**: 5173 (Vite)
- **Backend Port**: 8000

## Setup

1. Clone the repository
```bash
git clone [your-repo-url]
cd [your-repo-name]
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_uri
```

5. Run the application
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

- `GET /`: Root endpoint, returns basic API information
- `POST /summarize`: Generate text summaries
- `POST /generate_flashcards`: Create study flashcards
- `POST /code_review`: Get code review suggestions

All POST endpoints accept a JSON body with a `prompt` field:
```json
{
    "prompt": "Your text here"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 