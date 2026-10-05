# Power BI Implementation Guide

## Objective

Recreate the IT Operations Dashboard in Power BI Desktop using the synthetic dataset in:

`data/incidents.csv`

The repository is intentionally designed so that another IT professional can reproduce the analysis without access to any private or production system.

## 1. Import the Dataset

In Power BI Desktop:

1. Select **Get data**.
2. Choose **Text/CSV**.
3. Select `data/incidents.csv`.
4. Confirm the first row is being used as headers.
5. Select **Transform Data**.

## 2. Recommended Data Types

Set the columns as follows:

| Column | Recommended type |
|---|---|
| Incident ID | Text |
| Created Date | Date |
| Created Time | Time |
| Priority | Text |
| Category | Text |
| Subcategory | Text |
| Service | Text |
| Assignment Group | Text |
| Department | Text |
| Location | Text |
| Status | Text |
| Resolution Hours | Decimal number |
| SLA Target Hours | Whole number |
| SLA Met | Text |
| First Contact Resolution | Text |
| Reopened | Text |
| Business Impact | Text |
| Root Cause Type | Text |

## 3. Core Measures

Create these measures in the `Incidents` table.

```DAX
Total Incidents =
COUNTROWS(Incidents)

Open Incidents =
CALCULATE(
    COUNTROWS(Incidents),
    Incidents[Status] = "Open"
)

In Progress Incidents =
CALCULATE(
    COUNTROWS(Incidents),
    Incidents[Status] = "In Progress"
)

Resolved and Closed =
CALCULATE(
    COUNTROWS(Incidents),
    Incidents[Status] IN {"Resolved", "Closed"}
)

SLA Compliance % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Incidents),
        Incidents[Status] IN {"Resolved", "Closed"},
        Incidents[SLA Met] = "Yes"
    ),
    [Resolved and Closed]
)

Average MTTR Hours =
CALCULATE(
    AVERAGE(Incidents[Resolution Hours]),
    Incidents[Status] IN {"Resolved", "Closed"}
)

First Contact Resolution % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Incidents),
        Incidents[Status] IN {"Resolved", "Closed"},
        Incidents[First Contact Resolution] = "Yes"
    ),
    [Resolved and Closed]
)

Reopen Rate % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Incidents),
        Incidents[Status] IN {"Resolved", "Closed"},
        Incidents[Reopened] = "Yes"
    ),
    [Resolved and Closed]
)

P1 P2 Incidents =
CALCULATE(
    COUNTROWS(Incidents),
    Incidents[Priority] IN {"P1", "P2"}
)
```

## 4. Executive Dashboard Layout

Build the first page as an executive overview.

### KPI Cards

Use:

- Total Incidents
- Open Incidents
- Resolved and Closed
- SLA Compliance %
- Average MTTR Hours
- First Contact Resolution %
- Reopen Rate %

### Main Visuals

Recommended visuals:

1. **Line chart** — incident volume by month
2. **Donut chart** — incidents by priority
3. **Bar chart** — incidents by category
4. **Bar chart** — average MTTR by priority
5. **100% stacked bar or column chart** — SLA compliance by priority
6. **Donut chart** — incident status
7. **Bar chart** — incident volume by service

## 5. Management Interpretation

The dashboard is intended to move beyond ticket counting.

A manager should be able to identify:

- Which priorities create the greatest operational risk
- Where SLA performance is weakest
- Which services generate the most demand
- Which incident categories may indicate recurring problems
- Whether faster closure is being achieved at the expense of quality
- Where problem-management or service-improvement activity should focus

## 6. Validation

After importing the repository dataset, the dashboard should reproduce the portfolio figures documented in the README approximately as follows:

| KPI | Expected value |
|---|---:|
| Total Incidents | 1,200 |
| Open Incidents | 300 |
| Resolved + Closed | 600 |
| SLA Compliance | 98.7% |
| Average MTTR | 12.4 hours |
| First Contact Resolution | 66.0% |
| Reopen Rate | 6.0% |
| P1 + P2 Incidents | 180 |

Minor presentation differences can occur from Power BI formatting or filter context; the underlying measures should use the definitions above.

## 7. Recommended Future Model

For a more mature implementation, replace the single-table model with a star schema:

```text
                    DimDate
                       |
DimService ---- FactIncident ---- DimPriority
                       |
                 DimCategory
                       |
                DimDepartment
                       |
                  DimLocation
```

This will make the model easier to extend with:

- Change management data
- Problem records
- Service availability
- Asset data
- Knowledge-base usage
- Business impact
- Cost and procurement data

## Portfolio Positioning

This project demonstrates a leadership-oriented workflow:

**ITSM data → operational KPIs → Power BI analysis → management insight → continuous improvement**

It is intentionally framed as a professional proof of concept rather than a generic Power BI tutorial.
