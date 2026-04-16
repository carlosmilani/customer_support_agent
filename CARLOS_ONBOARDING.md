# Intern Onboarding: Agent Service

## 1. Git

PR-based workflow with rebasing (no merge commits).

```bash
# Feature branch
git checkout -b feature/my-feature
git commit -m "Add product extraction endpoint"

# Keep up to date
git fetch origin
git rebase origin/main

# Clean up before PR
git rebase -i HEAD~3  # squash/reword

# Push
git push --force-with-lease
```

**Practice:** [learngitbranching.js.org](https://learngitbranching.js.org/)

---

## 2. Python Async

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)  # non-blocking
    return {"data": "value"}

async def main():
    results = await asyncio.gather(
        fetch_data(),
        fetch_data(),
    )
    print(results)

asyncio.run(main())
```

**Key concepts:**
- Process vs thread vs coroutine/EventLoop
- `async def` declares a coroutine
- `await` pauses without blocking other tasks
- `asyncio.gather()` runs concurrently

**Read:** Fluent Python (async chapter)

---

## 3. Architecture

3-layer separation: Routers → Services → Repositories

```
POST /extract
     │
     ▼
┌─────────────────────────────────────┐
│  Router                             │
│  - HTTP validation only             │
│  - Convert exceptions to HTTP       │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  Service                            │
│  - Business logic                   │
│  - LLM calls, prompt rendering      │
│  - No HTTP concepts, no raw SQL     │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  Repository                         │
│  - SQL only                         │
│  - No business logic                │
└─────────────────────────────────────┘
```

**Read:** [docs/ARCHITECTURE.md](ARCHITECTURE.md) and `CLAUDE.md`

---

## 4. LangGraph

State machine for multi-step agent workflows.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    route: str
    response: str

async def router_node(state: AgentState) -> dict:
    route = await classify_intent(state["input"])
    return {"route": route}

async def respond_node(state: AgentState) -> dict:
    response = await generate_response(state["input"], state["route"])
    return {"response": response}

graph = StateGraph(AgentState)
graph.add_node("router", router_node)
graph.add_node("respond", respond_node)

graph.add_edge(START, "router")
graph.add_edge("router", "respond")
graph.add_edge("respond", END)

app = graph.compile()
result = await app.ainvoke({"input": "Tell me about motors"})
```

**Study our agent:**
1. `app/services/agent-webservice/graph.py` — workflow
2. `app/services/agent-webservice/nodes.py` — node implementations
3. `app/services/agent-webservice/templates/` — prompts

**Read:** [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
