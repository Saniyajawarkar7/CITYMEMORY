# Data Dictionary

| Entity | Key Fields | Purpose |
|---|---|---|
| Asset | asset_id, type, location, criticality | Identifies infrastructure |
| Incident | incident_id, asset_id, date, description | Records failures |
| Inspection | inspection_id, asset_id, date, condition | Records observed condition |
| Intervention | intervention_id, asset_id, type, date | Records maintenance actions |
| Outcome | outcome_id, intervention_id, date, result | Records intervention results |
| Context | rainfall, season, nearby_failures | Stores relevant conditions |

## Data Relationships

Asset → Incident → Inspection → Intervention → Outcome → Context

The structure allows CITYMEMORY to connect infrastructure history with intervention outcomes and contextual information.
