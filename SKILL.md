# Snowflake Monitoring Assessment Skill

## Objective

Assess Snowflake account activity and recommend monitoring rules based on observed administrative, security, governance, and compute-related activity.

This skill helps identify what should be monitored in a Snowflake account, enables relevant preset monitoring rules, detects reportable events, and summarises events using Cortex.

This enables a data platform team to quickly understand:
- What activity is occurring in their Snowflake environment
- What should be monitored
- How to operationalise monitoring

## Prerequisites

- Active Snowflake connection (`cortex connections list`)
- Access to `ACCOUNTADMIN` role

## Available SQL Assets

The SQL implementation is provided in the `sql/` directory:

1. `01_account_environment_setup.sql`
   - Creates the assessment role, warehouse, database, and schema.

2. `02_assessment_views.sql`
   - Creates activity classification views over Snowflake account metadata and query history.

3. `03_assessment_tables.sql`
   - Creates monitoring rule and monitoring event tables.

4. `04_seed_monitoring_rules.sql`
   - Seeds preset monitoring rules by domain.

5. `05_assessment_procedures.sql`
   - Provides procedures to enable rules, monitor events, and summarise events with Cortex.

6. `06_teardown.sql`
   - Cleanup or drop all objects created by the skill.

## Workflow

### Step 1: Validate Connection

Goal: Establish a connection to Snowflake. 

Actions:

1. Execute to get account context:

    ```sql
    SELECT CURRENT_ACCOUNT() AS ACCOUNT,
          CURRENT_REGION() AS REGION,
          CURRENT_ROLE() AS ROLE,
          CURRENT_USER() AS USERNAME,
    ```

2. Present to user:

    ```.md
    Snowflake Account
    ========================
    Account:    [account]
    Region:     [region]
    Role:       [role]
    User:       [username]
    ```

### Step 2: Build Monitoring Assessment Objects

Goal: Build complete Monitoring Assessment objects.  

Actions:

Execute the scripts in the `sql/` directory exactly as written in this order:

- 01_account_environment_setup.sql
- 02_assessment_views.sql
- 03_assessment_tables.sql
- 04_seed_monitoring_rules.sql
- 05_assessment_procedures.sql

**DO NOT CONTINUE PAST THIS STEP**: Users must confirm if they would like to proceed with the assessment. 

### Step 3: Execute Domain Assessment and Present Results

Goal: Shows Snowflake activity for each Domain over the last 90 days.

Actions:

Run the view `V_DOMAIN_ASSESSMENT` and present results to the user. 

**DO NOT CONTINUE PAST THIS STEP**: Users must confirm if they would like to proceed with enabling monitoring rules.  

### Step 4: Enable Monitoring Rules

Goal: Enable monitoring rules to capture events for required Domains.

Actions:

Execute the stored procedure `SP_UPDATE_MONITORING_RULES` with the required rule and enablement status passed in.

**DO NOT CONTINUE PAST THIS STEP**: Users must confirm if they would like to proceed enabling more Domains or continue to executing the event monitoring steps. 

### Step 5: Execute Event Monitoring Procedures

Goal: Establish a connection to Snowflake. 

Actions:

Execute the following stored procedure to begin tracking events for enabled Domains:
- `SP_MONITOR_EVENTS`
- `SP_CORTEX_SUMMARIZE_EVENTS`

**DO NOT CONTINUE PAST THIS STEP**: Workflow should end here, but provide a suggestion of building the streamlit app. 

### Step 6: Produce Streamlit App (Optional)

Goal: Create a Streamlit app to visualise the Domain assessment results and monitored events. 

Actions:

Use the `app.py` in the `streamlit/` directory to create a streamlit app `MONITORING_ASSESSMENT_APP` in the database and schema `MONITORING_ASSESSMENT_DB.ASSESSMENT`.

## Cleanup / Teardown (Optional)

If required, all objects created by this solution can be removed.

Execute this script in the `sql/` directory exactly as written:
  ```
  06_teardown.sql
  ```