from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Asset, Event


def detect_failure_echo(
    asset_id: int,
    db: Session,
    distance_threshold: float = 0.02,
    time_window_days: int = 30
):
    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    target_failures = db.query(Event).filter(
        Event.asset_id == asset_id,
        Event.event_type == "Failure"
    ).all()

    results = []
    other_failures = db.query(Event).filter(
        Event.event_type == "Failure", Event.asset_id != asset_id
    ).all()

    for failure in target_failures:

        for other_failure in other_failures:

            other_asset = db.query(Asset).filter(
                Asset.id == other_failure.asset_id
            ).first()

            if not other_asset:
                continue

            if asset.latitude is None or asset.longitude is None:
                continue

            if other_asset.latitude is None or other_asset.longitude is None:
                continue

            distance = (
                (asset.latitude - other_asset.latitude) ** 2
                + (asset.longitude - other_asset.longitude) ** 2
            ) ** 0.5

            time_difference = abs(
                (failure.event_date - other_failure.event_date).days
            )

            if (
                distance <= distance_threshold
                and time_difference <= time_window_days
            ):
                results.append({
                    "asset": asset.asset_code,
                    "related_asset": other_asset.asset_code,
                    "failure_date": failure.event_date,
                    "related_failure_date": other_failure.event_date,
                    "spatial_distance": round(distance, 4),
                    "time_difference_days": time_difference,
                    "echo_detected": True,
                    "interpretation": (
                        "Failures repeatedly occurred within the "
                        "same spatial-temporal window"
                    )
                })

    return results
