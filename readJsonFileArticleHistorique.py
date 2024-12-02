import json
import time
from docx import Document
import re
import markdown
from html2docx import html2docx


def check_pdf_field(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


# Example usage
pdf_path = "articleHistorique.json"
jsonData = check_pdf_field(pdf_path)
data_2 = jsonData[2]
ret = ""
for i in jsonData[2]["data"]:
    ret += f"\nNom: {i['nom']}" f"Contenu: {i['contenu']}"

print(ret)
# Save as doc


def remove_invalid_xml_chars(s):
    # Remove control characters (except newlines, tabs)
    return re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]", "", s)


cleaned_ret = remove_invalid_xml_chars(ret)
doc = Document()
doc.add_paragraph(cleaned_ret)
# Save the document
doc.save("articleHistorique.docx")


# Convert Markdown to HTML
html_content = markdown.markdown(ret)

# Wrap the HTML content in basic HTML structure
html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML Page</title>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Save the HTML content to a file
with open("articleHistorique.html", "w", encoding="utf-8") as f:
    f.write(html_page)

print("Markdown has been converted to an HTML page: output.html")
time.sleep(1)
print("Converting html to DOC...")
docx_file_path = "articleHistorique.docx"
with open(docx_file_path, "wb") as f:
    html2docx(html_page, f)

print(f"HTML has been converted to {docx_file_path}")
