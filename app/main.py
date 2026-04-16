# app/main.py
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.agent_router import router as chat_router
from app.repositories.feedback_repo.repository import FeedbackRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP: Actions executed when the server starts ---
    print("--- [Startup] Initializing Database ---")
    await FeedbackRepository.init_db()
    
    yield # The server is running and handling requests
    
    # --- SHUTDOWN: Actions executed when the server stops ---
    print("--- [Shutdown] Closing resources if necessary ---")

# We updated the title and metadata for English standards
app = FastAPI(
    title="Customer Support Agent Onboarding", 
    lifespan=lifespan
)

# Including the router with a versioned prefix
app.include_router(chat_router, prefix="/v1")

if __name__ == "__main__":
    # Running uvicorn with hot-reload enabled for development
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)