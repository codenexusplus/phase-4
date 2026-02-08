from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)  # Using string for user_id as it could be UUID


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversation"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
