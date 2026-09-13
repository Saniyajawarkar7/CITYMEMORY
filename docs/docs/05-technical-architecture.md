# 5. Technical Architecture

## 5.1 Architecture Overview

CITYMEMORY follows a modular web-based architecture consisting of:

- A web dashboard for infrastructure visualization and interaction
- A FastAPI backend for application logic and APIs
- A relational data layer for infrastructure assets and events
- Separate intelligence services for recurrence, survival, echo, signature, comparison, and planning
- A future-ready spatial architecture for GIS and larger-scale deployment

The high-level architecture is:

```text
┌──────────────────────────────────────────────┐
│              DATA SOURCES                    │
│ Complaints | Inspections | Repairs | GIS     │
│ Weather | Images | Field Records             │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│          DATA INGESTION & PROCESSING         │
│ Validation | Cleaning | Standardization      │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│             CITYMEMORY DATA LAYER            │
│ Asset | Incident | Intervention | Outcome    │
│ Context | Location | Historical Events       │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│           INTELLIGENCE SERVICES              │
│                                              │
│ Recurrence / Amnesia                        │
│ Intervention Survival                       │
│ Failure Echo                                │
│ Failure Signature                           │
│ Historical Comparison                       │
│ Preventive Action Planner                   │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│              DECISION LAYER                  │
│ Historical Evidence | Priority | Explanation │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│             CITYMEMORY DASHBOARD             │
│ Map | Asset History | Intelligence | Actions │
└──────────────────────┬───────────────────────┘
                       ↓
              Human Decision-Maker
                       ↓
                New Intervention
                       ↓
                Observed Outcome
                       ↓
              Write Back to Memory
```
---
## 5.2 Frontend Architecture

The current prototype uses a React-based frontend with Vite as the development and build tool.

The frontend is responsible for:

Displaying infrastructure assets
Showing infrastructure locations on a map
Presenting asset history
Displaying historical intelligence
Showing recommendations and priority information
Providing an interface for interacting with the backend APIs
Current Frontend Stack
React
Vite
Leaflet
React-Leaflet

Leaflet and React-Leaflet provide the mapping layer for geographic infrastructure visualization.
---
## 5.3 Backend Architecture

The backend is implemented using Python and FastAPI.

FastAPI provides:

REST-style API endpoints
Request handling
Backend application logic
Integration with the database layer
Communication between the frontend and intelligence services

The current prototype exposes separate route modules for infrastructure assets and events.

Conceptually:
``` text
React Frontend
      ↓
FastAPI Backend
      ↓
Route Layer
      ↓
Database / Intelligence Services
```
---
The backend is intentionally modular so that individual intelligence capabilities can evolve independently.
---
## 5.4 Database Layer

CITYMEMORY uses SQLAlchemy as the ORM layer.

The current prototype supports a relational database configuration and uses SQLite as the local demonstration database by default.

The database configuration can also be supplied through the DATABASE_URL environment variable.

For larger-scale deployment, a PostgreSQL/PostGIS architecture can be considered for stronger relational and geospatial capabilities.

The repository documentation describes PostgreSQL/PostGIS as a scalable deployment consideration rather than claiming that the current demonstration environment is already running on it.
---
## 5.5 Current Prototype Data Model

The current prototype uses an asset-centric relational model.

At its core are two primary entities:
``` text
Asset
  │
  └── Event
```
---
An asset represents an infrastructure object or location.

An event represents a historical occurrence associated with that asset.

The current prototype event structure supports fields such as:

Event type
Event date
Description
Outcome
Asset association

The broader CITYMEMORY methodology extends this into:
``` start
Asset
  │
  ├── Incident
  │      └── Inspection
  │
  ├── Intervention
  │      └── Outcome
  │
  └── Context
```
---
This distinction is important:

The conceptual data model is broader than the simplified database model used in the current prototype.
---
## 5.6 Asset Representation

Each infrastructure asset can contain information such as:

Unique asset code
Asset type
Latitude
Longitude
Installation date
Current condition
Importance / criticality
Associated historical events

Example:
``` start
Asset
────────────────────────
Code: RD-104
Type: Road
Location: Geographic coordinates
Condition: Poor
Importance: High
        │
        ├── Failure Event
        ├── Intervention Event
        ├── Failure Event
        └── Inspection Event
```
This asset-centric representation allows historical events to remain connected to the infrastructure they belong to.
---
## 5.7 Event Representation

An event represents a significant infrastructure occurrence.

Possible event types include:

Failure
Intervention
Inspection
Other maintenance-related events

Each event can contain:

Associated asset
Event type
Event date
Description
Outcome information

The event history provides the chronological basis for CITYMEMORY's historical analysis.
---
## 5.8 Intelligence Service Layer
The prototype separates the major intelligence capabilities into individual backend services.

The current service modules include:
``` start
services/
├── amnesia.py
├── comparison.py
├── echo.py
├── planner.py
├── signature.py
└── survival.py
```
---
This modular structure maps directly to the six core CITYMEMORY capabilities.

Amnesia Service

Identifies repeated short-lived intervention or failure cycles.

Survival Service

Calculates or analyzes observed duration between interventions and subsequent failures.

Echo Service

Examines relationships between historical failures across assets.

Signature Service

Identifies recurring contextual patterns in failure information.

Comparison Service

Compares historical intervention outcomes.

Planner Service

Combines relevant signals to generate preventive prioritization.

The separation of services makes the architecture easier to test, extend, and replace.
---
## 5.9 API Layer
The backend exposes application endpoints for assets and events.

The intended API structure is organized around resources such as:
``` start

GET  /assets
GET  /assets/{id}
GET  /assets/{id}/memory

GET  /events
POST /events

GET  /survival
GET  /echoes
GET  /signature
GET  /comparison
GET  /recommendations
```
---
## 5.10 Frontend–Backend Communication

The communication flow is:
``` start
User
  ↓
React Dashboard
  ↓
HTTP API Request
  ↓
FastAPI
  ↓
Route Handler
  ↓
Database / Intelligence Service
  ↓
Processed Response
  ↓
React Dashboard
  ↓
Visualization
```
---
For example:
---
``` start
User selects Road R-104
        ↓
Frontend requests asset history
        ↓
FastAPI retrieves asset/events
        ↓
Historical services process relevant records
        ↓
Backend returns structured evidence
        ↓
Dashboard displays timeline and intelligence
```
---
## 5.11 Geospatial Layer
CITYMEMORY is designed around infrastructure locations.

The current prototype represents assets using latitude and longitude and uses Leaflet for map visualization.

This enables functions such as:

Asset location display
Nearby asset identification
Spatial event visualization
Historical failure mapping

For a production-scale deployment, PostGIS can provide more advanced spatial querying and indexing.

Potential future spatial capabilities include:

Distance-based asset relationships
Spatial clustering
Geographic failure density
Infrastructure network relationships
Spatial-temporal analysis
---
5.12 Historical Intelligence Pipeline

The intelligence layer processes historical events in multiple stages.
``` start
Historical Events
       ↓
Filter by Asset / Location
       ↓
Sort by Time
       ↓
Calculate Recurrence Signals
       ↓
Measure Intervention Survival
       ↓
Identify Repeated Cycles
       ↓
Analyze Spatial-Temporal Relationships
       ↓
Extract Failure Context
       ↓
Compare Historical Interventions
       ↓
Generate Preventive Priority
```
---
Each stage contributes evidence to the final decision-support output.
---

# 5.13 Explainability and Human-in-the-Loop

CITYMEMORY is designed as a decision-support system. Its recommendations should be accompanied by the historical evidence that contributed to them.

Instead of showing only:

**Priority: HIGH**

the system can present supporting evidence such as:

- Repeated historical failures
- Short observed intervention survival
- Repeated intervention cycles
- Similar historical failure contexts
- Related nearby failures
- High asset importance

Example:

```text
Priority: HIGH

Supporting Evidence:
• Repeated historical failures
• Short observed intervention survival
• Similar historical failure context
• Related nearby failures
• High asset criticality
```
---
This makes the output easier for infrastructure teams to inspect and challenge.
---

## 5.14 Human-in-the-Loop Architecture

CITYMEMORY is a decision-support system.

The architecture intentionally keeps a human decision-maker between the recommendation and the actual intervention.
``` text

Historical Data
      ↓
CITYMEMORY Analysis
      ↓
Recommendation
      ↓
Human Review
      ↓
Engineering / Maintenance Decision
      ↓
Intervention
      ↓
Observed Outcome
      ↓
CITYMEMORY Memory
```
---
This is important because historical data may be incomplete and infrastructure decisions can involve factors that are not represented in digital records.
---
## 5.15 Continuous Learning Architecture

The system is designed around a feedback loop.
``` text
        ┌──────────────────────┐
        │ Historical Memory    │
        └──────────┬───────────┘
                   ↓
             New Incident
                   ↓
              Analysis
                   ↓
          Decision Support
                   ↓
             Intervention
                   ↓
          Observed Outcome
                   ↓
        ┌──────────────────────┐
        │ Write Back to Memory │
        └──────────┬───────────┘
                   │
                   └──────────────→ Future Analysis
```
---
This creates the institutional-memory effect that differentiates CITYMEMORY from systems that only record current complaints or work orders
---
## 5.16 Security and Access Considerations

A production deployment should include:

Authentication
Role-based access control
Secure API communication
Audit logging
Data validation
Protection of sensitive infrastructure information
Controlled access to operational records
Backup and recovery mechanisms

The current prototype focuses on demonstrating the core infrastructure-memory workflow rather than implementing a complete production security system.
---
## 5.17 Deployment Architecture
Prototype Deployment

The current prototype can run locally as two application components:
``` text
Frontend
React + Vite
localhost:5173
       ↓
Backend
FastAPI
       ↓
SQLite Demonstration Database
```
---
## Scalable Deployment

A future deployment can use:
``` text
Users
  ↓
Web Application
  ↓
API Server
  ↓
Application / Intelligence Services
  ↓
PostgreSQL + PostGIS
  ↓
Municipal Data Sources
```
---
Additional services can be introduced as system scale and data volume increase.
---
## 5.18 Technology Summary
Layer	Technology / Approach
Frontend	React
Frontend Tooling	Vite
Mapping	Leaflet / React-Leaflet
Backend	Python / FastAPI
ORM	SQLAlchemy
Database	SQLite for local prototype
Scalable Database	PostgreSQL/PostGIS considered
Analytics	Python-based rule/statistical analysis
Spatial Processing	Geographic coordinates and spatial analysis
Architecture	Modular web application

The project documentation identifies React, Vite, Leaflet, Python, FastAPI, SQLAlchemy, Pandas, scikit-learn, relational storage, and PostgreSQL/PostGIS as relevant parts of the technical approach.
---
## 5.19 Prototype vs Production

CITYMEMORY intentionally separates the demonstration architecture from the production architecture.

Current Prototype
Local web application
React/Vite frontend
FastAPI backend
SQLAlchemy database layer
SQLite demonstration database
Modular intelligence services
Demonstration/sample data
Leaflet-based map
Production Direction
PostgreSQL/PostGIS
Municipal system integration
Stronger authentication and authorization
Data validation and governance
Larger historical datasets
More advanced spatial analysis
Scalable deployment infrastructure
Expanded monitoring and audit capabilities

The current prototype uses demonstration/sample data and should not be interpreted as live municipal infrastructure data
---
## 5.20 Architecture Design Principles

CITYMEMORY follows these architectural principles:

Modular

Each intelligence capability is separated into an independent service or logical module.

Asset-Centric

Historical information is connected to the infrastructure asset or location.

Explainable

Decision-support outputs should expose the historical evidence behind them.

Extensible

New infrastructure categories and data sources can be added without redesigning the entire system.

Spatially Aware

Infrastructure locations are first-class information in the system.

Human-in-the-Loop

Recommendations support rather than replace engineering decisions.

Feedback Driven

Observed intervention outcomes can become part of future infrastructure memory.
---
## 5.21 Summary

CITYMEMORY combines a web dashboard, API backend, relational data model, geospatial representation, and modular historical intelligence services.

The architecture can be summarized as:

React → FastAPI → SQLAlchemy / Database → Intelligence Services → Decision Support → Dashboard

The broader system adds:

Municipal Data → Infrastructure Memory → Historical Intelligence → Preventive Decision → Outcome → Updated Memory

The key architectural objective is not simply to store infrastructure records, but to create a technical foundation through which historical infrastructure experience can be retrieved, analyzed, explained, and reused.
``` start



### Commit it as:

```text
Add technical architecture documentation
```



