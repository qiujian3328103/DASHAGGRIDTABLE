import sqlite3

# Database path
DB_URL = "test_database.db"

# Connect to the database
conn = sqlite3.connect(DB_URL)
cursor = conn.cursor()

# Create the table 'product_reference' if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_reference_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        step_seq TEXT,
        process_id TEXT,
        program_name TEXT,
        last_update TEXT
    )
''')

# Insert test data into 'product_reference' table
test_data = [
    ("Product1", "step1", "process1", "program1", "2024-08-24"),
    ("Product2", "step2", "process2", "program2", "2024-08-25")
]

cursor.executemany('''
    INSERT INTO product_reference_table (product, step_seq, process_id, program_name, last_update)
    VALUES (?, ?, ?, ?, ?)
''', test_data)

# Commit changes and close the connection
conn.commit()
conn.close()