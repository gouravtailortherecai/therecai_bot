from sqlalchemy import Column, Integer, BigInteger, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    username = Column(Text)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
