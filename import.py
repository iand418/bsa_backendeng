import pandas as pd
import sqlite3

# Create a database connection
conn = sqlite3.connect('database.db')

# Read the CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Create a table in the database and insert the data
df.to_sql('bookings', conn, index=False)

# Close the database connection
conn.close()