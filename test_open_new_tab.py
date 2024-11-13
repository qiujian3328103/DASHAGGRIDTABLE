import dash_ag_grid as dag
from dash import Dash, html, dcc
import pandas as pd

data = {
    "ticker": ["AAPL", "MSFT", "AMZN", "GOOGL"],
    "company": ["Apple", "Microsoft", "Amazon", "Alphabet"],
    "quantity": [75, 40, 100, 50],
}
df = pd.DataFrame(data)

columnDefs = [
    {
        "headerName": "Stock Ticker",
        "field": "company",
        # Custom cellRenderer function to display company name but use ticker for the link
        "cellRenderer": "StockLink",
    },
    {
        "headerName": "Company",
        "field": "company",
    },
    {
        "headerName": "Shares",
        "field": "quantity",
        "editable": True,
    },
]

grid = dag.AgGrid(
    id="simple-column-example-1",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
)

app = Dash(__name__)

app.layout = html.Div([dcc.Markdown("Display Company Name, Link to Ticker"), grid])

if __name__ == "__main__":
    app.run(debug=True)
