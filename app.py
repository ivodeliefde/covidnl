# Covid NL dashboard.

import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# Load data
df = pd.read_csv(
    r"https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
)
# df = pd.read_csv(r"C:\Users\IvodeLiefdeTensing\Downloads\COVID-19_aantallen_gemeente_per_dag.csv", sep=";")
df["Date_of_publication"] = pd.to_datetime(df["Date_of_publication"])
df_province = (
    df.groupby(["Date_of_publication", "Province"])[
        ["Date_of_publication", "Total_reported"]
    ]
    .sum()
    .reset_index()
)

# Initialise the app
app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])

print(df.head().to_dict("records"))

# Define the app
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(className="col-md", children=[html.H2("Covid NL dashboard")])
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-md-3 Light left",
                    children=[
                        dash_table.DataTable(
                            id="totals",
                            columns=[{"name": i, "id": i} for i in [" ", "Totals"]],
                            data=[
                                {
                                    " ": "Number of cases",
                                    "Totals": df["Total_reported"].sum(),
                                },
                                {
                                    " ": "Number of deceased",
                                    "Totals": df["Deceased"].sum(),
                                },
                                {
                                    " ": "Data since",
                                    "Totals": df["Date_of_publication"].min(),
                                },
                                {
                                    " ": "Latest data",
                                    "Totals": df["Date_of_publication"].max(),
                                },
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="col-md-9",
                    children=[
                        dcc.Graph(
                            id="province",
                            config={"displayModeBar": False},
                            animate=True,
                            figure=px.line(
                                df_province,
                                x="Date_of_publication",
                                y="Total_reported",
                                color="Province",
                            ),
                        )
                    ],
                ),
            ],
        ),
    ]
)

def server():
    app.run_server(debug=False)


# Run the app
if __name__ == "__main__":
    server()