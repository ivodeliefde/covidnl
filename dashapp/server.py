# server.py

from os.path import join, dirname, realpath
import json
import pandas as pd
from flask import Flask, send_file
from flask_caching import Cache

server = Flask(__name__, static_folder=join(dirname(realpath(__file__)), "static"))
cache = Cache(
    server,
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": join(dirname(realpath(__file__)), "tmp"),
    },
)
server.config.suppress_callback_exceptions = True

timeout = 300

# Load data
df = pd.read_csv(
    r"https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
)
# df = pd.read_csv(
#     r"C:\Users\IvodeLiefdeTensing\Downloads\COVID-19_aantallen_gemeente_per_dag (1).csv",
#     sep=";",
# )
df["Date_of_publication"] = pd.to_datetime(df["Date_of_publication"])

# CBS population data
pop = pd.read_csv(
    join(server.static_folder, "data", "Regionale_kerncijfers_Nederland_2020.csv"),
    sep=";",
)

df = pd.merge(df, pop, how="left", left_on="Municipality_name", right_on="Regio's")
df["Total_reported_per_100000"] = (
    df["Total_reported"]
    / df["Bevolking/Bevolkingssamenstelling op 1 januari/Totale bevolking (aantal)"]
    * 100000
).fillna(0)
df["Deceased_per_100000"] = (
    df["Deceased"]
    / df["Bevolking/Bevolkingssamenstelling op 1 januari/Totale bevolking (aantal)"]
    * 100000
).fillna(0)
df["Hospital_admission_per_100000"] = (
    df["Hospital_admission"]
    / df["Bevolking/Bevolkingssamenstelling op 1 januari/Totale bevolking (aantal)"]
    * 100000
).fillna(0)


df_total = (
    df.groupby(["Date_of_publication"])[
        [
            "Date_of_publication",
            "Total_reported",
            "Total_reported_per_100000",
            "Hospital_admission",
            "Hospital_admission_per_100000",
            "Deceased",
            "Deceased_per_100000",
        ]
    ]
    .sum()
    .reset_index()
)

df_total["Total_reported_week"] = df_total["Total_reported"].rolling(7).mean()
df_total["Hospital_admission_week"] = df_total["Hospital_admission"].rolling(7).mean()
df_total["Deceased_week"] = df_total["Deceased"].rolling(7).mean()

with open(
    join(server.static_folder, "data", "municipalities_simplified_2.geojson")
) as f:
    municipalities = json.load(f)


@server.route("/styles/style.css")
def send_css():
    filepath = join(server.static_folder, "styles", "style.css")
    return send_file(filepath, attachment_filename="style.css")

@server.route("/js/covid19nl.js")
def send_js():
    filepath = join(server.static_folder, "js", "covid19nl.js")
    return send_file(filepath, attachment_filename="covid19nl.js")

@server.route("/js/zepto.min.js")
def send_zepto():
    filepath = join(server.static_folder, "js", "zepto.min.js")
    return send_file(filepath, attachment_filename="zepto.min.js")

