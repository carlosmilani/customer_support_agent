# AI Customer Support Agent (Onboarding)

An asynchronous AI Agent built with **FastAPI**, **LangGraph**, and **SQLite**. The agent classifies customer intents and generates empathetic responses using LLMs (Groq/Llama 3.1).

## 🛠️ Tech Stack
- **Framework:** FastAPI
- **Orchestration:** LangGraph (State Machine)
- **LLM:** Groq (Llama 3.1 8b Instant)
- **Database:** SQLite (aiosqlite)
- **Package Manager:** uv

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/carlosmilani/customer_support_agent
   cd customer_support_agent
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Activate the Virtual Environment:**

   **On Windows (PowerShell):**
   ```bash
   .venv\Scripts\activate
   ```

   **On Linux / macOS:**
   ```bash
   source .venv/bin/activate
   ```

4. **Configure environment:**
- Create a `.env` file based on `.env.example`.
- Add your `GROQ_API_KEY`.

5. **Start the server**
   ```bash
   python -m app.main
   ```

## Testing with CURL

**Purchase intent:**
   ```bash
   curl -X POST "http://localhost:8000/v1/chat" -H "Content-Type: application/json" -d "{\"message\": \"I want to buy a laptop\"}"
   ```

**Delivery intent:**
   ```bash
   curl -X POST "http://localhost:8000/v1/chat" -H "Content-Type: application/json" -d "{\"message\": \"Where is my order?\"}"
   ```

**Feedback intent:**
   ```bash
   curl -X POST "http://localhost:8000/v1/chat" -H "Content-Type: application/json" -d "{\"message\": \"I want to rate the product\"}"
   ```