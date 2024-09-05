import sqlite3 

url = "/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/test_database.db"

# Connect to the SQLite3 database (or create it if it doesn't exist)
conn = sqlite3.connect(url)
cursor = conn.cursor()

# Create a new table called 'status_table' if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS status_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL
    )
''')

# Insert status values if the table is empty
cursor.execute('SELECT COUNT(*) FROM status_table')
row_count = cursor.fetchone()[0]

if row_count == 0:
    status_values = [("Open",), ("Close",), ("KIV",), ("New",)]
    cursor.executemany('INSERT INTO status_table (status) VALUES (?)', status_values)
    conn.commit()

# Close the database connection
conn.close()

print('pass')

# Reconnect to the SQLite3 database
conn = sqlite3.connect(url)
cursor = conn.cursor()

# Create a new table called 'pgm_process_table' with the same structure as 'status_table'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pgm_process_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pgm_process TEXT NOT NULL
    )
''')

# Insert process options into the pgm_process_table if it's empty
cursor.execute('SELECT COUNT(*) FROM pgm_process_table')
row_count = cursor.fetchone()[0]

if row_count == 0:
    pgm_process_values = [("Test",), ("Process",), ("Equipment",), ("Device",), ("TBD",)]
    cursor.executemany('INSERT INTO pgm_process_table (pgm_process) VALUES (?)', pgm_process_values)
    conn.commit()

# Close the connection
conn.close()

# Reconnect to the SQLite3 database
conn = sqlite3.connect(url)
cursor = conn.cursor()

# Create a new table called 'fit_status_table' with the same structure as the other tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fit_status_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fit_status TEXT NOT NULL
    )
''')

# Insert fit status options into the fit_status_table if it's empty
cursor.execute('SELECT COUNT(*) FROM fit_status_table')
row_count = cursor.fetchone()[0]

if row_count == 0:
    fit_status_values = [("Open",), ("Closed",)]
    cursor.executemany('INSERT INTO fit_status_table (fit_status) VALUES (?)', fit_status_values)
    conn.commit()

# Close the connection
conn.close()


# Reconnect to the SQLite3 database
conn = sqlite3.connect(url)
cursor = conn.cursor()

# # Create a new table called 'fit_status_table' with the same structure as the other tables
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         fit_status TEXT NOT NULL
#     )
# ''')

# # Insert fit status options into the fit_status_table if it's empty
# cursor.execute('SELECT COUNT(*) FROM users_table')
# row_count = cursor.fetchone()[0]

# if row_count == 0:
#     users = [("Open",), ("Closed",), ("A",), ("B",), ("C",), ("D",), ("E",), ("F",), ("G",), ("H",), ("I",), ("J",)]
#     cursor.executemany('INSERT INTO users_table (users) VALUES (?)', users)
#     conn.commit()

# # Close the connection
# conn.close()

