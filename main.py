import os
import sqlite3
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Replace with your deployed frontend URL (Netlify)
FRONTEND_URL = "relaxed-macaron-0ceca5.netlify.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "qna.db"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY environment variable not set!")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS qna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class QARequest(BaseModel):
    question: str

def query_groq_llm(question: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        "temperature": 0.5,
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def log_qa(question, answer):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO qna (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

@app.post("/ask")
async def ask(request: QARequest):
    answer = query_groq_llm(request.question)
    log_qa(request.question, answer)
    return {"answer": answer}

@app.get("/history")
async def history():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT question, answer, timestamp FROM qna ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return [{"question": q, "answer": a, "timestamp": t} for q, a, t in rows]
