"""
CITYMEMORY demo data seeder (v2 - matches exact event_type values your
services expect: "Failure" and "Intervention"). Run once from backend/.
 
Usage:
    python seed.py
"""
 
from datetime import date
from database import SessionLocal, engine, Base
from models import Asset, Event
 
Base.metadata.create_all(bind=engine)
 
db = SessionLocal()
 
db.query(Event).delete()
db.query(Asset).delete()
db.commit()
 
# ---------------------------------------------------------------------------
# ASSETS
# ---------------------------------------------------------------------------
assets_data = [
    dict(asset_code="RD-001", asset_type="Road", latitude=21.1458, longitude=79.0882,
         condition="Poor", importance="High"),
    dict(asset_code="RD-002", asset_type="Road", latitude=21.1500, longitude=79.0950,
         condition="Fair", importance="Medium"),
    dict(asset_code="PIPE-001", asset_type="Water Pipeline", latitude=21.1400, longitude=79.0800,
         condition="Poor", importance="High"),
    dict(asset_code="PIPE-002", asset_type="Water Pipeline", latitude=21.1470, longitude=79.0700,
         condition="Fair", importance="Medium"),
    dict(asset_code="LGT-001", asset_type="Streetlight", latitude=21.1550, longitude=79.0850,
         condition="Good", importance="Low"),
    dict(asset_code="XFR-001", asset_type="Transformer", latitude=21.1420, longitude=79.1000,
         condition="Poor", importance="High"),
    dict(asset_code="RD-003", asset_type="Road", latitude=21.1600, longitude=79.0750,
         condition="Fair", importance="Medium"),
]
 
asset_objs = {}
for data in assets_data:
    a = Asset(installation_date=date(2018, 1, 1), **data)
    db.add(a)
    db.commit()
    db.refresh(a)
    asset_objs[data["asset_code"]] = a
 
print(f"Created {len(asset_objs)} assets.")
 
# ---------------------------------------------------------------------------
# EVENTS
# event_type is ALWAYS "Failure" or "Intervention" (services filter on this
# exact string). Descriptions carry the real-world detail, and some mention
# "rain" / "overflow" / "block" so the Signature detector finds patterns.
#
# RD-001: pothole fails 3 times, each "repair" (Intervention) survives <90
#         days before failing again -> triggers Amnesia + low survival.
# PIPE-001: leak recurs, mostly rain-related -> Signature pattern.
# XFR-001: overload failures with short-lived fixes -> Amnesia + Planner high.
# ---------------------------------------------------------------------------
events_data = [
    # RD-001 — recurring pothole, repairs keep failing quickly
    dict(code="RD-001", event_type="Failure", event_date=date(2022, 3, 10),
         description="Pothole formed near market junction after heavy rain"),
    dict(code="RD-001", event_type="Intervention", event_date=date(2022, 3, 20),
         description="Patch repair applied to pothole"),
    dict(code="RD-001", event_type="Failure", event_date=date(2022, 6, 5),
         description="Pothole reappeared at same spot after monsoon rain"),
    dict(code="RD-001", event_type="Intervention", event_date=date(2022, 6, 15),
         description="Patch repair applied again"),
    dict(code="RD-001", event_type="Failure", event_date=date(2022, 9, 2),
         description="Pothole reappeared, road surface block of debris nearby"),
    dict(code="RD-001", event_type="Intervention", event_date=date(2023, 4, 12),
         description="Full resurfacing of the stretch completed"),
    dict(code="RD-001", event_type="Failure", event_date=date(2024, 8, 20),
         description="Minor pothole near same location after heavy rain"),
 
    # RD-002 — light history
    dict(code="RD-002", event_type="Failure", event_date=date(2023, 1, 15),
         description="Surface cracking observed"),
    dict(code="RD-002", event_type="Intervention", event_date=date(2023, 2, 1),
         description="Cracks sealed"),
 
    # RD-003 — minimal, mostly clean
    dict(code="RD-003", event_type="Intervention", event_date=date(2023, 6, 1),
         description="Routine inspection, preventive resurfacing"),
 
    # PIPE-001 — recurring leak, rain related, short intervention survival
    dict(code="PIPE-001", event_type="Failure", event_date=date(2022, 1, 10),
         description="Leak detected near joint A after heavy rain"),
    dict(code="PIPE-001", event_type="Intervention", event_date=date(2022, 1, 18),
         description="Joint clamp replaced"),
    dict(code="PIPE-001", event_type="Failure", event_date=date(2022, 4, 2),
         description="Leak reappeared near same joint, water overflow observed"),
    dict(code="PIPE-001", event_type="Intervention", event_date=date(2022, 4, 12),
         description="Pipe section replaced"),
    dict(code="PIPE-001", event_type="Failure", event_date=date(2022, 7, 5),
         description="Leak again at same section after rain"),
    dict(code="PIPE-001", event_type="Intervention", event_date=date(2023, 2, 25),
         description="Full section relining done"),
    dict(code="PIPE-001", event_type="Failure", event_date=date(2024, 3, 5),
         description="New minor seepage nearby, block in drainage suspected"),
 
    # PIPE-002 — normal
    dict(code="PIPE-002", event_type="Intervention", event_date=date(2023, 5, 10),
         description="Scheduled maintenance completed"),
 
    # LGT-001 — minimal
    dict(code="LGT-001", event_type="Intervention", event_date=date(2023, 11, 1),
         description="Bulb replaced"),
 
    # XFR-001 — overload failures, short-lived fixes
    dict(code="XFR-001", event_type="Failure", event_date=date(2022, 5, 1),
         description="Transformer tripped due to overload"),
    dict(code="XFR-001", event_type="Intervention", event_date=date(2022, 5, 3),
         description="Temporary fuse fix applied"),
    dict(code="XFR-001", event_type="Failure", event_date=date(2022, 7, 20),
         description="Tripped again under peak load"),
    dict(code="XFR-001", event_type="Intervention", event_date=date(2022, 7, 22),
         description="Fuse replaced again"),
    dict(code="XFR-001", event_type="Failure", event_date=date(2023, 1, 20),
         description="Tripped a third time during peak demand"),
    dict(code="XFR-001", event_type="Intervention", event_date=date(2023, 2, 5),
         description="Capacity upgrade installed"),
    dict(code="XFR-001", event_type="Failure", event_date=date(2024, 6, 18),
         description="Isolated trip during heatwave"),
]
 
count = 0
for e in events_data:
    asset = asset_objs[e["code"]]
    ev = Event(
        asset_id=asset.id,
        event_type=e["event_type"],
        event_date=e["event_date"],
        description=e["description"],
        outcome="",
    )
    db.add(ev)
    count += 1
 
db.commit()
print(f"Created {count} events.")
 
db.close()
print("Seeding complete. Event types now match 'Failure' / 'Intervention' exactly.")