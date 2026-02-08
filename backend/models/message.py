from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str = Field(min_length=1)


class Message(MessageBase, table=True):
    __tablename__ = "message"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
