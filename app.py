import streamlit as st

from services.parser import extract_pdf_text
from services.prompt_builder import build_prompt
from services.report_parser import parse_report


st.set_page_config(
    page_title="ComplianceMind v0.1",
    layout="wide"
)

st.title("ComplianceMind v0.1")
st.subheader("AI-Powered Compliance Auditor")


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


# ======================
# FILE UPLOAD
# ======================

company = st.file_uploader(
    "Upload Company Documents",
    type="pdf"
)

rules = st.file_uploader(
    "Upload Compliance Rules",
    type="pdf"
)


# ======================
# ANALYZE BUTTON
# ======================

if st.button("Analyze"):

    if company and rules:

        st.session_state.company_text = (
            extract_pdf_text(company)
        )

        st.session_state.rules_text = (
            extract_pdf_text(rules)
        )

        st.session_state.audit_prompt = (
            build_prompt(
                st.session_state.company_text,
                st.session_state.rules_text
            )
        )

        st.session_state.analyzed = True

    else:
        st.error(
            "Please upload both files."
        )


# ======================
# DISPLAY RESULTS
# ======================

if st.session_state.analyzed:

    st.divider()

    st.header("Company Document")

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
        "Paste the prompt into ChatGPT, "
        "copy the audit report, "
        "then paste it below."
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

        parsed = parse_report(
            audit_result
        )

        st.divider()

        st.header(
            "Compliance Dashboard"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(
                "Compliance Score"
            )
            st.metric(
                "Score",
                parsed["score"]
            )

        with col2:
            st.subheader(
                "Risk Level"
            )
            st.metric(
                "Risk",
                parsed["risk"]
            )

        st.subheader(
            "Executive Summary"
        )
        st.write(
            parsed["summary"]
        )

        st.subheader(
            "Found Controls"
        )
        st.write(
            parsed["found"]
        )

        st.subheader(
            "Missing Controls"
        )
        st.write(
            parsed["missing"]
        )

        st.subheader(
            "Evidence"
        )
        st.write(
            parsed["evidence"]
        )

        st.subheader(
            "Recommendations"
        )
        st.write(
            parsed["recommendations"]
        )

        st.download_button(
            label="Download Audit Report",
            data=audit_result,
            file_name="audit_report.txt",
            mime="text/plain"
        )