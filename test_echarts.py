import json
import random
import dash
import feffery_antd_components as fac
from dash import dcc, html, Input, Output, ClientsideFunction
from pyecharts.charts import Bar, Scatter
from pyecharts import options as opts
import pandas as pd 
from dash import no_update
# Read and process the CSV data
def read_and_process_csv_perato():
    # Read the CSV file using pandas (assumes the CSV is in the same directory)
    df = pd.read_csv("/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/test_yield_data.csv")  # Replace with your actual CSV file path
    
    # needs to proccess the data to plot. 
    # Group by 'date' and 'group_col' and calculate the mean of the 'value' column
    grouped_df = df.groupby(['date', 'group_col'], as_index=False)['value'].mean()

    # Create a MultiIndex of all unique combinations of 'date' and 'group_col'
    all_combinations = pd.MultiIndex.from_product(
        [df['date'].unique(), df['group_col'].unique()],
        names=['date', 'group_col']
    )

    # Reindex the grouped DataFrame to include all combinations and fill missing values with 0
    output_df = grouped_df.set_index(['date', 'group_col']).reindex(all_combinations, fill_value=0).reset_index()
    
    # Pivot the data to reshape it for easier plotting
    pivot_df = output_df.pivot(index='date', columns='group_col', values='value').fillna(0)
    print(pivot_df)
    
    
    # Calculate total sum for each group_col across all dates and sort by this sum
    total_sums = pivot_df.sum(axis=0).sort_values(ascending=False)

    # Sort the pivoted DataFrame columns based on the sum
    pivot_df = pivot_df[total_sums.index]

    # Convert the reshaped DataFrame into a dictionary for plotting
    grouped_dict = pivot_df.to_dict(orient='index')

    return pivot_df, grouped_dict


# Define a function to return ECharts options using the processed CSV data
def perato_echarts_options():
    # Read and process the CSV file to get grouped data
    grouped_df, grouped_dict = read_and_process_csv_perato()
    
    # Create a bar chart using pyecharts
    bar = Bar()

    # Set X-axis as unique 'group' values
    bar.add_xaxis(list(grouped_df.index))

    # Add series data for each unique 'time' (week)
    for time, values in grouped_dict.items():
        # values.items() contains ('group_name', average_value) pairs
        bar.add_yaxis(str(time), list(values.values()))

    # Set chart options including the toolbox
    bar.set_global_opts(
        # title_opts=opts.TitleOpts(title="Average Values by Group and Date (Sorted)"),
        xaxis_opts=opts.AxisOpts(name="Group", axislabel_opts={"rotate": 30}),
        yaxis_opts=opts.AxisOpts(name="Average Value"),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        toolbox_opts=opts.ToolboxOpts(is_show=True, feature={
            "saveAsImage": {},  # Enables save as image option
            "dataZoom": {},     # Enables zooming feature
            "restore": {},      # Restore to the initial view
            "magicType": {"type": ["line", "bar"]}  # Switch between bar and line chart
        })
    )

    # Return the ECharts options in JSON format
    return json.loads(bar.dump_options_with_quotes())


app = dash.Dash(
    __name__,
    # external_scripts=['https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js']
)

app.layout = html.Div(
    [
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdSegmented(
                                id = 'segmented',
                                options=[
                                    {'label': i, 'value': i}
                                    for i in ['Bar', 'Scatter', 'Line', 'CDF','Perato', 'Boxplot']
                                ],
                                defaultValue='Bar',
                            ),
                        html.Div(
                            id='echarts-container',
                            style={
                                'width': '500px',
                                'height': '500px'
                            }
                        ),   
                    ],
                    flex='none',
                    style={'height': 'fit-content'},
                ),
            ],
            gutter=10,
            justify='center',
            align='middle',
            style={
                'width': '100%',
                'height': 600,
                'borderRadius': 6,
                'border': '1px solid #40a9ff',
            },
        ),

        dcc.Store(
            id='data-store'
        )
    ]
)

@app.callback(
    Output('data-store', 'data'),
    Input('segmented', 'value')
)
def get_echarts_options(segemented_value):
    if segemented_value == 'Bar':
        return perato_echarts_options()
    else:
        return no_update

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside_charts',
        function_name='render_charts'
    ),
    Output('echarts-container', 'children'),
    Input('data-store', 'data')
)

if __name__ == "__main__":
    app.run(debug=True)