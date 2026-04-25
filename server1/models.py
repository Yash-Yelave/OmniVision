import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./omnivision.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Pothole(Base):
    __tablename__ = "potholes"
    
    pothole_id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    confidence = Column(Float)
    image_path = Column(String)
    detected_time = Column(DateTime, default=datetime.utcnow)
    severity_level = Column(String)

class UserLocation(Base):
    __tablename__ = "user_locations"
    
    location_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    
    alert_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    pothole_id = Column(Integer, ForeignKey("potholes.pothole_id"), index=True)
    distance_meters = Column(Float)
    alert_message = Column(String)
    video_url = Column(String, nullable=True)
    alert_time = Column(DateTime, default=datetime.utcnow)

# Ensure tables are created (use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
