from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=8000)
    conversation_id: str = Field(min_length=1, max_length=100)
    user_id: str = Field(default="demo-user", min_length=1, max_length=100)

class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    steps: list[str] = []
    tool_calls: int = 0
