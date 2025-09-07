# PragyanAI LLM Chatbot

A full-stack AI chatbot application built with React frontend and FastAPI backend, powered by Groq's LLM API. This project enables interactive real-time conversations with an AI assistant, storing chat history in a lightweight SQLite database.



## Features

- **Interactive Chat UI:** User-friendly React interface with message avatars, loading indicators, and chat history.
- **AI Powered Backend:** FastAPI server querying Groq’s LLM for intelligent responses.
- **Persistent Chat History:** SQLite database stores all question-and-answer pairs with timestamps.
- **Dark Mode Toggle:** Switch between light and dark themes for better user experience.
- **Feedback System:** Users can provide thumbs up/down feedback on AI responses.
- **Smooth Animations:** Animated chat bubbles enhance interactivity with Framer Motion.

---

## Technologies Used

- **Frontend:** React, Framer Motion, react-toggle-dark-mode
- **Backend:** FastAPI, Python, SQLite, requests
- **AI API:** Groq LLM API (meta-llama/llama-4-scout-17b-16e-instruct)
- **Styling:** Inline CSS / CSS Modules (customizable)

---

## Getting Started

### Prerequisites

- Node.js and npm installed for frontend
- Python 3.8+ installed for backend
- Groq API Key (sign up at [Groq](https://groq.com) to get your API key)

### Installation

#### Frontend

