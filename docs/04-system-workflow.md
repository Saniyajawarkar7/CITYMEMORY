# 4. System Workflow

## 4.1 Overview

CITYMEMORY follows a continuous workflow that converts infrastructure events into structured historical memory and then uses that memory to support future decisions.

The overall workflow is:

**Data → Memory → Analysis → Intelligence → Decision Support → Outcome → Memory**

The system is designed so that new outcomes can be written back into the infrastructure history, allowing the memory to grow over time.

---

## 4.2 High-Level Workflow

```text
Data Sources
     ↓
Data Ingestion
     ↓
Data Cleaning & Standardization
     ↓
Infrastructure Memory
     ↓
Historical Intelligence
     ↓
Decision Support
     ↓
Preventive Action
     ↓
Observed Outcome
     ↓
Write Back to Memory
```
---
## 4.3 Step 1 — Data Sources

CITYMEMORY can work with multiple sources of infrastructure information.

Potential sources include:

Citizen complaints
Inspection records
Maintenance and repair records
Infrastructure asset registries
GIS information
Weather and environmental information
Images and field observations

The exact sources available will depend on the municipality and the infrastructure category being implemented.
---
## 
4.4 Step 2 — Data Ingestion

Records from available sources are collected and brought into a common system.

The ingestion layer is responsible for receiving information such as:

Asset identifiers
Event dates
Locations
Event types
Inspection details
Intervention details
Outcome information
Contextual information

Where multiple systems use different formats, the information is mapped into a common CITYMEMORY structure.
---
4.5 Step 3 — Data Cleaning and Standardization

Infrastructure records may contain inconsistent names, incomplete fields, duplicate records, or different formats.

The preprocessing stage can therefore perform tasks such as:

Field standardization
Date normalization
Location validation
Duplicate detection
Missing-value handling
Event-type normalization
Asset identifier matching
Text cleaning

The purpose is to create reliable records before applying historical analysis
---
## 4.6 Step 4 — Infrastructure Memory

After preprocessing, records are connected to infrastructure assets.

The core relationship is:

Asset → Incident → Inspection → Intervention → Outcome → Context

This creates a historical timeline for each asset or location.
For example
``` text
Asset: Road R-104

2023
  └── Failure
        ↓
      Patch Repair

2024
  └── Failure
        ↓
      Patch Repair

2025
  └── Failure
        ↓
      Drainage Intervention

2026
  └── New Failure
```
---
## 4.7 Step 5 — Historical Intelligence

Once the infrastructure history is available, CITYMEMORY applies multiple analysis modules.

Recurrence Analysis

Identifies repeated failures associated with an asset or location.

Intervention Survival Analysis

Measures the observed duration between an intervention and subsequent recurrence.

Infrastructure Amnesia

Highlights repeated short-lived intervention cycles.

Failure Echo Analysis

Examines spatial-temporal relationships between historical failures.

Failure Signature Analysis

Identifies recurring contextual combinations associated with failures.

Historical Intervention Comparison

Compares observed outcomes of historically comparable interventions.

These analyses generate evidence rather than replacing engineering judgment
---
## 4.8 Step 6 — Decision Support

The intelligence generated from historical records is presented to users through the decision-support layer.

Possible outputs include:

Asset history
Recurrence indicators
Intervention survival information
Infrastructure Amnesia flags
Failure relationships
Failure signatures
Historical intervention comparisons
Preventive action priorities

The purpose is to make historical evidence available at the point where infrastructure decisions are being considered.
---
## 4.9 Step 7 — Preventive Action Prioritization

The Memory-Weighted Preventive Action Planner combines relevant historical signals.

Potential factors include:

Failure recurrence
Intervention survival
Infrastructure Amnesia
Failure signatures
Failure echoes
Asset criticality
Current condition
Cost or budget constraints

The system can produce a ranked list of assets or actions requiring attention.

Example: 
``` start
Asset: Road R-104
Priority: HIGH

Historical Evidence:
• Repeated failures
• Short observed intervention survival
• Similar failure context observed previously
• Related nearby failures
• High asset criticality
```
---
## 4.10 Step 8 — Human Decision

CITYMEMORY does not autonomously make engineering decisions.

A municipal engineer or authorized decision-maker reviews the available evidence and selects the appropriate action.

This human-in-the-loop approach is important because:

Infrastructure conditions can change.
Historical records may be incomplete.
Engineering constraints may not be fully represented in the data.
Field knowledge can provide information that is not available in digital records.

---
## 4.11 Step 9 — Intervention

After a decision is made, the selected maintenance or preventive intervention is performed through the existing municipal workflow.

Examples may include:

Road repair
Drainage correction
Pipeline maintenance
Streetlight replacement
Utility maintenance
Other infrastructure-specific interventions

CITYMEMORY does not require the initial prototype to replace these operational workflows.
---
## 4.12 Step 10 — Observe Outcome

After an intervention, the resulting condition can be recorded.

Depending on available data, the outcome may include:

Intervention completion
Observed condition
Subsequent recurrence
Duration until recurrence
Inspection observations
Additional contextual information

This information becomes valuable for evaluating the historical performance of interventions.
---
## 4.13 Step 11 — Write Back to Memory

The final stage closes the loop.

The new intervention and its observed outcome are added to the infrastructure history.

The cycle therefore becomes:
``` text
Historical Memory
      ↓
Current Failure
      ↓
Analysis
      ↓
Decision Support
      ↓
Intervention
      ↓
Observed Outcome
      ↓
Updated Historical Memory
```
---
This is the core institutional-memory concept behind CITYMEMORY.
---
## 4.14 End-to-End Example

Consider a road that repeatedly deteriorates after periods of heavy rainfall.

Event

A new deterioration complaint is received.

Memory Retrieval

CITYMEMORY identifies the corresponding road asset and retrieves its historical timeline.

The history shows:

Multiple previous failures
Previous patch repairs
A drainage-related intervention
Different observed stability periods
Historical Analysis

The system evaluates:

Recurrence

The road has failed repeatedly.

Intervention Survival

Previous interventions show different observed durations before recurrence.

Infrastructure Amnesia

Repeated short-lived repair cycles are identified.

Failure Echo

Nearby drainage or road failures are examined for historical spatial-temporal relationships.

Failure Signature

The current context is compared with recurring historical contexts such as rainfall and drainage conditions.

Historical Intervention Comparison

Previous intervention outcomes are compared where records are sufficiently comparable.

Decision Support

The Preventive Action Planner combines the available evidence and ranks the asset for attention.

The user can see both the recommendation and the historical reasons behind it.

Outcome

After the selected intervention is completed, the observed outcome is recorded.

The new record becomes part of the road's future infrastructure memory.
---
## 4.15 System Workflow Diagram

The complete CITYMEMORY workflow can be represented as:
``` text
┌─────────────────────────────────────┐
│          DATA SOURCES               │
│ Complaints | Inspections | Repairs  │
│ GIS | Weather | Images              │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│       INGESTION & CLEANING          │
│ Standardization | Validation        │
│ Matching | Missing Data Handling    │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│       CITYMEMORY DATA MODEL         │
│ Asset → Incident → Inspection       │
│ → Intervention → Outcome → Context  │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│      HISTORICAL INTELLIGENCE        │
│ Recurrence | Survival | Amnesia     │
│ Echo | Signature | Comparison       │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│          DECISION LAYER             │
│ Evidence | Prioritization           │
│ Preventive Action Recommendations   │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│          HUMAN DECISION             │
│ Engineer / Authorized Decision Maker │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│            INTERVENTION             │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│         OBSERVED OUTCOME            │
└──────────────────┬──────────────────┘
                   │
                   └──────────────┐
                                  ↓
                       ┌────────────────────┐
                       │ WRITE BACK TO      │
                       │ INFRASTRUCTURE     │
                       │ MEMORY             │
                       └────────────────────┘
```
---
## 4.16 Prototype Demonstration Flow

The CITYMEMORY prototype can demonstrate the workflow through the following sequence:
``` text
Select Asset
     ↓
View Asset Memory
     ↓
View Historical Events
     ↓
Check Recurrence
     ↓
Check Intervention Survival
     ↓
View Infrastructure Amnesia
     ↓
View Failure Echoes
     ↓
View Failure Signature
     ↓
Compare Historical Interventions
     ↓
View Preventive Recommendation
```
---
This sequence demonstrates how the individual features work together as one infrastructure-memory system.
---
## 4.17 Workflow Design Principles

CITYMEMORY follows several important principles.

History First

Historical evidence is retrieved before generating a preventive recommendation.

Explainability

Decision-support outputs should show the historical evidence contributing to them.

Human in the Loop

Final engineering decisions remain with authorized users.

No Unjustified Causality

Spatial or temporal relationships are presented as associations unless stronger evidence is available.

Continuous Memory

New intervention outcomes can become part of the system's future evidence base.

Phased Deployment

The system can begin with a limited infrastructure class and geographic area before expanding.
---
## 4.18 Summary

CITYMEMORY converts fragmented infrastructure events into a continuous workflow:

Collect → Connect → Remember → Analyze → Compare → Prioritize → Act → Observe → Remember Again

The key distinction is that the system does not stop after recording an infrastructure event.

It attempts to preserve the lesson from that event so that future infrastructure decisions can benefit from the city's accumulated experience.

