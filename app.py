# Covid NL dashboard.

from datetime import datetime
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
df_total = (
    df.groupby(["Date_of_publication"])[["Date_of_publication", "Total_reported"]]
    .sum()
    .reset_index()
)

# Initialise the app
app = dash.Dash(
    external_stylesheets=[dbc.themes.JOURNAL, "style.css"],
    assets_folder = "assets"
)
server = app.server

# Define the plots
def add_marker(fig, date, text, xshift=40, yshift=0):
    fig.add_vline(x=date, line_dash="dashdot")
    fig.add_annotation(
        x=date,
        y=2000,
        text=text,
        showarrow=False,
        # yshift=500,
        xshift=xshift,
        yshift=yshift,
    )


fig_total = px.line(
    df_total,
    x="Date_of_publication",
    y="Total_reported",
)
fig_total.update_layout(xaxis_range=["2020-01-01", datetime.now()])
add_marker(fig_total, "2020-01-23", "First<br>Case EU", xshift=35)
add_marker(fig_total, "2020-02-27", "First<br>Case NL", xshift=35)
add_marker(fig_total, "2020-04-23", "Intelligent<br>Lockdown")
add_marker(fig_total, "2020-06-01", "Relaxing<br>Lockdown<br>Measures")
add_marker(fig_total, "2020-10-14", "Partial<br>Lockdown")
add_marker(fig_total, "2020-12-14", "Strict<br>Lockdown")


# Define the app
app.layout = html.Div(
    children=[
        html.Div(
            className="row text-white bg-primary",
            children=[
                html.Div(
                    className="col-md header",
                    children=[html.H2("Covid-19 in the Netherlands")],
                )
            ],
        ),
        html.Div(
            className="row jumbotron bg-light",
            children=[
                html.Div(
                    className="col-sm-6 col-md-6 col-lg-4 col-xl-3 datatable",
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
                    className="col-sm-6 col-md-6 col-lg-8 col-xl-9",
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
    ]
)


def main(**kwargs):
    app.run_server(debug=False)


# Run the app
if __name__ == "__main__":
    main()
