import streamlit as st

from services.parser import extract_pdf_text
from services.prompt_builder import build_prompt


st.title("ComplianceMind v0")
st.subheader("AI-Powered SOC2 Compliance Auditor")


# Upload company document
company = st.file_uploader(
    "Upload Company Documents",
    type="pdf"
)

# Upload SOC2 rules
rules = st.file_uploader(
    "Upload SOC2 Rules",
    type="pdf"
)


if st.button("Analyze"):

    if company and rules:

        # Extract text from PDFs
        company_text = extract_pdf_text(company)
        rules_text = extract_pdf_text(rules)

        # Build audit prompt
        audit_prompt = build_prompt(
            company_text,
            rules_text
        )

        # Display extracted company document
        st.write("## === COMPANY DOCUMENT ===")
        st.text(company_text[:1000])

        # Display extracted SOC2 rules
        st.write("## === COMPLIANCE RULES ===")
        st.text(rules_text[:1000])

        # Display generated prompt
        st.write("## Generated Audit Prompt")

        st.text_area(
            label="Copy this prompt and paste it into ChatGPT/Grok",
            value=audit_prompt,
            height=500
        )

        st.info("Copy the prompt above and paste it into ChatGPT to generate the compliance audit report.")

    else:
        st.error(
            "Please upload both the company document and SOC2 rules."
        )