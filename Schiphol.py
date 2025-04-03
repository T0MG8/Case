import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from branca.colormap import linear
from streamlit_folium import st_folium
import geopandas as gpd


# URL van het datasetbestand
url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

# Kolomnamen zoals gedefinieerd in de OpenFlights-dataset
columns = [
    "Airport ID", "Name", "City", "Country", "IATA", "ICAO", 
    "Latitude", "Longitude", "Altitude", "Timezone", 
    "DST", "Tz database time zone", "Type", "Source"
]

# Inlezen van het CSV-bestand
df = pd.read_csv(url, header=None, names=columns)

# ----------------------------------------------------------------------------------------------------------------------------------------------

vluchten = pd.read_csv("Schiphol.csv")

vluchten = vluchten.dropna(subset=['pier'])

# Toon alle kolommen
pd.set_option('display.max_columns', None)

# Toon alle rijen (indien gewenst)
pd.set_option('display.max_rows', None)

vluchten['route.destinations'] = vluchten['route.destinations'].astype(str).str.replace(r"[\[\]']", "", regex=True)

vluchten.rename(columns={'route.destinations': 'IATA'}, inplace=True)

# Zet de kolommen om naar datetime
vluchten['actualLandingTime'] = pd.to_datetime(vluchten['actualLandingTime'], errors='coerce')
vluchten['scheduleDateTime'] = pd.to_datetime(vluchten['scheduleDateTime'], errors='coerce')

# Bereken het tijdsverschil tussen actualLandingTime en estimatedLandingTime
vluchten['landingDelay'] = vluchten['actualLandingTime'] - vluchten['scheduleDateTime']

# Zet het tijdsverschil om naar seconden
vluchten['landingDelay'] = vluchten['landingDelay'].dt.total_seconds()

# ----------------------------------------------------------------------------------------------------------------------------------------------

df_merged = vluchten.merge(df, on="IATA", how="left")

# ----------------------------------------------------------------------------------------------------------------------------------------------

types_filtered = pd.read_csv("type.csv", delimiter=";")
types_filtered = types_filtered[['IATA type code', 'Aantal']]

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Dataframes samenvoegen op de overeenkomstige kolommen
df_merged = df_merged.merge(
    types_filtered[['IATA type code', 'Aantal']],  # Selecteer relevante kolommen
    left_on='aircraftType.iataSub',               # Kolom in df_merged
    right_on='IATA type code',                    # Kolom in types_filtered
    how='left'                                    # 'left' om originele df_merged te behouden
)


# ----------------------------------------------------------------------------------------------------------------------------------------------

# Dataframes samenvoegen op de overeenkomstige kolommen
vluchten = vluchten.merge(
    types_filtered[['IATA type code', 'Aantal']],  # Selecteer relevante kolommen
    left_on='aircraftType.iataSub',               # Kolom in df_merged
    right_on='IATA type code',                    # Kolom in types_filtered
    how='left'                                    # 'left' om originele df_merged te behouden
)

# Zorg ervoor dat 'actualLandingTime' een datetime is
vluchten['actualLandingTime'] = pd.to_datetime(vluchten['actualLandingTime'])

# Afronden naar de dichtstbijzijnde 15 minuten
vluchten['actualLandingTime_15m'] = vluchten['actualLandingTime'].dt.floor('15T')

# Groeperen per 15 minuten en passagiersaantallen optellen
vluchten_grouped = vluchten.groupby('actualLandingTime_15m', as_index=False)['Aantal'].sum()

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Aantal passagiers per 15 minuten
vluchten_grouped = vluchten.groupby('actualLandingTime_15m', as_index=False)['Aantal'].sum()

# Aantal vluchten per 15 minuten (aantal rijen tellen)
vluchten_counts = vluchten.groupby('actualLandingTime_15m', as_index=False).size()

# Maak een figuur met een dubbele y-as
fig = go.Figure()

# Voeg de lijnplot toe voor passagiersaantallen
fig.add_trace(go.Scatter(
    x=vluchten_grouped['actualLandingTime_15m'],
    y=vluchten_grouped['Aantal'],
    mode='lines+markers',
    name='Aantal passagiers',
    yaxis='y1'
))

# Voeg de staafdiagram toe voor het aantal vluchten
fig.add_trace(go.Bar(
    x=vluchten_counts['actualLandingTime_15m'],
    y=vluchten_counts['size'],
    name='Aantal vluchten',
    yaxis='y2',
    opacity=0.6
))

# Layout-instellingen met dubbele y-as
fig.update_layout(
    title='Aantal passagiers en aantal vluchten per 15 minuten',
    xaxis=dict(title='Tijd'),
    yaxis=dict(
        title='Aantal passagiers',
        side='left',
        showgrid=True
    ),
    yaxis2=dict(
        title='Aantal vluchten',
        side='right',
        overlaying='y',
        showgrid=True
    ),
    barmode='group',  # Optioneel: 'overlay' voor transparantie of 'group' voor naast elkaar
    template="plotly_white"
)

# Streamlit weergave
st.plotly_chart(fig)

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Coördinaten voor Schiphol
coo_schip = [52.3105, 4.7683]

# Maak een folium kaart
m = folium.Map(location=coo_schip, zoom_start=2)

# Laad het geoJSON bestand in een GeoDataFrame
gdf = gpd.read_file("wereldgrenzen.geojson")

# Tel het aantal rijen per land
drukte_per_land = df_merged['Country'].value_counts().to_dict()

# Normaliseer de drukte voor kleurgebruik
max_value = max(drukte_per_land.values()) if drukte_per_land else 1
colormap = linear.YlOrRd_09.scale(0, max_value)  

# Functie om een kleur te geven per land
def get_color(country):
    value = drukte_per_land.get(country, 0)
    if value == 0:
        return 'gray'  # Grijs als de waarde 0 is
    return colormap(value)

geojson_layer = folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        'fillColor': get_color(feature['properties']['COUNTRY']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['COUNTRY'], 
        aliases=['Land:'],  # Voeg een alias toe voor leesbaarheid
        localize=True,
        sticky=True
    )
).add_to(m)

# Voeg de colormap toe aan de kaart
colormap.caption = "Drukte per land"
colormap.add_to(m)

# Voeg de laagcontrole toe
folium.LayerControl().add_to(m)

folium_static(m)

# --------------------------------------------------------------------------------------------------------------------------------------------

