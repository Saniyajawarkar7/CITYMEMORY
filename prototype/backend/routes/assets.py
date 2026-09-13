from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Asset
from schemas import AssetCreate, AssetRead

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    new_asset = Asset(
        asset_code=asset.asset_code,
        asset_type=asset.asset_type,
        latitude=asset.latitude,
        longitude=asset.longitude,
        condition=asset.condition,
        importance=asset.importance
    )

    db.add(new_asset)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An asset with this code already exists")
    db.refresh(new_asset)

    return new_asset


@router.get("/", response_model=list[AssetRead])
def get_assets(db: Session = Depends(get_db)):
    return db.query(Asset).order_by(Asset.asset_code).all()
