# app/services/agent_webservice/nodes.py
import asyncio
from app.services.agent_webservice.state import AgentState

# Simulating the function used to load prompt templates from files
def load_prompt_template(name: str) -> str:
    """
    In a production environment, this would read from the templates folder:
    with open(f"app/services/agent_webservice/templates/{name}.txt", "r") as f:
        return f.read()
    """
    return "You are an assistant. The customer said: {user_input}. Route: {route}."

async def router_node(state: AgentState) -> dict:
    """
    Classifies the user's intent based on keywords.
    In a real scenario, this would be a call to an LLM.
    """
    print("[Node: Router] Classifying intent...")
    await asyncio.sleep(0.5) # Simulating network latency with AI API
    
    text = state["input"].lower()
    
    # Intent classification logic
    if "buy" in text or "price" in text or "purchase" in text:
        return {"route": "purchase"}
    elif "delivery" in text or "track" in text or "shipping" in text:
        return {"route": "delivery"}
    elif "rate" in text or "feedback" in text or "score" in text:
        return {"route": "rate"}
    
    return {"route": "unknown"}

async def respond_node(state: AgentState) -> dict:
    """
    Generates a response based on the identified route.
    """
    route = state["route"]
    print(f"[Node: Respond] Generating response for route: {route}...")
    await asyncio.sleep(1.0) # Simulating LLM text generation
    
    # Simulated standard responses
    if route == "purchase":
        # In a real case, the LLM would extract the specific product from the text
        response = "We have Product X in stock for only $99.90. Would you like to place an order?"
    elif route == "delivery":
        response = "I checked your order: it is on its way and will arrive tomorrow by 6 PM!"
    elif route == "rate":
        response = "We appreciate your feedback! What rating (0 to 10) would you give the product?"
    else:
        response = "I'm sorry, I couldn't understand your request. Could you please rephrase it?"
        
    return {"response": response}