import datetime
import plotly.express as px

from .server import municipalities

# Define the plots
def add_marker(fig, date, text, xshift=0, yshift=0, bgcolor="#EBFCFF", y=2000):
    fig.add_vline(x=date, line_dash="dashdot")
    fig.add_annotation(
        x=date,
        y=y,
        text=text,
        showarrow=False,
        xshift=xshift,
        yshift=yshift,
        bgcolor=bgcolor,
    )


def create_figure_total_sum(df_total, column="Total_reported", key="Reported Cases"):

    fig_total = px.line(
        df_total,
        x="Date_of_publication",
        y=column,
    )

    fig_total.update_layout(
        xaxis_range=[
            "2020-01-01",
            datetime.datetime.now() + datetime.timedelta(days=25),
        ],
        yaxis_range=[df_total[column].max() * -0.1, df_total[column].max() * 1.15],
    )
    fig_total.add_scatter(
        x=df_total["Date_of_publication"],
        y=df_total[f"{column}_week"],
        mode="lines",
        opacity=0.7,
        name="Weekly Average",
    )

    y = 2000
    extra_y_shift = 0
    if column == "Hospital_admission":
        y = 200
        extra_y_shift = 40
    elif column == "Deceased":
        y = 200
        extra_y_shift = 5

    add_marker(fig_total, "2020-01-23", "First<br>Case EU", yshift=-30, y=y)
    add_marker(fig_total, "2020-02-27", "First<br>Case NL", yshift=5, y=y)
    add_marker(
        fig_total,
        "2020-04-23",
        "Intelligent<br>Lockdown",
        yshift=45 + extra_y_shift,
        y=y,
    )
    add_marker(fig_total, "2020-06-01", "Relaxing<br>Lockdown<br>Measures", y=y)
    add_marker(
        fig_total, "2020-10-14", "Partial<br>Lockdown", yshift=-30 + extra_y_shift, y=y
    )
    add_marker(fig_total, "2020-12-14", "Strict<br>Lockdown", y=y)
    add_marker(
        fig_total,
        "2021-01-05",
        "Start<br>Vaccination<br>Campaign",
        xshift=10,
        yshift=50,
        y=y,
    )

    fig_total.update_layout(
        title=f"Development of {key.lower()} since Feb 27, 2020",
        xaxis_title="Date",
        yaxis_title=column.replace("_", " "),
    )

    return fig_total


def create_figure_total_abs(df, dt=None, column="Total_reported"):
    if dt is None:
        dt = df["Date_of_publication"].max()
    elif isinstance(dt, str):
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d")

    max_range = 101
    steps = 20
    if column == "Deceased":
        max_range = 6
        steps = 1
    elif column == "Hospital_admission":
        max_range = 21
        steps = 5

    fig_map_abs = px.choropleth_mapbox(
        df.loc[df["Date_of_publication"] == dt, :],
        geojson=municipalities,
        locations="Municipality_name",
        featureidkey="properties.gemeentenaam",
        color=column,
        color_continuous_scale="Viridis",
        range_color=(0, max_range - 1),
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 52.1561, "lon": 5.3878},
        opacity=0.5,
        labels={"Number of cases": column},
        title=f'{column.replace("_"," ")} on {dt.strftime("%B %d, %Y")}',
    )

    fig_map_abs.update_layout(margin={"r": 0, "t": 35, "l": 0, "b": 0})

    fig_map_abs.layout.coloraxis.colorbar.title = ""
    fig_map_abs.layout.coloraxis.colorbar.tickvals = [
        i for i in range(0, max_range, steps)
    ]
    fig_map_abs.layout.coloraxis.colorbar.ticktext = [
        f">{x}"
        if i == len(fig_map_abs.layout.coloraxis.colorbar.tickvals) - 1
        else f"{x}"
        for i, x in enumerate(range(0, max_range, steps))
    ]

    return fig_map_abs


# print(df["Date_of_publication"], df["Date_of_publication"].max(), df["Date_of_publication"] == df["Date_of_publication"].max())
def create_figure_total_perc(df, dt=None, column="Total_reported"):
    if dt is None:
        dt = df["Date_of_publication"].max()
    elif isinstance(dt, str):
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d")

    max_range = 101
    steps = 20
    if column == "Deceased":
        max_range = 6
        steps = 1
    elif column == "Hospital_admission":
        max_range = 21
        steps = 5

    fig_map_perc = px.choropleth_mapbox(
        df.loc[df["Date_of_publication"] == dt, :],
        geojson=municipalities,
        locations="Municipality_name",
        featureidkey="properties.gemeentenaam",
        color=f"{column}_per_100000",
        color_continuous_scale="Viridis",
        range_color=(0, max_range - 1),
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 52.1561, "lon": 5.3878},
        opacity=0.5,
        labels={"Number of cases": f"{column}_per_100000"},
        title=f'{column.replace("_"," ")} per 100.000 inhabitants on {dt.strftime("%B %d, %Y")}',
    )

    fig_map_perc.update_layout(margin={"r": 0, "t": 35, "l": 0, "b": 0})

    fig_map_perc.layout.coloraxis.colorbar.title = ""
    fig_map_perc.layout.coloraxis.colorbar.tickvals = [
        i for i in range(0, max_range, steps)
    ]
    fig_map_perc.layout.coloraxis.colorbar.ticktext = [
        f">{x}"
        if i == len(fig_map_perc.layout.coloraxis.colorbar.tickvals) - 1
        else f"{x}"
        for i, x in enumerate(range(0, max_range, steps))
    ]

    return fig_map_perc
