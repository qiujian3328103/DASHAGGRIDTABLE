import dash_ag_grid as dag
from dash import Dash, html

# Define column definitions for the AgGrid table, including a column for images
columnDefs = [
    {
        "headerName": "Stock Ticker",
        "field": "ticker",
    },
    {
        "headerName": "Company",
        "field": "company",
    },
    {
        "headerName": "Last Close Price",
        "field": "price",
        "valueFormatter": {"function": """d3.format("($,.2f")(params.value)"""},
    },
    {
        "headerName": "Logo",
        "field": "logo",
        "cellRenderer": "LogoRenderer",  # Custom cell renderer for images
        "autoHeight": True  # Ensure proper height for images
    }
]

# Sample data to populate the AgGrid, including image URLs for logos
data = [
    {"ticker": "AAPL", "company": "Apple Inc.", "price": 150.75, "logo": "https://logo.clearbit.com/apple.com"},
    {"ticker": "GOOGL", "company": "Alphabet Inc.", "price": 2750.0, "logo": "https://logo.clearbit.com/google.com"},
    {"ticker": "MSFT", "company": "Microsoft Corp.", "price": 300.65, "logo": "https://logo.clearbit.com/microsoft.com"}
]

# Create the AgGrid component
grid = dag.AgGrid(
    id="custom-loading-overlay",
    columnDefs=columnDefs,
    rowData=data,  # Initially populate the grid with data
    columnSize="sizeToFit",
)

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        html.H3("Ag-Grid with Images"),
        grid,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
