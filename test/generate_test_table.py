import sqlite3
import uuid

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Create the sbl_table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sbl_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sba_date TEXT,
        eval_date TEXT,
        product TEXT,
        bin INTEGER,
        sba_cnt INTEGER,
        hit_rate TEXT,
        sba_avg TEXT,
        sba_limit TEXT,
        status TEXT,
        pgm_process TEXT,
        comment TEXT,
        action_item TEXT,
        assigned_team TEXT,
        action_owner TEXT,
        pe_owner TEXT,
        fit TEXT,
        fit_status TEXT,
        follow_up TEXT,
        last_update TEXT,
        foreigner_key TEXT UNIQUE
    )
''')

# Create the map_image table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS map_image (
        foreigner_key TEXT,
        map_image BLOB,
        FOREIGN KEY (foreigner_key) REFERENCES sbl_table(foreigner_key)
    )
''')

# Create the trend_image table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trend_image (
        foreigner_key TEXT,
        trend_image BLOB,
        FOREIGN KEY (foreigner_key) REFERENCES sbl_table(foreigner_key)
    )
''')

# Sample data to insert into sbl_table
data = [
    ('2024-06-21', '2024-08-23', 'Electron', 5999, 27, 7.52, 0.46, 0.15, 'Open', 'Process', 'some comments', 'Needs actions', 'A', 'A', 'A', 'www.google.com', 'Open', 'some follow up', '2/1/2024'),
    ('2024-06-22', '2024-08-23', 'Waikiki', 1837, 31, 8.52, 0.52, 0.12, 'KIV', 'PGM', 'some comments', 'Needs actions', 'B', 'B', 'B', 'www.google.com', 'Closed', 'some follow up', '2/2/2024'),
    ('2024-07-23', '2024-08-24', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-24', '2024-08-25', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'PGM', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-25', '2024-08-26', 'Waikiki', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-25', '2024-08-27', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-26', '2024-08-28', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'TBD', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-27', '2024-08-29', 'Waikiki', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-28', '2024-08-30', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-29', '2024-08-31', 'Waikiki', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'write comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-30', '2024-09-01', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'PGM', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-07-31', '2024-09-22', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-21', '2024-08-23', 'Electron', 5999, 27, 7.52, 0.46, 0.15, 'Open', 'Process', 'some comments', 'Needs actions', 'A', 'A', 'A', 'www.google.com', 'Open', 'some follow up', '2/1/2024'),
    ('2024-08-22', '2024-08-23', 'Waikiki', 1837, 31, 8.52, 0.52, 0.12, 'KIV', 'PGM', 'some comments', 'Needs actions', 'B', 'B', 'B', 'www.google.com', 'Closed', 'some follow up', '2/2/2024'),
    ('2024-08-23', '2024-08-24', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-24', '2024-08-25', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'PGM', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-25', '2024-08-26', 'Electron', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-25', '2024-08-27', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-26', '2024-08-28', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'TBD', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-27', '2024-08-29', 'Waikiki', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-28', '2024-08-30', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-29', '2024-08-31', 'Hamilton', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'write comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-30', '2024-09-01', 'Cater', 4507, 51, 9.52, 0.46, 0.10, 'New', 'PGM', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024'),
    ('2024-08-31', '2024-09-22', 'Hamilton', 4507, 51, 9.52, 0.46, 0.10, 'New', 'Process', 'some comments', 'Needs actions', 'C', 'C', 'C', 'www.google.com', 'Open', 'some follow up', '2/3/2024')
]

# Insert the data into the sbl_table with a generated UUID for the foreigner_key
foreigner_keys = []
for row in data:
    foreigner_key = str(uuid.uuid4())
    foreigner_keys.append(foreigner_key)
    cursor.execute('''
        INSERT INTO sbl_table (sba_date, eval_date, product, bin, sba_cnt, hit_rate, sba_avg, sba_limit, status, pgm_process, comment, action_item, assigned_team, action_owner, pe_owner, fit, fit_status, follow_up, last_update, foreigner_key)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', row + (foreigner_key,))

# Sample image data to insert into map_image and trend_image tables
# You would normally read an image from a file in binary mode (rb) using open()
with open(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\DashAggridTable\test\map_image.JPG', 'rb') as file:
    image_data_map = file.read()

with open(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\DashAggridTable\test\trend_image.JPG', 'rb') as file:
    image_data_trend = file.read()


# Insert images into the map_image table
for key in foreigner_keys:
    cursor.execute('''
        INSERT INTO map_image (foreigner_key, map_image)
        VALUES (?, ?)
    ''', (key, image_data_map))

# Insert images into the trend_image table
for key in foreigner_keys:
    cursor.execute('''
        INSERT INTO trend_image (foreigner_key, trend_image)
        VALUES (?, ?)
    ''', (key, image_data_trend))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()


