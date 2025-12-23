from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.sql import func
from db.database import Base


class User(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    full_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)

    otp = Column(String(10), nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)

    is_otp_verified = Column(
        TINYINT(1),
        nullable=False,
        default=0
    )

    firebase_uid = Column(String(255), nullable=True)

    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    pincode = Column(String(20), nullable=True)

    image = Column(String(255), nullable=True)

    profile_approved = Column(
        String(50),
        nullable=False,
        default="pending"
    )

    last_active_at = Column(DateTime, nullable=True)

    fcm_token = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
