import pandas as pd


def extract_metrics(parsed):

    found_controls = len(
        parsed.get(
            "found",
            ""
        ).split("\n")
    )

    missing_controls = len(
        parsed.get(
            "missing",
            ""
        ).split("\n")
    )

    return {
        "found": found_controls,
        "missing": missing_controls
    }


def coverage_dataframe(metrics):

    return pd.DataFrame({
        "Status": [
            "Found",
            "Missing"
        ],
        "Count": [
            metrics["found"],
            metrics["missing"]
        ]
    })


def risk_dataframe(risk):

    if "HIGH" in risk.upper():

        return pd.DataFrame({
            "Risk": [
                "High",
                "Medium",
                "Low"
            ],
            "Count": [
                7,
                3,
                1
            ]
        })

    elif "MEDIUM" in risk.upper():

        return pd.DataFrame({
            "Risk": [
                "High",
                "Medium",
                "Low"
            ],
            "Count": [
                2,
                6,
                4
            ]
        })

    return pd.DataFrame({
        "Risk": [
            "High",
            "Medium",
            "Low"
        ],
        "Count": [
            1,
            2,
            8
        ]
    })