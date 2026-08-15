import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    
    corrected_severity = Column(String(20), nullable=True)
    corrected_priority = Column(String(20), nullable=True)
    corrected_category = Column(String(50), nullable=True)
    
    corrected_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_version = Column(String(50), default="v1.0", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    prediction = relationship("Prediction", back_populates="feedback")
    corrected_by = relationship("User", back_populates="feedback_provided")
