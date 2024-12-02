import json
import time
from docx import Document
import re
import markdown
from html2docx import html2docx
import markdown
from docx import Document
from bs4 import BeautifulSoup
import os


class ConvertGsscData:
    jsonData = None
    ret = ""

    def __init__(self, inputFile_path, outputFile_path):
        print(self.getFilesList(inputFile_path))
        chunk = [i for i in (self.getFilesList(inputFile_path))]
        try:
            for file in self.getFilesList(inputFile_path):
                self.jsonData = self.check_pdf_field(f"{inputFile_path}/{file}")
                self.extractData(f"{outputFile_path}/{file.split(".")[0]}")
        except FileNotFoundError:
            print(f"The file {chunk} was not found!")

    def getFilesList(self, folder_path):
        file_list = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
        return file_list

    def extractData(self, output_file):
        added_titles = set()
        for i in self.jsonData[2]["data"]:
            if i["appName"] not in added_titles:
                added_titles.add(i["appName"])
                self.filter_and_sort_by_appname(i["appName"])
        html_content = markdown.markdown(self.ret)
        self.convertToHtmlContent(html_content, f"{output_file}.html")
        self.convertToDoc(html_content, f"{output_file}.docx")

    def extractData_54_56(self, output_file):
        added_titles = set()
        for i in self.jsonData[2]["data"]:
            if i["appName"] not in added_titles:
                added_titles.add(i["appName"])
                self.filter_and_sort_by_appname(i["appName"])
        html_content = markdown.markdown(self.ret)
        self.convertToHtmlContent(html_content, f"{output_file}.html")
        self.convertToDoc(html_content, f"{output_file}.docx")

    def check_pdf_field(self, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def remove_characters(self, text):
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)

    # Extract relevant data (appName, nom, contenu)
    def filter_and_sort_by_appname(self, app_name):
        extracted_data = []
        for entry in self.jsonData[2]["data"]:
            if entry["appName"] == app_name:
                nom = entry.get("nom", "")
                extracted_data.append(
                    {
                        "appName": entry["appName"],
                        "nom": nom,
                        "contenu": entry["contenu"],
                    }
                )
        # Sort the filtered data by 'nom'
        sorted_data = sorted(extracted_data, key=lambda x: x["nom"])

        # Display the sorted data
        for item in sorted_data:
            # encoded_string = dirty_string.encode("utf-8", "ignore")
            nom = item.get("nom", "")
            self.ret += (
                f"\n#{self.remove_characters(item['appName'])}"
                f"\n# {nom}"
                f"\n{self.remove_characters(item['contenu'])}"
            )

    def remove_invalid_xml_chars(self, s):
        return re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]", "", s)

    # Function to convert Markdown to DOCX
    def convertToDoc(self, markdown_content, output_file):
        html_content = markdown.markdown(markdown_content)

        soup = BeautifulSoup(html_content, "html.parser")

        doc = Document()

        for element in soup.children:
            try:
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
            except ReferenceError:
                print("Value error")
        print(output_file)
        doc.save(output_file)

    # Wrap the HTML content in basic HTML structure
    def convertToHtmlContent(self, html_content, output_html):
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
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_page)
        print(f"Markdown has been converted to an HTML page: {output_html}")


# End of class


input_file_1_3 = "jsonToExtract_1_3"
input_file_54_56 = "jsonToExtract_54_56"
folderOutput_path = "extracted"

ConvertGsscData(input_file_1_3, folderOutput_path)
ConvertGsscData(input_file_54_56, folderOutput_path)
