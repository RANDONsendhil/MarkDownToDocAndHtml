import mysql.connector

# Replace these values with your database information
config = {
	'user': 'root',
	'password': '',
	'host': 'localhost',
	'database': 'gssc_articles',
}

try:
	# Establish the connection
	connection = mysql.connector.connect(**config)

	if connection.is_connected():
		print("Successfully connected to the database")

		# Create a cursor object using the cursor() method
		cursor = connection.cursor()

		# Write the SQL query to retrieve data
		sql_query = "SELECT * FROM your_table"

		# Execute the query
		cursor.execute(sql_query)

		# Fetch all rows from the executed query
		results = cursor.fetchall()

		# Iterate through the results and print them
		for row in results:
			print(row)

except mysql.connector.Error as err:
	print(f"Error: {err}")
finally:
	# Close the cursor and connection
	if 'cursor' in locals():
		cursor.close()
	if 'connection' in locals() and connection.is_connected():
		connection.close()
		print("Database connection closed.")
