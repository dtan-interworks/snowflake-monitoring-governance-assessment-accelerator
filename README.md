# Snowflake Monitoring & Governance Assessment Accelerator

## Contents

- [Snowflake Monitoring \& Governance Assessment Accelerator](#snowflake-monitoring--governance-assessment-accelerator)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Problem Statement](#problem-statement)
  - [Solution](#solution)
  - [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation and Usage](#installation-and-usage)
  - [Assessment Objects](#assessment-objects)
  - [Streamlit App](#streamlit-app)
  - [Cleanup / Teardown](#cleanup--teardown)

## Overview

This solution provides a Snowflake-native, Cortex-powered capability to assess monitoring and governance readiness based on actual platform activity.

It enables teams to:

- Analyse Snowflake account activity
- Identify monitoring opportunities
- Recommend monitoring rules
- Detect reportable events
- Generate AI-powered summaries of activity

## Problem Statement

Snowflake environments often lack visibility into:

- Access control changes
- Integration activity
- Compute configuration changes
- Governance events

Traditional approaches rely on static best practices rather than actual observed behaviour.


## Solution

This accelerator uses Snowflake metadata and query history to:

1. Detect real activity across key domains
2. Classify activity into monitoring categories
3. Recommend monitoring rules based on observed behaviour
4. Detect reportable events
5. Use Cortex AI to explain events in natural language

## Architecture

```
Snowflake Metadata Layer
   ↓
Domain Assessment and Activity Classification Views
   ↓
Monitoring Rule Recommendations
   ↓
Event Detection & Cortex AI Summarisation
```

## Project Structure 

```
snowflake-monitoring-governance-assessment-accelerator/
├── SKILL.md                               # Cortex Code skill definition and workflow
├── README.md                              # Project overview, setup, and usage guide
├── streamlit/                             # Optional UI layer
│   └── app.py                             # Streamlit app for visualising assessment, rules, and events
└── sql/                                   # Core Snowflake implementation
    ├── 01_account_environment_setup.sql   # Creates role, warehouse, database, and schema
    ├── 02_assessment_views.sql            # Activity classification views (query history → domains)
    ├── 03_assessment_tables.sql           # Monitoring rules and events tables
    ├── 04_seed_monitoring_rules.sql       # Predefined rule library
    ├── 05_assessment_procedures.sql       # Detection logic, rule updates, and Cortex summarisation
    └── 06_teardown.sql                    # Cleanup script for all deployed objects
```

## Prerequisites 

- Cortex Code CLI installed
- Access to a Snowflake Account
- Access to `ACCOUNTADMIN` Role

## Installation and Usage

1. Install [Cortex Code CLI](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-cli)

2. Clone the skill repository into your current directory

    ```
    git clone https://github.com/dtan-interworks/snowflake-monitoring-governance-assessment-accelerator.git
    ```
3. Run the following command to begin working with Cortex in your CLI

    ```
    cortex
    ```

4. Validate your Snowflake connection

    ```
    cortex connections list
    ```

5. With Cortex, simply ask or use the following prompt:

    ```
    Could you explain what the Snowflake Monitoring and Governance assessment does?
    ```
    ```
    Run the setup of the Monitoring and Governance assessment skill
    ```
    ```
    Run the domain assessment and present the results
    ```
    ```
    Enable the monitoring rule for the top 3 active domains
    ```


## Assessment Objects 

The following Snowflake objects are created as part of the Monitoring & Governance Assessment Accelerator:

| Name | Type | Description |
|------|------|-------------|
| `MONITORING_ASSESSMENT_ROLE` | Role | Custom role used to execute monitoring assessment queries and access Snowflake account metadata. |
| `MONITORING_ASSESSMENT_WH` | Warehouse | Dedicated virtual warehouse used to run assessment queries and monitoring procedures. |
| `MONITORING_ASSESSMENT_DB` | Database | Database used to store all monitoring assessment objects including views, tables, and procedures. |
| `ASSESSMENT` | Schema | Schema that contains all monitoring-related objects such as views, tables, and stored procedures. |
| `V_DOMAIN_ASSESSMENT` | View | Aggregates query history into activity domains (e.g. access control, compute, governance) with counts and latest activity timestamps. |
| `V_<RULE_DOMAIN>` | View | Maps observed activity domains to recommended monitoring rules. 12 views in total, one for each domain. |
| `MONITORING_RULES` | Table | Stores predefined monitoring rules with domains, descriptions, corresponding views, and enablement status. |
| `MONITORING_EVENTS` | Table | Stores detected events based on enabled monitoring rules, including query details, timestamps, and Cortex summaries. |
| `SP_UPDATE_MONITORING_RULES` | Stored Procedure | Updates the enabled/disabled status of monitoring rules based on assessment recommendations. |
| `SP_MONITOR_EVENTS` | Stored Procedure | Scans Snowflake query history and inserts matching events into the monitoring events table. |
| `SP_CORTEX_SUMMARIZE_EVENTS` | Stored Procedure | Uses Snowflake Cortex to generate natural language summaries for detected monitoring events. |
| `MONITORING_ASSESSMENT_APP` | Streamlit App | Optional visual interface for reviewing assessment results, rule status, detected events, and Cortex-generated summaries. |


## Streamlit App

An optional Streamlit in Snowflake is included to visualise:

- observed activity by domain
- recommended monitoring rules
- enabled and disabled rule status
- detected monitoring events
- Cortex-generated event summaries

Use the following Cortex prompt to setup the app:

```
Enable the Streamlit application for the Monitoring and Governance assessment skill
```


## Cleanup / Teardown 

To remove all deployed Snowflake objects created by this solution, use the following Cortex prompt:


```
Run the teardown steps to remove all objects created by the Monitoring and Governance assessment skill
```

⚠️ This will delete all monitoring configuration, rules, and detected events.



