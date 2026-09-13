from sqlalchemy.orm import Session

from fastapi import HTTPException
from models import Asset, Event


def detect_amnesia(asset_id: int, db: Session):
    if not db.get(Asset, asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")
    interventions = db.query(Event).filter(
        Event.asset_id == asset_id,
        Event.event_type == "Intervention"
    ).order_by(Event.event_date).all()

    results = []

    for intervention in interventions:

        next_failure = db.query(Event).filter(
            Event.asset_id == asset_id,
            Event.event_type == "Failure",
            Event.event_date > intervention.event_date
        ).order_by(Event.event_date).first()

        if next_failure:
            survival_days = (
                next_failure.event_date - intervention.event_date
            ).days

            if survival_days < 90:
                results.append({
                    "intervention_date": intervention.event_date,
                    "failure_date": next_failure.event_date,
                    "survival_days": survival_days,
                    "amnesia_flag": True,
                    "reason": "Intervention was followed by failure within 90 days"
                })

    return results
