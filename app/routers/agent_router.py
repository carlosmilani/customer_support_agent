# app/routers/agent_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent_webservice.workflow import run_workflow

router = APIRouter()

# Data schema for request validation
class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    HTTP endpoint for interacting with the support agent.
    The Router receives, validates, and forwards the message to the Service.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="The message cannot be empty.")

    try:
        # Asynchronous call to the Service (LangGraph Workflow)
        # While the Service awaits for AI , the Router remains free for other requests
        response_text = await run_workflow(request.message)
        
        return {
            "status": "success",
            "virtual_assistant": response_text
        }
    except Exception as e:
        # The Router converts internal failures into appropriate HTTP responses
        print(f"Internal Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")