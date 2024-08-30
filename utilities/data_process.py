import sqlite3

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