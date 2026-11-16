from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.memory.store import ConversationStore
from app.agent.graph import run_agent
from app.core.config import get_settings

router = APIRouter()
store = ConversationStore(get_settings().sqlite_path)

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    settings = get_settings()
    history = store.history(payload.user_id, payload.conversation_id, limit=16)
    try:
        answer, steps, tool_calls = run_agent(payload.message, history, settings.agent_max_steps)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    store.add(payload.user_id, payload.conversation_id, "user", payload.message)
    store.add(payload.user_id, payload.conversation_id, "assistant", answer)
    return ChatResponse(conversation_id=payload.conversation_id, answer=answer, steps=steps, tool_calls=tool_calls)

@router.get("/conversations/{conversation_id}")
def get_history(conversation_id: str, user_id: str = "demo-user"):
    return {"conversation_id":conversation_id, "messages":store.history(user_id, conversation_id, 100)}

@router.delete("/conversations/{conversation_id}")
def delete_history(conversation_id: str, user_id: str = "demo-user"):
    store.clear(user_id, conversation_id)
    return {"deleted":True, "conversation_id":conversation_id}
