from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Literal, Optional


class AssetCreate(BaseModel):
    asset_code: str = Field(min_length=2, max_length=50)
    asset_type: str = Field(min_length=2, max_length=50)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    condition: Literal["Good", "Fair", "Poor"]
    importance: Literal["Low", "Medium", "High"]


class EventCreate(BaseModel):
    asset_id: int
    event_type: Literal["Failure", "Intervention"]
    event_date: date
    description: str
    outcome: Optional[str] = ""


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_code: str
    asset_type: str
    latitude: Optional[float]
    longitude: Optional[float]
    installation_date: Optional[date]
    condition: Optional[str]
    importance: Optional[str]


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    event_type: str
    event_date: date
    description: Optional[str]
    outcome: Optional[str]
