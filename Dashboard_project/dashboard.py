import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load CSV (make sure filename matches!)
df = pd.read_csv("data/food_cities.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Food Places Dashboard (Iloilo City)"),

    html.Label("Filter by Food Type:"),
    dcc.Dropdown(
        id="type-dropdown",
        options=[{"label": t, "value": t} for t in df["Type"].unique()],
        value=df["Type"].unique().tolist(),
        multi=True
    ),

    html.Label("Filter by City:"),
    dcc.Dropdown(
        id="city-dropdown",
        options=[{"label": c, "value": c} for c in df["City"].unique()],
        value=df["City"].unique().tolist(),
        multi=True
    ),

    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="pie-chart"),
    dcc.Graph(id="scatter-chart")
])

@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("scatter-chart", "figure"),
    Input("type-dropdown", "value"),
    Input("city-dropdown", "value")
)
def update_graphs(selected_types, selected_cities):
    filtered_df = df[
        (df["Type"].isin(selected_types)) &
        (df["City"].isin(selected_cities))
    ]

    bar_fig = px.bar(filtered_df, x="Place", y="Reviews", color="Type")
    pie_fig = px.pie(filtered_df, names="Type")
    scatter_fig = px.scatter(filtered_df, x="Price_Range", y="Rating",
                             size="Reviews", color="Type")

    return bar_fig, pie_fig, scatter_fig

if __name__ == "__main__":
    app.run(debug=True)