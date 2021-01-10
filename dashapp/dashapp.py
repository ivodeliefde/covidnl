# Covid NL dashboard.
import datetime
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from .server import df, municipalities

from .server import server, cache, df, df_total


def add_marker(fig, date, text, xshift=0, yshift=0, bgcolor="#EBFCFF"):
    fig.add_vline(x=date, line_dash="dashdot")
    fig.add_annotation(
        x=date,
        y=2000,
        text=text,
        showarrow=False,
        # yshift=500,
        xshift=xshift,
        yshift=yshift,
        bgcolor=bgcolor,
    )


fig_total = px.line(
    df_total,
    x="Date_of_publication",
    y="Total_reported",
)
fig_total.update_layout(
    xaxis_range=["2020-01-01", datetime.datetime.now() + datetime.timedelta(days=25)]
)
add_marker(fig_total, "2020-01-23", "First<br>Case EU", yshift=-30)
add_marker(fig_total, "2020-02-27", "First<br>Case NL", yshift=5)
add_marker(fig_total, "2020-04-23", "Intelligent<br>Lockdown", yshift=45)
add_marker(fig_total, "2020-06-01", "Relaxing<br>Lockdown<br>Measures")
add_marker(fig_total, "2020-10-14", "Partial<br>Lockdown", yshift=-30)
add_marker(fig_total, "2020-12-14", "Strict<br>Lockdown")
add_marker(
    fig_total, "2021-01-05", "Start<br>Vaccination<br>Campaign", xshift=10, yshift=50
)
fig_total.add_scatter(x=df_total['Date_of_publication'],
                      y=df_total['Total_reported_week'],
                      mode='lines',
                      opacity=0.7,
                      name="Weekly Average")

fig_map_abs = px.choropleth_mapbox(
    df.loc[df["Date_of_publication"] == df["Date_of_publication"].max(), :],
    geojson=municipalities,
    locations="Municipality_name",
    featureidkey="properties.gemeentenaam",
    color= "Total_reported",
    color_continuous_scale="Viridis",
    range_color=(0, 100),
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": 52.1561, "lon": 5.3878},
    opacity=0.5,
    labels={"Number of cases": "Total_reported"},
    title=f'Total reported on {df["Date_of_publication"].max().strftime("%d-%m-%Y")}'
)

fig_map_abs.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0})

# print(df["Date_of_publication"], df["Date_of_publication"].max(), df["Date_of_publication"] == df["Date_of_publication"].max())

fig_map_perc = px.choropleth_mapbox(
        df.loc[df["Date_of_publication"] == df["Date_of_publication"].max(), :],
        geojson=municipalities,
        locations="Municipality_name",
        featureidkey="properties.gemeentenaam",
        color="Total_reported_per_100000",
        color_continuous_scale="Viridis",
        range_color=(0, 100),
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 52.1561, "lon": 5.3878},
        opacity=0.5,
        labels={"Number of cases": "Total_reported_per_100000"},
        title=f'Total reported per 100000 on {df["Date_of_publication"].max().strftime("%d-%m-%Y")}'
    )

fig_map_perc.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )



# Initialise the app
app = dash.Dash(
    external_stylesheets=[
        dbc.themes.JOURNAL,
        "https://covidnldash.herokuapp.com/styles/style.css",
        # "http://localhost:5000/styles/style.css",
    ],
    assets_folder="static",
    name="Covid-19 NL",
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
                                    " ": "Data up to",
                                    "Totals": df["Date_of_publication"].max(),
                                },
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="col-xl-9",
                    children=[
                        dcc.Graph(
                            id="total_cases",
                            config={"displayModeBar": False},
                            animate=True,
                            figure=fig_total,
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
                    ],
                ),
                html.Div(
                    className="col-xl-5",
                    children=[
                        dcc.Graph(
                            id="choropleth_abs",
                            figure=fig_map_abs,
                        )
                    ],
                ),
                html.Div(
                    className="col-xl-5",
                    children=[
                        dcc.Graph(
                            id="choropleth_perc",
                            figure=fig_map_perc,
                        )
                    ],
                ),
            ],
        ),
    ]
)


# Callbacks
@app.callback(Output("choropleth_abs", "figure"), [Input("date", "date")])
@cache.memoize(
    # timeout=timeout   # in seconds
)
def display_choropleth(dto):
    dt = dto.split("T")[0]

    fig_map_abs = px.choropleth_mapbox(
        df.loc[df["Date_of_publication"] == dt, :],
        geojson=municipalities,
        locations="Municipality_name",
        featureidkey="properties.gemeentenaam",
        color="Total_reported",
        color_continuous_scale="Viridis",
        range_color=(0, 100),
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 52.1561, "lon": 5.3878},
        opacity=0.5,
        # labels={"Number of cases": "Total_reported"},
        title=f'Total reported on {df["Date_of_publication"].max().strftime("%d-%m-%Y")}'

    )

    fig_map_abs.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    fig_map_abs.layout.coloraxis.colorbar.title = ""

    return fig_map_abs


# Callbacks
@app.callback(Output("choropleth_perc", "figure"), [Input("date", "date")])
@cache.memoize(
    # timeout=timeout   # in seconds
)
def display_choropleth_perc(dto):
    dt = dto.split("T")[0]
    fig_map_perc = px.choropleth_mapbox(
        df.loc[df["Date_of_publication"] == dt, :],
        geojson=municipalities,
        locations="Municipality_name",
        featureidkey="properties.gemeentenaam",
        color="Total_reported_per_100000",
        color_continuous_scale="Viridis",
        range_color=(0, 100),
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 52.1561, "lon": 5.3878},
        opacity=0.5,
        # labels={"Number of cases": "Total_reported_per_100000"},
        title=f'Total reported per 100000 on {df["Date_of_publication"].max().strftime("%d-%m-%Y")}'
    )

    fig_map_perc.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    fig_map_perc.layout.coloraxis.colorbar.title = ""

    return fig_map_perc


def main(**kwargs):
    app.run_server(debug=False)


# Run the app
if __name__ == "__main__":
    main()
