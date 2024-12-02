import json
import time
from docx import Document
import re
import markdown
from html2docx import html2docx
import markdown
from docx import Document
from bs4 import BeautifulSoup


class ConvertGsscData:
    jsonData = None
    ret = ""
    output_file = "article.docx"

    def __init__(self):
        _path = "REQUETES/application_1.json"
        try:
            self.jsonData = self.check_pdf_field(_path)
            self.extractData()
        except FileNotFoundError:
            print(f"The file {_path} was not found!")

    def extractData(self):
        added_titles = set()
        for i in self.jsonData[2]["data"]:
            if i["appName"] not in added_titles:
                added_titles.add(i["appName"])
                self.filter_and_sort_by_appname(i["appName"])
        html_content = markdown.markdown(self.ret)
        self.convertToHtmlContent(html_content)

        self.convertToDoc(html_content, self.output_file)

    def check_pdf_field(self, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def remove_characters(self, text):
        return re.sub(r"#.*\n", "\n", text)

    # Extract relevant data (appName, nom, contenu)
    def filter_and_sort_by_appname(self, app_name):
        extracted_data = []
        for entry in self.jsonData[2]["data"]:
            if entry["appName"] == app_name:
                extracted_data.append(
                    {
                        "appName": entry["appName"],
                        "nom": entry["nom"],
                        "contenu": entry["contenu"],
                    }
                )

        # Sort the filtered data by 'nom'
        sorted_data = sorted(extracted_data, key=lambda x: x["nom"])

        # Display the sorted data
        for item in sorted_data:
            self.ret += (
                f"\n#{item['appName']}" f"\n#{item['nom']}" f"\n{item['contenu']}"
            )

    def remove_invalid_xml_chars(self, s):
        return re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]", "", s)

    # Function to convert Markdown to DOCX
    def convertToDoc(self, markdown_content, output_file):
        html_content = markdown.markdown(markdown_content)

        soup = BeautifulSoup(html_content, "html.parser")

        doc = Document()

        for element in soup.children:
            if element.name == "h1":
                # Convert <h1> to Heading level 1 in Word
                doc.add_heading(element.get_text(), 0)
            elif element.name == "h2":
                # Convert <h2> to Heading level 2 in Word
                doc.add_heading(element.get_text(), level=2)
            elif element.name == "h3":
                # Convert <h3> to Heading level 3 in Word
                doc.add_heading(element.get_text(), level=3)
            elif element.name == "p":
                # Convert <p> to a paragraph in Word
                doc.add_paragraph(element.get_text())
            elif element.name == "ul":
                # Convert <ul> (unordered list) to a Word list
                for li in element.find_all("li"):
                    doc.add_paragraph(f"- {li.get_text()}", style="List Bullet")
            elif element.name == "ol":
                # Convert <ol> (ordered list) to a Word list
                for li in element.find_all("li"):
                    doc.add_paragraph(f"{li.get_text()}", style="List Number")
            elif element.name == "a":
                # Handle links
                text = element.get_text()
                link = element.get("href")
                doc.add_paragraph(
                    f"{text} ({link})"
                )  # In this case, just add a plain link

        doc.save(output_file)

    # Wrap the HTML content in basic HTML structure
    def convertToHtmlContent(self, html_content):
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
        with open("html_article.html", "w", encoding="utf-8") as f:
            f.write(html_page)
        print("Markdown has been converted to an HTML page: article_01.html")


ConvertGsscData()
