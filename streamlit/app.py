import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Snowflake Monitoring Assessment",
    layout="wide"
)

session = get_active_session()

DB = "MONITORING_ASSESSMENT_DB"
SCHEMA = "ASSESSMENT"

def run_sql(sql: str):
    return session.sql(sql).collect()

def load_df(sql: str) -> pd.DataFrame:
    return session.sql(sql).to_pandas()

st.title("Snowflake Monitoring & Governance Assessment")
st.caption("Visualise assessment activity, rule status, detected events, and Cortex summaries.")

# -------------------------
# Actions
# -------------------------
with st.sidebar:
    st.header("Actions")

    if st.button("Run Event Monitoring"):
        run_sql(f"CALL {DB}.{SCHEMA}.SP_MONITOR_EVENTS()")
        st.success("Event monitoring completed.")

    if st.button("Generate Cortex Summaries"):
        run_sql(f"CALL {DB}.{SCHEMA}.SP_CORTEX_SUMMARIZE_EVENTS()")
        st.success("Cortex summaries generated.")

    st.divider()
    st.caption("Use the Rules tab to enable or disable monitoring rules.")

# -------------------------
# Tabs
# -------------------------
tab_summary, tab_rules, tab_events = st.tabs(
    ["Assessment Summary", "Monitoring Rules", "Detected Events"]
)

# -------------------------
# Tab 1: Assessment Summary
# -------------------------
with tab_summary:
    st.subheader("Observed Activity by Domain")

    domain_df = load_df(f"""
        SELECT *
        FROM {DB}.{SCHEMA}.V_DOMAIN_ASSESSMENT
        ORDER BY QUERY_COUNT DESC
    """)

    if domain_df.empty:
        st.info("No assessed activity found.")
    else:
        total_domains = len(domain_df)
        active_domains = int((domain_df["QUERY_COUNT"] > 0).sum())
        total_activity = int(domain_df["QUERY_COUNT"].sum())

        c1, c2, c3 = st.columns(3)
        c1.metric("Domains Assessed", total_domains)
        c2.metric("Active Domains", active_domains)
        c3.metric("Observed Activity", total_activity)

        st.bar_chart(
            domain_df.set_index("QUERY_DOMAIN")["QUERY_COUNT"]
        )

        st.dataframe(domain_df, use_container_width=True)

# -------------------------
# Tab 2: Monitoring Rules
# -------------------------
with tab_rules:
    st.subheader("Monitoring Rule Status")

    rules_df = load_df(f"""
        SELECT
            RULE_ID,
            RULE_DOMAIN,
            RULE_DESCRIPTION,
            ENABLED
        FROM {DB}.{SCHEMA}.MONITORING_RULES
        ORDER BY RULE_ID
    """)

    if rules_df.empty:
        st.info("No monitoring rules found.")
    else:
        enabled_count = int(rules_df["ENABLED"].sum())
        disabled_count = len(rules_df) - enabled_count

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rules", len(rules_df))
        c2.metric("Enabled", enabled_count)
        c3.metric("Disabled", disabled_count)

        selected_domain = st.selectbox(
            "Filter by domain",
            ["All"] + sorted(rules_df["RULE_DOMAIN"].dropna().unique().tolist())
        )

        filtered_rules = rules_df.copy()
        if selected_domain != "All":
            filtered_rules = filtered_rules[filtered_rules["RULE_DOMAIN"] == selected_domain]

        st.dataframe(filtered_rules, use_container_width=True)

        st.divider()
        st.subheader("Update Rule Status")

        rule_options = {
            f"{row.RULE_ID} - {row.RULE_DOMAIN} - {row.RULE_DESCRIPTION}": row.RULE_ID
            for row in rules_df.itertuples()
        }

        selected_rule_label = st.selectbox("Select rule", list(rule_options.keys()))
        selected_rule_id = rule_options[selected_rule_label]

        new_status = st.checkbox("Enabled", value=bool(
            rules_df.loc[rules_df["RULE_ID"] == selected_rule_id, "ENABLED"].iloc[0]
        ))

        if st.button("Update Selected Rule"):
            run_sql(f"""
                CALL {DB}.{SCHEMA}.SP_UPDATE_MONITORING_RULES(
                    {selected_rule_id},
                    {str(new_status).upper()}
                )
            """)
            st.success(f"Rule {selected_rule_id} updated.")
            st.experimental_rerun()

# -------------------------
# Tab 3: Detected Events
# -------------------------
with tab_events:
    st.subheader("Detected Events")

    events_df = load_df(f"""
        SELECT
            ev.EVENT_ID,
            r.RULE_DOMAIN,
            r.RULE_DESCRIPTION,
            ev.EVENT_TIME,
            ev.USER_NAME,
            ev.ROLE_NAME,
            ev.CORTEX_SUMMARY,
            ev.QUERY_TEXT
        FROM {DB}.{SCHEMA}.MONITORING_EVENTS ev
        JOIN {DB}.{SCHEMA}.MONITORING_RULES r
            ON ev.RULE_ID = r.RULE_ID
        ORDER BY ev.EVENT_TIME DESC
    """)

    if events_df.empty:
        st.info("No detected events found. Run event monitoring first.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Events", len(events_df))
        c2.metric("Domains", events_df["RULE_DOMAIN"].nunique())
        c3.metric("With Cortex Summary", events_df["CORTEX_SUMMARY"].notna().sum())

        selected_event_domain = st.selectbox(
            "Filter events by domain",
            ["All"] + sorted(events_df["RULE_DOMAIN"].dropna().unique().tolist()),
            key="event_domain_filter"
        )

        filtered_events = events_df.copy()
        if selected_event_domain != "All":
            filtered_events = filtered_events[
                filtered_events["RULE_DOMAIN"] == selected_event_domain
            ]

        st.dataframe(
            filtered_events[
                [
                    "EVENT_ID",
                    "RULE_DOMAIN",
                    "RULE_DESCRIPTION",
                    "EVENT_TIME",
                    "USER_NAME",
                    "ROLE_NAME",
                    "CORTEX_SUMMARY"
                ]
            ],
            use_container_width=True
        )

        st.divider()
        st.subheader("Event Detail")

        event_ids = filtered_events["EVENT_ID"].tolist()
        selected_event_id = st.selectbox("Select event", event_ids)

        selected_event = filtered_events[
            filtered_events["EVENT_ID"] == selected_event_id
        ].iloc[0]

        st.markdown("### Cortex Summary")
        st.write(selected_event["CORTEX_SUMMARY"] or "No Cortex summary generated yet.")

        st.markdown("### Query Text")
        st.code(selected_event["QUERY_TEXT"], language="sql")