from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from models import generate_embedding, search_in_faiss, add_to_faiss
from utils import get_response_from_mongo, store_in_mongo, generate_with_gemini, collection
import markdown

# Define request model
class PromptRequest(BaseModel):
    prompt: str

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def get_root():
    return {'message': 'RAG Pipeline with AI Features'}

# Common function to handle RAG retrieval + AI generation
async def process_request(request: PromptRequest, task_type: str):
    try:
        # Step 1: Generate embedding for the query
        prompt_embedding = generate_embedding(request.prompt)

        # Step 2: Search for similar embeddings in FAISS
        distances, indices = search_in_faiss(prompt_embedding, k=1)

        # Step 3: Check similarity threshold (If found, return cached response)
        if distances[0][0] < 0.5:
            cached_response = get_response_from_mongo(request.prompt, task_type)
            if cached_response:
                markdown_response = f"## Cached Response\n\n**Prompt:** {request.prompt}\n\n**Task:** {task_type}\n\n**Response:**\n\n{cached_response}"
                return HTMLResponse(content=markdown.markdown(markdown_response))

        # Step 4: If no match, generate response using Gemini
        ai_generated_response = generate_with_gemini(request.prompt, task_type)

        # Step 5: Store response in MongoDB & FAISS
        store_in_mongo(request.prompt, ai_generated_response, task_type)
        add_to_faiss(prompt_embedding, request.prompt, task_type, ai_generated_response)

        markdown_response = f"## AI-Generated Response\n\n**Prompt:** {request.prompt}\n\n**Task:** {task_type}\n\n**Response:**\n\n{ai_generated_response}"
        return HTMLResponse(content=markdown.markdown(markdown_response))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Summarization Endpoint
@app.post("/summarize", response_class=HTMLResponse)
async def summarize(request: PromptRequest):
    return await process_request(request, "summarization")

# Flashcard Generation Endpoint
@app.post("/generate_flashcards", response_class=HTMLResponse)
async def generate_flashcards(request: PromptRequest):
    return await process_request(request, "flashcards")

# Code Review Endpoint
@app.post("/code_review", response_class=HTMLResponse)
async def code_review(request: PromptRequest):
    return await process_request(request, "code_review")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
