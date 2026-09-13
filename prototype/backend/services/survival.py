from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Asset, Event


def calculate_intervention_survival(asset_id: int, db: Session):
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

            results.append({
                "intervention_date": intervention.event_date,
                "next_failure_date": next_failure.event_date,
                "survival_days": survival_days
            })

    return results
