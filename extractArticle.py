import mysql.connector
import json
from datetime import datetime
from convertJsonMarkdownToDocAndHtml import ConvertGsscData


class ExtractSqlData(ConvertGsscData):
    query = None

    def __init__(self, query, **kwargs):
        self.query = query
        self.appName = kwargs.get("appName")
        super().__init__(**kwargs)

    def connectDbExtract(self):
        # Replace these values with your database information
        config = {
            "user": "root",
            "password": "",
            "host": "localhost",
            "database": "gssc",
        }

        try:
            # Establish the connection
            connection = mysql.connector.connect(**config)

            if connection.is_connected():
                print("Successfully connected to the database")

                cursor = connection.cursor()
                sql_query = self.query
                cursor.execute(sql_query)
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description]

                result = [dict(zip(columns, row)) for row in results]
                for row in result:
                    # Check if 'date_de_publication' key exists in the row and remove it
                    for key in ["date_de_publication", "derniere_modif"]:
                        row.pop(key, None)

                # Write the result to a JSON file
                output = f"{self.input_file_path}/{self.appName}.json"
                with open(output, "w", encoding="utf-8") as json_file:
                    json.dump(result, json_file, indent=4, default=str)

                print(f"Query executed successfully. Results saved to {self.appName}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the connection
            if connection:
                connection.close()

    def run(self):
        self.connectDbExtract()
        super().run()


if __name__ == "__main__":
    input_path = "json_application"
    folder_output_path = "extracted"
    try:
        # Open and read the JSON file
        with open("query/query.json", "r") as file:
            data = json.load(file)
        # Iterate over the list of apps and print the "appname" for each app
        for q in data["queries"]:
            appName = q["appName"]
            query = q["query"]
            executed = ExtractSqlData(
                query=query,
                appName=appName,
                input_file_path=input_path,
                output_file_path=folder_output_path,
            ).run()

    except FileNotFoundError:
        print("The file 'data.json' was not found.")
    except json.JSONDecodeError:
        print("There was an error decoding the JSON data.")
