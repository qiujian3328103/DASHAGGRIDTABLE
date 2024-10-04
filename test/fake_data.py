import pandas as pd
import numpy as np 
import random 
df = pd.read_csv('test_yield_data.csv', index_col=False)

df['value'] = random.choices(range(1, 100), k=len(df))

# Group by 'date' and 'group_col' and calculate the mean of the 'value' column
grouped_df = df.groupby(['date', 'group_col'], as_index=False)['value'].mean()

# Create a MultiIndex of all unique combinations of 'date' and 'group_col'
all_combinations = pd.MultiIndex.from_product(
    [df['date'].unique(), df['group_col'].unique()],
    names=['date', 'group_col']
)

# Reindex the grouped DataFrame to include all combinations and fill missing values with 0
full_df = grouped_df.set_index(['date', 'group_col']).reindex(all_combinations, fill_value=0).reset_index()

print(full_df)

