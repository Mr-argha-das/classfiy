from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from db.database import Base  # SQLAlchemy Base


class Message(Base):
    __tablename__ = "messages_table"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(Integer, ForeignKey("customers.id"))   # matches Laravel customers.id
    receiver_id = Column(Integer, ForeignKey("customers.id")) # matches Laravel customers.id
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user1_id = Column(Integer, ForeignKey("customers.id"))   # matches Laravel customers.id
    user2_id = Column(Integer, ForeignKey("customers.id"))   # matches Laravel customers.id
    last_message_id = Column(String(36), ForeignKey("messages_table.id"))

    last_message = relationship("Message", foreign_keys=[last_message_id])
