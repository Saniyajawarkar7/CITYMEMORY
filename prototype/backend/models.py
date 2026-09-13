from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_code = Column(String, unique=True, nullable=False)
    asset_type = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    installation_date = Column(Date)
    condition = Column(String)
    importance = Column(String)
    events = relationship("Event", back_populates="asset", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    event_date = Column(Date, nullable=False)
    description = Column(String)
    outcome = Column(String)
    asset = relationship("Asset", back_populates="events")
