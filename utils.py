import google.generativeai as genai
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure MongoDB
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'rag_pipeline')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'prompt_responses')

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    # Test the connection
    client.server_info()
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini Models
models = {
    "flash": genai.GenerativeModel('gemini-2.0-flash'),  # For Summarization & Flashcards
    "code": genai.GenerativeModel('models/gemini-2.0-flash-lite')  # For Code Review
}

# Fetch response from MongoDB
def get_response_from_mongo(prompt: str, task_type: str):
    """Fetch response from MongoDB"""
    try:
        result = collection.find_one({"prompt": prompt, "task_type": task_type})
        return result["response"] if result else None
    except Exception as e:
        print(f"Error fetching from MongoDB: {e}")
        return None

# Store prompt-response pair in MongoDB
def store_in_mongo(prompt: str, response: str, task_type: str):
    """Store prompt-response pair in MongoDB"""
    try:
        collection.insert_one({
            "prompt": prompt, 
            "response": response, 
            "task_type": task_type
        })
    except Exception as e:
        print(f"Error storing in MongoDB: {e}")
        raise

# Generate response using Gemini API
def generate_with_gemini(prompt: str, task_type: str):
    """Generate response using Gemini API"""
    model_key = "code" if task_type == "code_review" else "flash"
    
    try:
        # Add task-specific instructions to the prompt
        if task_type == "summarization":
            enhanced_prompt = f"Please provide a clear and concise summary of the following text:\n\n{prompt}"
        elif task_type == "flashcards":
            enhanced_prompt = f"Create flashcards in a Q&A format from the following text:\n\n{prompt}"
        elif task_type == "code_review":
            enhanced_prompt = f"Please review the following code and provide feedback on best practices, potential issues, and suggestions for improvement:\n\n{prompt}"
        else:
            enhanced_prompt = prompt

        response = models[model_key].generate_content(enhanced_prompt)
        return response.text
    except Exception as e:
        print(f"Failed to generate response with Gemini ({model_key}): {e}")
        raise ValueError(f"Failed to generate response with Gemini: {e}")
