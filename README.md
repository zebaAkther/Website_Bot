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
cd frontend
npm install
npm start


#### Backend

cd backend
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_api_key_here" # Or set in your environment variables
uvicorn main:app --reload




---

## Usage

- Open the frontend React app in your browser.
- Type your questions in the chat input box.
- AI responses will appear in real time.
- Dark mode toggle is available in the header.
- Provide feedback on AI answers with thumbs up/down.

---

## Environment Variables

- `GROQ_API_KEY` — Your API key to access the Groq LLM service.  
  Make sure to keep it secret and do not expose it in public repositories.

---

## Deployment

You can deploy the frontend and backend separately:

- Frontend on platforms like Netlify, Vercel, or Render static hosting.
- Backend on Render, Heroku, AWS, or other cloud servers supporting Python FastAPI.

Configure environment variables and update the API URLs in frontend accordingly.

---

## Contributing

Contributions welcome! Please open issues or pull requests on GitHub.

---

## License

This project is licensed under the MIT License.

---




