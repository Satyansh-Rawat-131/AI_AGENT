def combine_documents(documents):

    combined = ""

    for name, text in documents.items():

        combined += (
            f"\n"
            f"==============================\n"
            f"DOCUMENT: {name}\n"
            f"==============================\n\n"
        )

        combined += text
        combined += "\n\n"

    return combined