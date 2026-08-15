import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SimilarBug(Base):
    __tablename__ = "similar_bugs"

    id = Column(Integer, primary_key=True, index=True)
    source_bug_id = Column(Integer, ForeignKey("bugs.id", ondelete="CASCADE"), nullable=False, index=True)
    similar_bug_id = Column(Integer, ForeignKey("bugs.id", ondelete="CASCADE"), nullable=False, index=True)
    similarity_score = Column(Float, nullable=False)  # 0.0 to 1.0 (Similarity ratio)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    source_bug = relationship("Bug", foreign_keys=[source_bug_id], back_populates="source_similarities")
    similar_bug = relationship("Bug", foreign_keys=[similar_bug_id], back_populates="target_similarities")
