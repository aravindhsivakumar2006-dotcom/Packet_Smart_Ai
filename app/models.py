from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime
from.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    budget = Column(Float)
    input_data = Column(Text)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)