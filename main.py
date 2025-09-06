import os
import sqlite3
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Configuration ---
DB_FILE = "qna.db"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY environment variable not set!")

# --- Database Setup ---
def setup_database():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS qna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_qa(question: str, answer: str):
    """Logs a question and its answer to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO qna (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging to database: {e}")

# --- FastAPI App Initialization ---
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Run database setup on application startup."""
    setup_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

# --- Groq LLM Helper ---
def query_groq_llm(question: str) -> str:
    """Sends a question to the Groq API and returns the answer."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct", # Using the same model as before for consistency
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        "temperature": 0.5,
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error calling Groq API: {e}")
        raise HTTPException(status_code=500, detail=f"Error communicating with Groq API: {e}")


# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Groq Chatbot is Running!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Receives a prompt, gets a completion from Groq, logs the interaction,
    and returns the response.
    """
    answer = query_groq_llm(request.prompt)
    log_qa(request.prompt, answer)
    return {"response": answer}

@app.get("/history")
async def history():
    """Retrieves the last 50 Q&A pairs from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        # Fetch the most recent 50 entries
        cur.execute("SELECT question, answer, timestamp FROM qna ORDER BY id DESC LIMIT 50")
        rows = cur.fetchall()
        conn.close()
        return [{"question": q, "answer": a, "timestamp": t} for q, a, t in rows]
    except Exception as e:
        print(f"Error fetching history from database: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve chat history.")
