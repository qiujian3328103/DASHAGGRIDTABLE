import sqlite3
import base64
def insert_data_to_db(sba_date, eval_date, product, bin_value, sba_cnt, hit_rate, sba_avg, sba_limit, status):
    """Function to insert data into SQLite database

    Args:
        sba_date (_type_): _description_
        eval_date (_type_): _description_
        product (_type_): _description_
        bin_value (_type_): _description_
        sba_cnt (_type_): _description_
        hit_rate (_type_): _description_
        sba_avg (_type_): _description_
        sba_limit (_type_): _description_
        status (_type_): _description_
    """
    conn = sqlite3.connect(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\DashAggridTable\test\test_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO sbl_table (sba_date, eval_date, product, bin, sba_cnt, hit_rate, sba_avg, sba_limit, status, pgm_process, comment, action_item, assigned_team, action_owner, pe_owner, fit, fit_status, follow_up, last_update, foreigner_key)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sba_date, eval_date, product, bin_value, sba_cnt, hit_rate, sba_avg, sba_limit, status, '', '', '', '', '', '', '', '', '', '', ''))

    conn.commit()
    conn.close()


def query_row_by_id(row_id):
    """Function to query a specific row from the SQLite database by ID."""
    conn = sqlite3.connect(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\DashAggridTable\test\test_database.db')
    cursor = conn.cursor()

    # Fetch the specific row from sbl_table based on the provided ID
    cursor.execute('''
        SELECT id, sba_date, eval_date, product, bin, sba_cnt, hit_rate, sba_avg, sba_limit, status, pgm_process, comment, action_item, assigned_team, action_owner, pe_owner, fit, fit_status, follow_up, last_update, foreigner_key
        FROM sbl_table
        WHERE id = ?
    ''', (row_id,))
    
    row = cursor.fetchone()

    if row:
        # Fetch map images for the foreigner_key
        cursor.execute('SELECT map_image FROM map_image WHERE foreigner_key = ?', (row[20],))
        map_images = cursor.fetchall()
        map_image_b64 = [base64.b64encode(img[0]).decode('utf-8') for img in map_images]

        # Fetch trend images for the foreigner_key
        cursor.execute('SELECT trend_image FROM trend_image WHERE foreigner_key = ?', (row[20],))
        trend_images = cursor.fetchall()
        trend_image_b64 = [base64.b64encode(img[0]).decode('utf-8') for img in trend_images]

        # Convert the data to a dictionary format
        row_data = {
            "Id": row[0],
            "SBA Date": row[1],
            "Eval Date": row[2],
            "Product": row[3],
            "Bin": row[4],
            "SBA CNT": row[5],
            "Hit Rate": row[6],
            "SBA Avg": row[7],
            "SBA Limit": row[8],
            "Status": row[9],
            "PGM/Process": row[10],
            "Comment": row[11],
            "Action Item": row[12],
            "Assigned Team": row[13],
            "Action Owner": row[14],
            "PE Owner": row[15],
            "FIT": row[16],
            "FIT Status": row[17],
            "Follow Up": row[18],
            "Last Update": row[19],
            "Map Images": map_image_b64,
            "Trend Images": trend_image_b64,
        }

        conn.close()
        return row_data
    else:
        conn.close()
        return None
