def build_prompt(company_docs, soc2_rules):

    return f"""
You are a senior SOC2 compliance auditor.

Analyze the company documentation against the SOC2 controls.

Provide your response EXACTLY in the following format.

==================================================
EXECUTIVE SUMMARY
==================================================

Provide a brief assessment.

==================================================
FOUND CONTROLS
==================================================

List all controls found.

==================================================
MISSING CONTROLS
==================================================

List all controls that are missing.

==================================================
EVIDENCE
==================================================

For each found control, provide supporting evidence.

==================================================
COMPLIANCE SCORE
==================================================

Provide a score between 0 and 100.

==================================================
RISK LEVEL
==================================================

Choose one:
LOW
MEDIUM
HIGH

==================================================
RECOMMENDATIONS
==================================================

Provide specific remediation steps.

==================================================
COMPANY DOCUMENTATION
==================================================

{company_docs}

==================================================
SOC2 REQUIREMENTS
==================================================

{soc2_rules}

"""