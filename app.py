import streamlit as st
import plotly.express as px
import pandas as pd

from services.parser import extract_pdf_text
from services.prompt_builder import build_prompt
from services.report_parser import parse_report
from services.document_manager import combine_documents
from services.visualizer import (extract_metrics,coverage_dataframe,risk_dataframe)


st.set_page_config(
    page_title="ComplianceMind v0.2",
    layout="wide"
)

st.title("ComplianceMind v0.2")
st.subheader("AI-Powered Multi-Document Compliance Auditor")


# ======================
# SESSION STATE
# ======================

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "audit_prompt" not in st.session_state:
    st.session_state.audit_prompt = ""

if "company_text" not in st.session_state:
    st.session_state.company_text = ""

if "rules_text" not in st.session_state:
    st.session_state.rules_text = ""

if "document_count" not in st.session_state:
    st.session_state.document_count = 0

if "document_names" not in st.session_state:
    st.session_state.document_names = []


# ======================
# FILE UPLOAD
# ======================

company_files = st.file_uploader(
    "Upload Company Documents",
    type="pdf",
    accept_multiple_files=True
)

rules = st.file_uploader(
    "Upload Compliance Rules",
    type="pdf"
)


# ======================
# ANALYZE BUTTON
# ======================

if st.button("Analyze"):

    if company_files and rules:

        documents = {}

        for file in company_files:
            documents[file.name] = extract_pdf_text(file)

        st.session_state.company_text = combine_documents(documents)

        st.session_state.document_count = len(documents)
        st.session_state.document_names = list(documents.keys())

        st.session_state.rules_text = extract_pdf_text(rules)

        st.session_state.audit_prompt = build_prompt(
            st.session_state.company_text,
            st.session_state.rules_text
        )

        st.session_state.analyzed = True

    else:
        st.error("Please upload company documents and compliance rules.")


# ======================
# DISPLAY RESULTS
# ======================

if st.session_state.analyzed:

    st.divider()

    st.header("Uploaded Company Documents")

    st.write(
        f"Total Documents: "
        f"{st.session_state.document_count}"
    )

    for doc in st.session_state.document_names:
        st.write(f"✓ {doc}")

    st.divider()

    st.header("Combined Company Documents")

    st.text(
        st.session_state.company_text[:1000]
    )

    st.header("Compliance Rules")

    st.text(
        st.session_state.rules_text[:1000]
    )

    st.header("Generated Audit Prompt")

    st.text_area(
        "Copy this prompt into ChatGPT",
        value=st.session_state.audit_prompt,
        height=400,
        key="prompt_box"
    )

    st.info(
        "Copy the prompt into ChatGPT, "
        "obtain the audit report, "
        "and paste it below."
    )

    audit_result = st.text_area(
        "Paste ChatGPT Audit Result",
        height=400,
        key="audit_box"
    )

    # ======================
    # PARSE AUDIT
    # ======================

    if audit_result:

        parsed = parse_report(audit_result)

        st.divider()

        st.header("Compliance Dashboard")

        metrics = extract_metrics(parsed)

        col1, col2 = st.columns(2)

        with col1:

            coverage_df = coverage_dataframe(metrics)

            fig = px.pie(
                coverage_df,
                values="Count",
                names="Status",
                title="Compliance Coverage")

            st.plotly_chart(
                fig,
                use_container_width = True)

        with col2:

            risk_df = risk_dataframe(
            parsed.get("risk", ""))

            fig = px.bar(
                risk_df,
                x="Risk",
                y="Count",
                title="Risk Distribution")

            st.plotly_chart(
                fig,
                use_container_width=True)
            

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Compliance Score",parsed.get("score","N/A"))

        with c2:
            st.metric("Found Controls",metrics["found"])

        with c3:
            st.metric("Missing Controls",metrics["missing"])

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Compliance Score")
            st.metric(
                "Score",
                parsed.get("score", "N/A")
            )

        with col2:
            st.subheader("Risk Level")
            st.metric(
                "Risk",
                parsed.get("risk", "N/A")
            )

        st.subheader("Executive Summary")
        st.write(
            parsed.get("summary", "Not Found")
        )

        st.subheader("Found Controls")
        st.write(
            parsed.get("found", "Not Found")
        )

        st.subheader("Missing Controls")
        st.write(
            parsed.get("missing", "Not Found")
        )

        st.subheader("Evidence")
        st.write(
            parsed.get("evidence", "Not Found")
        )

        st.subheader("Recommendations")
        st.write(
            parsed.get(
                "recommendations",
                "Not Found"
            )
        )

        st.download_button(
            label="Download Audit Report",
            data=audit_result,
            file_name="audit_report.txt",
            mime="text/plain"
        )