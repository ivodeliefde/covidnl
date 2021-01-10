import datetime
import plotly.express as px

from .server import df, df_total, municipalities

# Define the plots

fig_total = px.line(
    df_total,
    x="Date_of_publication",
    y="Total_reported",
)
fig_total.update_layout(
    xaxis_range=["2020-01-01", datetime.datetime.now() + datetime.timedelta(days=25)]
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