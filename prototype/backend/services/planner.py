from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Asset, Event


def calculate_priority(asset_id: int, db: Session):

    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    failures = db.query(Event).filter(
        Event.asset_id == asset_id,
        Event.event_type == "Failure"
    ).count()

    interventions = db.query(Event).filter(
        Event.asset_id == asset_id,
        Event.event_type == "Intervention"
    ).count()

    score = 0

    # Recurrence
    if failures >= 3:
        score += 40
    elif failures == 2:
        score += 25
    elif failures == 1:
        score += 10

    # Intervention history
    if interventions >= 2:
        score += 20
    elif interventions == 1:
        score += 10

    # Asset importance
    if asset.importance and asset.importance.lower() == "high":
        score += 25
    elif asset.importance and asset.importance.lower() == "medium":
        score += 15

    # Current condition
    if asset.condition and asset.condition.lower() == "poor":
        score += 15
    elif asset.condition and asset.condition.lower() == "fair":
        score += 8

    if score >= 70:
        priority = "High"
        recommended_action = "Prioritize preventive intervention"
    elif score >= 40:
        priority = "Medium"
        recommended_action = "Schedule preventive inspection"
    else:
        priority = "Low"
        recommended_action = "Continue monitoring"

    return {
        "asset": asset.asset_code,
        "asset_type": asset.asset_type,
        "failure_count": failures,
        "intervention_count": interventions,
        "importance": asset.importance,
        "condition": asset.condition,
        "priority_score": score,
        "priority": priority,
        "recommended_action": recommended_action
    }
