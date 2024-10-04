import pandas as pd
from pyecharts.charts import Scatter
from pyecharts import options as opts

# Create the DataFrame with dynamic date values
data = {
    'root_lot_id': ['lot_1'] * 29,
    'wafer_id': ['W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W07', 'W08', 'W09', 'W10', 'W11', 'W12', 'W13', 'W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W07', 'W08', 'W09', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16'],
    'process_id': ['process1'] * 29,
    'step_seq': ['EDS_LOGIC'] * 29,
    'value': [80.1, 80.2, 79.2, 69.1, 58.1, 21.4, 89, 83, 84, 87, 89, 70, 78, 1.2, 1.3, 1.4, 1.2, 1.3, 1.4, 1.2, 2.1, 2.4, 2.5, 2.6, 2.8, 2.9, 3.2, 5.4, 2.1],
    'category': ['pgm1'] * 29,
    'date': ['WW33', 'WW33', 'WW33', 'WW33', 'WW33', 'WW34', 'WW34', 'WW34', 'WW34', 'WW34', 'WW35', 'WW35', 'WW35', 'WW33', 'WW33', 'WW33', 'WW33', 'WW33', 'WW34', 'WW34', 'WW34', 'WW34', 'WW34', 'WW35', 'WW35', 'WW35', 'WW35', 'WW35', 'WW35'],
    'group_col': ['YIELD'] * 13 + ['IDDQ'] * 16
}

df = pd.DataFrame(data)

# Create a mapping of unique dates to sequential x-axis values
unique_dates = df['date'].unique()
date_mapping = {date: idx for idx, date in enumerate(unique_dates)}

# Map the `date` column to the new x values
df['x_value'] = df['date'].map(date_mapping)

# Create a scatter plot using pyecharts
scatter = Scatter()

# Set the x-axis values using the sequential numeric values
scatter.add_xaxis(df['x_value'].tolist())

# Add scatter points for each group_col category
for group_name, group_df in df.groupby('group_col'):
    filter_df = df[df['group_col'] == group_name]
    scatter.add_yaxis(
        series_name=group_name,
        y_axis=filter_df['value'].tolist(),
        label_opts=opts.LabelOpts(is_show=False)
    )

# Configure global options
scatter.set_global_opts(
    title_opts=opts.TitleOpts(title="Scatter Plot with Dynamic Date Mapping"),
    xaxis_opts=opts.AxisOpts(
        type_='value',
        name="Date",
        min_=-0.5,
        max_=len(unique_dates) - 0.5,  # Range based on number of unique dates
        interval=1,
        axislabel_opts=opts.LabelOpts(formatter=lambda x: unique_dates[int(x)] if x >= 0 and x < len(unique_dates) else "")
    ),
    yaxis_opts=opts.AxisOpts(name="Value"),
    legend_opts=opts.LegendOpts(is_show=True)
)

# Render the scatter plot
scatter.render("vertical_scatter_plot.html")
