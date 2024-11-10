import pandas as pd 
# from config import TEST_WAFER_MAP_SAMPLE_DATA

def create_wafer_data_for_plotly(root_lot_id):
    """similar to create_wafer_data, but more suitable for plotly plot data strcuture

    Args:
        root_lot_id (_type_): _description_
    """
    TEST_WAFER_MAP_SAMPLE_DATA = r'/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/sample_wafermap_data.csv'
    df_raw = pd.read_csv(TEST_WAFER_MAP_SAMPLE_DATA, index_col=False)
    
    # filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001
    
    df['x0'] = df['ucs_die_origin_x']*0.001 - width/2
    df['x1'] = df['ucs_die_origin_x']*0.001 + width/2
    df['y0'] = df['ucs_die_origin_y'] *0.001 - height/2
    df['y1'] = df['ucs_die_origin_y']*0.001 + height/2
    
    df["color"] = "green"
    
    return df[['x0', 'x1', 'y0', 'y1', 'color', 'bin_value', 'sort_die_x', 'sort_die_y']]

def create_wafer_data(root_lot_id):
    print('pass')
    TEST_WAFER_MAP_SAMPLE_DATA = r'/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/sample_wafermap_data.csv'
    df_raw = pd.read_csv(TEST_WAFER_MAP_SAMPLE_DATA, index_col=False)
    
    # Filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001

    df['left'] = df['ucs_die_origin_x']*0.001 
    df['right'] = df['ucs_die_origin_x']*0.001
    df['bottom'] = df['ucs_die_origin_y'] *0.001
    df['top'] = df['ucs_die_origin_y']*0.001
    # Setting the width and height
    
    df["shot_bottom"] = df["ucs_die_y"]
    df["shot_left"] = df["ucs_die_x"]
    # shot_width = 5
    # shot_height = 12

    # Map the ucs_die_origin_x and ucs_die_origin_y to x and y, and set color
    df["color"] = "green"
    
    # Generate a list of dictionaries to match the format needed for D3.js
    single_wafer_data = df.apply(lambda row: {
        "x": row["left"],
        "y": row["bottom"],
        "color": row["color"],
        "bin_value": row["bin_value"],
        "mouseover": f"Die_X: {int(row['sort_die_x'])}\nDie_Y: {int(row['sort_die_y'])}"
    }, axis=1).tolist()
    

    # print(df)
    # # Generate a list of dictionaries to match the format needed for D3.js
    single_shot_data = df.apply(lambda row: {
        "x": row["shot_left"],
        "y": row["shot_bottom"],
        "color": row["color"],
    }, axis=1).tolist()
    
    wafer_data = single_wafer_data
    shot_data = single_shot_data
    

    return wafer_data, shot_data, width, height
    
# if __name__ == "__main__":
#     wafer_data, shot_data, width, height = create_wafer_data("ABCDEF")
#     print(wafer_data)
    