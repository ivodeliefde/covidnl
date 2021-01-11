# Covid NL dashboard.
import datetime
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from .server import server, cache, df, df_total, municipalities
from .figures import (
    create_figure_total_sum,
    create_figure_total_abs,
    create_figure_total_perc,
)


# Initialise the app
app = dash.Dash(
    title="Covid-19 NL",
    name="Covid-19 NL",
    external_stylesheets=[
        dbc.themes.JOURNAL,
        "https://covidnldash.herokuapp.com/styles/style.css",
        # "http://localhost:5000/styles/style.css",
    ],
    assets_folder="static",
    # sharing=True,
    server=server,
    url_base_pathname="/",
)

# Define the app
app.layout = html.Div(
    children=[
        html.Div(
            className="row text-white bg-primary header",
            children=[
                html.Div(
                    className="col-xl",
                    children=[html.H2("Covid-19 in the Netherlands")],
                )
            ],
        ),
        html.Div(
            className="row jumbotron bg-light",
            children=[
                html.Div(
                    className="col-xl-3 datatable",
                    children=[
                        dash_table.DataTable(
                            id="totals_table",
                            style_as_list_view=True,
                            columns=[{"name": i, "id": i} for i in [" ", "Totals"]],
                            data=[
                                {
                                    " ": "Reported cases",
                                    "Totals": df["Total_reported"].sum(),
                                },
                                {
                                    " ": "Hospital admissions",
                                    "Totals": df["Hospital_admission"].sum(),
                                },
                                {
                                    " ": "Deceased",
                                    "Totals": df["Deceased"].sum(),
                                },
                                {
                                    " ": "Data since",
                                    "Totals": df["Date_of_publication"]
                                    .min()
                                    .strftime("%d-%m-%Y"),
                                },
                                {
                                    " ": "Data up to",
                                    "Totals": df["Date_of_publication"]
                                    .max()
                                    .strftime("%d-%m-%Y"),
                                },
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="col-xl-9",
                    children=[
                        dcc.Graph(
                            id="total_figure",
                            config={"displayModeBar": False},
                            animate=False,
                            figure=create_figure_total_sum(df_total),
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row jumbotron bg-light",
            children=[
                html.Div(
                    className="col-xl-2",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.H4("Select a Date."),
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date",
                                    date=df["Date_of_publication"].max(),
                                    min_date_allowed=df["Date_of_publication"].min(),
                                    max_date_allowed=df["Date_of_publication"].max(),
                                    display_format="D-M-Y",
                                )
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.H4("Select a Statistic."),
                            ],
                        ),
                        html.Div(
                            className="row columns",
                            children=[
                                dcc.RadioItems(
                                    id="statistic",
                                    options=[
                                        {
                                            "label": "Reported Cases",
                                            "value": "Total_reported",
                                        },
                                        {
                                            "label": "Hospital Admissions",
                                            "value": "Hospital_admission",
                                        },
                                        {
                                            "label": "Deceased",
                                            "value": "Deceased",
                                        },
                                    ],
                                    value="Total_reported",
                                    labelStyle={"display": "block"},
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="col-xl-5",
                    children=[
                        dcc.Graph(
                            id="choropleth_abs",
                            figure=create_figure_total_abs(df),
                        )
                    ],
                ),
                html.Div(
                    className="col-xl-5",
                    children=[
                        dcc.Graph(
                            id="choropleth_perc",
                            figure=create_figure_total_perc(df),
                        )
                    ],
                ),
            ],
        ),
    ],
)


# Callbacks
# Line graph with total values
@app.callback(Output("total_figure", "figure"), [Input("statistic", "value")])
@cache.memoize()
def display_total_figure(column):

    fig_total = create_figure_total_sum(df_total, column)

    return fig_total


# Map with absolute values
@app.callback(
    Output("choropleth_abs", "figure"),
    [Input("date", "date"), Input("statistic", "value")],
)
@cache.memoize()
def display_choropleth_abs(dto, column):
    dt = dto.split("T")[0]

    fig_map_abs = create_figure_total_abs(df, dt, column)

    return fig_map_abs


# Map with values relative to the population
@app.callback(
    Output("choropleth_perc", "figure"),
    [Input("date", "date"), Input("statistic", "value")],
)
@cache.memoize()
def display_choropleth_perc(dto, column):
    dt = dto.split("T")[0]

    fig_map_perc = create_figure_total_perc(df, dt, column)

    return fig_map_perc


def main(**kwargs):
    app.run_server(debug=False)


# Run the app
if __name__ == "__main__":
    main()
