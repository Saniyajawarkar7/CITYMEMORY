from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Asset, Event


def detect_failure_signature(asset_id: int, db: Session):

    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    failures = db.query(Event).filter(
        Event.asset_id == asset_id,
        Event.event_type == "Failure"
    ).order_by(Event.event_date).all()

    if not failures:
        return {"asset": asset.asset_code, "failure_count": 0, "patterns": []}

    rainfall_related = 0
    overflow_related = 0
    blockage_related = 0

    for failure in failures:

        description = (failure.description or "").lower()

        if "rain" in description:
            rainfall_related += 1

        if "overflow" in description:
            overflow_related += 1

        if "block" in description:
            blockage_related += 1

    patterns = []

    if rainfall_related > 0:
        patterns.append({
            "factor": "Heavy rainfall",
            "failure_occurrences": rainfall_related,
            "interpretation": "Potential contributing pattern"
        })

    if overflow_related > 0:
        patterns.append({
            "factor": "Water overflow",
            "failure_occurrences": overflow_related,
            "interpretation": "Potential contributing pattern"
        })

    if blockage_related > 0:
        patterns.append({
            "factor": "Blockage",
            "failure_occurrences": blockage_related,
            "interpretation": "Potential contributing pattern"
        })

    return {
        "asset": asset.asset_code,
        "failure_count": len(failures),
        "patterns": patterns
    }
