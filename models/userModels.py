from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db.database import Base


class User(Base):
    __tablename__ = "customers"   # apne table ka naam yaha dalna hai

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    pincode = Column(String(20), nullable=True)
    image = Column(String(255), nullable=True)
    profile_approved = Column(String(255), default="pending", nullable=True)
    last_active_at = Column(DateTime, nullable=True)
    fcm_Token = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, full_name={self.full_name})>"
