# Covid NL dashboard.
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from .server import server, cache, df, df_total
from .figures import (
    create_figure_total_sum,
    create_figure_total_abs,
    create_figure_total_perc,
)
from .layout import layout


# Initialise the app
app = dash.Dash(
    title="Covid-19 NL",
    name="Covid-19 NL",
    external_stylesheets=[
        dbc.themes.JOURNAL,
        # "https://covidnldash.herokuapp.com/styles/style.css",
        "http://localhost:5000/styles/style.css",
    ],
    external_scripts=[
        "https://covidnldash.herokuapp.com/js/covid19nl.js",
    ],
    assets_folder="static",
    # sharing=True,
    server=server,
    url_base_pathname="/",
)


app.layout = layout


# Callbacks
# Line graph with total values
@app.callback(
    Output("total_figure", "figure"),
    [Input("statistic", "value"), Input("statistic", "options")],
)
@cache.memoize()
def display_total_figure(column, options):
    print(options)
    for opt in options:
        if opt["value"] == column:
            key = opt["label"]
            break

    fig_total = create_figure_total_sum(df_total, column, key)

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
