# app/services/agent_webservice/workflow.py
from app.services.agent_webservice.state import AgentState
from app.services.agent_webservice.nodes import router_node, respond_node
from app.repositories.feedback_repo.repository import FeedbackRepository
from langgraph.graph import StateGraph, START, END

# --- Graph Definition ---
# Initializing the State Machine with the defined AgentState
graph = StateGraph(AgentState)

# Adding processing nodes
graph.add_node("router", router_node)
graph.add_node("respond", respond_node)

# Defining the execution flow
graph.add_edge(START, "router")
graph.add_edge("router", "respond")
graph.add_edge("respond", END)

# Compiling the graph into an executable app
app = graph.compile()

async def run_workflow(user_input: str):
    """
    Orchestrates the agent logic: 
    1. Runs the LangGraph workflow
    2. Persists the interaction in the database
    3. Returns the final response
    """
    initial_state = {
        "input": user_input, 
        "route": "", 
        "response": ""
    }

    print(f"--- [Service] Starting Agent processing... ---")
    
    # Executing the graph asynchronously
    final_state = await app.ainvoke(initial_state)

    # Persisting the final state via Repository (SQL Layer)
    await FeedbackRepository.save_interaction(final_state)
    
    return final_state["response"]