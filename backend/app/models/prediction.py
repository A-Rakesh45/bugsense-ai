import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    bug_id = Column(Integer, ForeignKey("bugs.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    predicted_severity = Column(String(20), nullable=False)  # Critical, High, Medium, Low
    predicted_priority = Column(String(20), nullable=False)  # P1, P2, P3, P4
    predicted_category = Column(String(50), nullable=False)  # Functional, UI/UX, Performance, Security, etc.
    
    confidence = Column(Float, nullable=False, default=0.0)    # 0.0 to 1.0
    risk_score = Column(Float, nullable=False, default=0.0)    # 0.0 to 100.0
    risk_level = Column(String(20), nullable=False, default="Low") # Low, Medium, High, Critical
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    bug = relationship("Bug", back_populates="prediction")
    feedback = relationship("Feedback", back_populates="prediction", cascade="all, delete-orphan")
