# 6. Data Model

CITYMEMORY organizes infrastructure history as connected records:

**Asset → Incident → Inspection → Intervention → Outcome → Context**

## Core Entities

- **Asset:** infrastructure identity, type, location and criticality.
- **Incident:** failure/problem, date, description and location.
- **Inspection:** observed condition and inspection details.
- **Intervention:** repair or maintenance action performed.
- **Outcome:** result after intervention, including recurrence or stability.
- **Context:** rainfall, season, nearby failures and other relevant conditions.

## Purpose

This structure preserves the history of each asset and connects failures with previous interventions and outcomes.

The prototype uses a simplified Asset/Event relational model. The production design can extend this model using PostgreSQL/PostGIS for richer spatial and historical analysis.
