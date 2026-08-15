import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    steps_to_reproduce = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True)
    actual_result = Column(Text, nullable=True)
    environment = Column(String(100), default="Production", nullable=False)
    app_version = Column(String(50), default="v1.0.0", nullable=False)
    browser_device = Column(String(100), default="Chrome 120 / Windows 11", nullable=False)
    module = Column(String(100), default="General", nullable=False, index=True)
    status = Column(String(20), default="Open", nullable=False, index=True)  # Open, In Progress, Resolved, Closed
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    created_by = relationship("User", back_populates="bugs_created")
    prediction = relationship("Prediction", back_populates="bug", uselist=False, cascade="all, delete-orphan")
    
    source_similarities = relationship(
        "SimilarBug",
        foreign_keys="SimilarBug.source_bug_id",
        back_populates="source_bug",
        cascade="all, delete-orphan"
    )
    target_similarities = relationship(
        "SimilarBug",
        foreign_keys="SimilarBug.similar_bug_id",
        back_populates="similar_bug",
        cascade="all, delete-orphan"
    )
