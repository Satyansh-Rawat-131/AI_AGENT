import fitz

def extract_pdf_text(uploaded_file):

    """
    Returns:
        {
            "name" = "<filename>"
            "pages" =
            [
                {
                    "page" = 1,
                    "text" = "..."
                },
            ...
            ]
        }
    """

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )
    pages = []

    text = ""

    for page_num , page  in enumerate (pdf , start = 1):
        text += page.get_text()
        pages.append({
            "page" : page_num,
            "text" : text
        })

    pdf.close()

    return {
        "name" : uploaded_file.name , "pages" : pages
    }