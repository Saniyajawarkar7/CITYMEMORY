from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Asset, Event


def compare_interventions(asset_id: int, db: Session):
    if not db.get(Asset, asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")

    interventions = db.query(Event).filter(
        Event.asset_id == asset_id,
        Event.event_type == "Intervention"
    ).order_by(Event.event_date).all()

    if not interventions:
        return {"asset_id": asset_id, "interventions_compared": 0, "historical_results": [], "historically_better_intervention": None}

    results = []

    for intervention in interventions:

        next_failure = db.query(Event).filter(
            Event.asset_id == asset_id,
            Event.event_type == "Failure",
            Event.event_date > intervention.event_date
        ).order_by(Event.event_date).first()

        if next_failure:
            survival_days = (
                next_failure.event_date -
                intervention.event_date
            ).days

            results.append({
                "intervention_date": intervention.event_date,
                "intervention": intervention.description,
                "survival_days": survival_days
            })

    if not results:
        return {"asset_id": asset_id, "interventions_compared": 0, "historical_results": [], "historically_better_intervention": None}

    best_intervention = max(
        results,
        key=lambda x: x["survival_days"]
    )

    return {
        "asset_id": asset_id,
        "interventions_compared": len(results),
        "historical_results": results,
        "historically_better_intervention": best_intervention,
        "interpretation": (
            "Historical evidence favors the intervention "
            "with the longest recurrence-free survival."
        )
    }
