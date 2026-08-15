import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="Tester", nullable=False)  # Admin, Tester, Developer
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    bugs_created = relationship("Bug", back_populates="created_by", cascade="all, delete-orphan")
    feedback_provided = relationship("Feedback", back_populates="corrected_by", cascade="all, delete-orphan")
