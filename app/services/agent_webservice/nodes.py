import os
from langchain_groq import ChatGroq
from app.services.agent_webservice.state import AgentState
from dotenv import load_dotenv
import asyncio

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key, temperature=0)

def load_prompt_template(filename: str) -> str:
    """Reads a prompt template from the templates directory."""
    # Getting the absolute path to the templates folder
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "templates", filename)
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

async def router_node(state: AgentState) -> dict:
    print("[Node: Router] Classifying intent with LLM...")
    
    # Load and format the prompt
    template = load_prompt_template("router.txt")
    prompt = template.format(user_input=state["input"])
    
    # AI Call
    response = await llm.ainvoke(prompt)
    route = response.content.lower().strip()
    
    return {"route": route}

async def respond_node(state: AgentState) -> dict:
    print(f"[Node: Respond] Generating response for route: {state['route']}...")
    
    # Load and format the prompt
    template = load_prompt_template("respond.txt")
    prompt = template.format(
        user_input=state["input"], 
        route=state["route"]
    )
    
    # AI Call
    response = await llm.ainvoke(prompt)
    
    return {"response": response.content}