from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from services.survival import calculate_intervention_survival
from database import get_db
from models import Asset, Event
from services.amnesia import detect_amnesia
from services.echo import detect_failure_echo
from services.signature import detect_failure_signature
from services.comparison import compare_interventions
from services.planner import calculate_priority
from schemas import EventCreate, EventRead

router = APIRouter(
    prefix="/events",
    tags=["Infrastructure History"]
)


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == event.asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    new_event = Event(
        asset_id=event.asset_id,
        event_type=event.event_type,
        event_date=event.event_date,
        description=event.description,
        outcome=event.outcome
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get("/survival/{asset_id}")
def get_intervention_survival(
    asset_id: int,
    db: Session = Depends(get_db)
):
    return calculate_intervention_survival(asset_id, db)


@router.get("/amnesia/{asset_id}")
def get_amnesia(
    asset_id: int,
    db: Session = Depends(get_db)
):
    return detect_amnesia(asset_id, db)
@router.get("/echo/{asset_id}")
def get_failure_echo(
    asset_id: int,
    db: Session = Depends(get_db)
):
    return detect_failure_echo(asset_id, db)
@router.get("/signature/{asset_id}")
def get_failure_signature(
    asset_id: int,
    db: Session = Depends(get_db)
):
    return detect_failure_signature(asset_id, db)
@router.get("/comparison/{asset_id}")
def get_intervention_comparison(
    asset_id: int,
    db: Session = Depends(get_db)
):
    return compare_interventions(asset_id, db)
@router.get("/planner/{asset_id}")
def get_preventive_plan(
    asset_id: int,
    db: Session = Depends(get_db)
):
    return calculate_priority(asset_id, db)
@router.get("/{asset_id}")
def get_asset_history(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        return {"message": "Asset not found"}

    events = db.query(Event).filter(
        Event.asset_id == asset_id
    ).order_by(Event.event_date).all()

    return {
        "asset": asset.asset_code,
        "asset_type": asset.asset_type,
        "condition": asset.condition,
        "importance": asset.importance,
        "history": events
    }

