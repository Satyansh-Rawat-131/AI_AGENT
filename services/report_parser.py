import re


def extract_section(text, section):

    pattern = rf"{section}\s*(.*?)(?=\n[A-Z ][A-Z ]+\n|\Z)"

    match = re.search(
        pattern,
        text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return "Not Found"


def parse_report(report):

    return {
        "summary":
            extract_section(
                report,
                "EXECUTIVE SUMMARY"
            ),

        "found":
            extract_section(
                report,
                "FOUND CONTROLS"
            ),

        "missing":
            extract_section(
                report,
                "MISSING CONTROLS"
            ),

        "score":
            extract_section(
                report,
                "COMPLIANCE SCORE"
            ),

        "risk":
            extract_section(
                report,
                "RISK LEVEL"
            ),

        "recommendations":
            extract_section(
                report,
                "RECOMMENDATIONS"
            ),
    }