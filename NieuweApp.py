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
import folium
import geopandas as gpd
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
from branca.colormap import linear
import streamlit as st
from streamlit_folium import st_folium  # Zorg ervoor dat deze module is geïnstalleerd
import statsmodels.api as sm
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from branca.colormap import linear
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import linregress

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

import requests
import pandas as pd

df1 = pd.read_csv("Schiphol.csv")

# Toon alle kolommen
pd.set_option('display.max_columns', None)

# Toon alle rijen (indien gewenst)
pd.set_option('display.max_rows', None)

df1['route.destinations'] = df1['route.destinations'].astype(str).str.replace(r"[\[\]']", "", regex=True)

# Zet de kolommen om naar datetime
df1['actualLandingTime'] = pd.to_datetime(df1['actualLandingTime'], errors='coerce')
df1['scheduleDateTime'] = pd.to_datetime(df1['scheduleDateTime'], errors='coerce')

# Bereken het tijdsverschil tussen actualLandingTime en estimatedLandingTime
df1['landingDelay'] = df1['actualLandingTime'] - df1['scheduleDateTime']

# Zet het tijdsverschil om naar seconden
df1['landingDelay'] = df1['landingDelay'].dt.total_seconds()

import pandas as pd

# Samenvoegen van de dataframes op de kolom 'IATA'
df_merged = df1.merge(df, right_on="IATA", left_on= "route.destinations", how="left")

types_filtered = pd.read_csv("type.csv", delimiter=";")
types_filtered = types_filtered[['IATA type code', 'Aantal']]

# Dataframes samenvoegen op de overeenkomstige kolommen
df_merged = df_merged.merge(
    types_filtered[['IATA type code', 'Aantal']],  # Selecteer relevante kolommen
    left_on='aircraftType.iataSub',               # Kolom in df_merged
    right_on='IATA type code',                    # Kolom in types_filtered
    how='left'                                    # 'left' om originele df_merged te behouden
)

# Stel dat df_merged de DataFrame is en actualLandingTime een datetime kolom is.
df_merged['actualLandingTime'] = pd.to_datetime(df_merged['actualLandingTime'])

# Voeg de nieuwe kolom toe waarin de tijden naar beneden worden afgerond naar het dichtstbijzijnde 15 minuten interval
df_merged['actualLandingTime_15m'] = df_merged['actualLandingTime'].dt.floor('15T')





pagina = st.sidebar.radio("Selecteer een pagina", ['Inleiding', 'Drukte per pier', 'Vertraging per pier', 'Correlatie'])
if pagina == 'Inleiding':
    st.title("Is er een verband tussen de drukte en de vertraging per pier?")
    st.write('1. Wat is de drukte per pier?')
    st.write('2. Wat is de vertraging per pier?')
    st.write('3. In welke mate bestaat er een correlatie tussen de drukte en de vertraging per pier?')

    coo_schip = [52.3105, 4.7683]

    # Maak een folium kaart
    map = folium.Map(location=coo_schip, zoom_start=2)

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
    ).add_to(map)

    # Voeg de colormap toe aan de kaart
    colormap.caption = "Drukte per land"
    colormap.add_to(map)

    # Voeg de laagcontrole toe
    folium.LayerControl().add_to(map)

    # Toon de kaart in Streamlit
    st_folium(map, width=725, height=500)



elif pagina == 'Drukte per pier':
    # Coördinaten voor Schiphol
    st.title('Wat is de drukte per pier?')

    # Functie voor het genereren van een interactieve kaart
    def generate_map(df_merged, gdf):
        # Maak een folium kaart aan
        m = folium.Map(location=[52.307949, 4.761694], zoom_start=15)

        # Bereken het aantal per pier
        pier_counts = df_merged.groupby('pier')['Aantal'].sum().to_dict()

        # Normaliseer de drukte voor kleurgebruik
        max_value = max(pier_counts.values()) if pier_counts else 1
        colormap = linear.YlOrRd_09.scale(0, max_value)

        # Functie om een kleur te geven per land
        def get_color(pier):
            value = pier_counts.get(pier, 0)
            if value == 0:
                return 'gray'  # Grijs als de waarde 0 is
            return colormap(value)

        # GeoJSON-laag toevoegen aan de kaart met kleuren op basis van 'pier_counts'
        geojson_layer = folium.GeoJson(
            gdf,
            style_function=lambda feature: {
                'fillColor': get_color(feature['properties']['name']),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['name'], 
                aliases=['Pier:'],
                sticky=True
            ),
            popup=folium.GeoJsonPopup(fields=['name'], labels=True)  # Popup voor de naam van de pier
        ).add_to(m)

        return m

    # Laad de geoJSON gegevens voor de pieren
    gdf = gpd.read_file("pier.geojson")  # Zorg ervoor dat je het juiste bestand hebt

    # Genereer de kaart
    m = generate_map(df_merged, gdf)

    # Toon de folium kaart in Streamlit
    folium_static(m)




    # Dropdownmenu voor het selecteren van een pier, met de optie "Alle piers"
    pier_options = ['Alle piers', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    selected_pier = st.selectbox("Selecteer een Pier:", pier_options)

    # Filter de dataframe op basis van de geselecteerde pier
    if selected_pier == 'Alle piers':
        filtered_df = df_merged  # Gebruik alle piers
    else:
        filtered_df = df_merged[df_merged['pier'] == selected_pier]  # Filter op de geselecteerde pier

    # Aantal passagiers per 15 minuten voor de geselecteerde pier(s)
    df_grouped = filtered_df.groupby('actualLandingTime_15m', as_index=False)['Aantal'].sum()

    # Aantal vluchten per 15 minuten voor de geselecteerde pier(s)
    df_counts = filtered_df.groupby('actualLandingTime_15m', as_index=False).size()

    # Verkrijg de tijdstippen van alle piers (voor een consistente x-as)
    all_times = df_merged['actualLandingTime_15m'].unique()
    all_times = sorted(all_times)

    # Zorg ervoor dat beide dataframes de volledige lijst van tijdstippen bevatten
    df_grouped = df_grouped.set_index('actualLandingTime_15m').reindex(all_times, fill_value=0).reset_index()
    df_grouped.columns = ['actualLandingTime_15m', 'Aantal']

    df_counts = df_counts.set_index('actualLandingTime_15m').reindex(all_times, fill_value=0).reset_index()
    df_counts.columns = ['actualLandingTime_15m', 'size']

    # Definieer de kleuren voor de lijnen en staven
    line_color = 'blue'  # Kleur voor de passagierslijn
    bar_color = 'orange'  # Kleur voor de vluchtenstaven

    import numpy as np

    # Zorg ervoor dat actualLandingTime_15m een datetime-type is
    df_merged['actualLandingTime_15m'] = pd.to_datetime(df_merged['actualLandingTime_15m'])

    # Genereer een volledige reeks kwartiertijden tussen het minimum en maximum
    all_times = pd.date_range(start=df_merged['actualLandingTime_15m'].min(), 
                            end=df_merged['actualLandingTime_15m'].max(), 
                            freq='15T')

    # Zet het om naar een dataframe om te mergen
    all_times_df = pd.DataFrame({'actualLandingTime_15m': all_times})

    # Merge met de bestaande gegevens om ontbrekende kwartieren toe te voegen
    df_grouped = all_times_df.merge(df_grouped, on='actualLandingTime_15m', how='left').fillna(0)
    df_counts = all_times_df.merge(df_counts, on='actualLandingTime_15m', how='left').fillna(0)



    # Maak de grafiek opnieuw met de gefilterde gegevens
    fig = go.Figure()

    # Voeg de lijnplot toe voor passagiersaantallen
    fig.add_trace(go.Scatter(
        x=df_grouped['actualLandingTime_15m'],
        y=df_grouped['Aantal'],
        mode='lines+markers',
        name='Aantal passagiers',
        yaxis='y1',
        line=dict(color=line_color),  # Kleur van de lijn
        marker=dict(color=line_color),
        hovertemplate='Datum:%{x}<br>Aantal:%{y}'  # Kleur van de marker
    ))

    # Voeg de staafdiagram toe voor het aantal vluchten
    fig.add_trace(go.Bar(
        x=df_counts['actualLandingTime_15m'],
        y=df_counts['size'],
        name='Aantal vluchten',
        yaxis='y2',
        opacity=0.6,
        marker=dict(color=bar_color),
        hovertemplate='Datum:%{x}<br>Aantal:%{y}'
    ))

    # Layout-instellingen met dubbele y-as en gekleurde asmarkeringen
    fig.update_layout(
        title=f'Aantal passagiers en aantal vluchten per 15 minuten voor {selected_pier}',
        xaxis=dict(
            title='Tijd',
            tickangle=45,  # Draai de x-asmarkeringen om overlapping te voorkomen
        ),
        yaxis=dict(
            title='Aantal passagiers',
            side='left',
            showgrid=True,
            tickfont=dict(color=line_color),  # Kleur van de y-as markeringen
            title_font=dict(color=line_color),  # Kleur van de y-as titel
            linecolor=line_color  # Kleur van de y-as lijn
        ),
        yaxis2=dict(
            title='Aantal vluchten',
            side='right',
            overlaying='y',
            showgrid=True,
            tickfont=dict(color=bar_color),  # Kleur van de tweede y-as markeringen
            title_font=dict(color=bar_color),  # Kleur van de tweede y-as titel
            linecolor=bar_color  # Kleur van de tweede y-as lijn
        ),
        barmode='group',
        template="plotly_white"
    )

    # Toon de grafiek
    st.plotly_chart(fig)


    # Merge de gegevens op 'actualLandingTime_15m'
    merged_data = pd.merge(df_grouped, df_counts, on='actualLandingTime_15m')

    # Bereken de lineaire regressie
    slope, intercept, r_value, p_value, std_err = linregress(merged_data['size'], merged_data['Aantal'])



    fig1 = go.Figure()

    # Voeg de scatterplot toe
    fig1.add_trace(go.Scatter(
        x=merged_data['size'],
        y=merged_data['Aantal'],
        mode='markers',
        name='Aantal vluchten vs Aantal passagiers',
        hovertemplate='<b>Aantal vluchten:</b> %{x}<br>' +
                    '<b>Aantal passagiers:</b> %{y}<br>' +
                    '<b>r-waarde:</b> ' + f'{r_value:.2f}'  # Voeg r_value toe aan de hovertekst
    ))

    # Voeg de regressielijn toe
    fig1.add_trace(go.Scatter(
        x=merged_data['size'],
        y=slope * merged_data['size'] + intercept,
        mode='lines',
        name=f'Regressielijn',
        line=dict(color='red', dash='dash'),
        hoverinfo='none'  # Geen hover-informatie voor de lijn zelf
    ))

    # Layout-instellingen
    fig1.update_layout(
        title='Aantal vluchten vs Aantal passagiers per 15 minuten',
        xaxis=dict(title='Aantal vluchten'),
        yaxis=dict(title='Aantal passagiers'),
        template="plotly_white"
    )

    # Toon de grafiek in Streamlit
    st.plotly_chart(fig1)




elif pagina == 'Vertraging per pier':
    st.title("Wat is de vertraging per pier?")
    df3 = pd.read_csv("Schipholdata2.csv")
    df3['actualOffBlockTime'] = pd.to_datetime(df3['actualOffBlockTime'])
    df3['actualOffBlockTime_15m'] = df3['actualOffBlockTime'].dt.floor('15T')
    df3['actualOffBlockTime_15m_time'] = df3['actualOffBlockTime_15m'].dt.strftime('%H:%M')
    df3['actualOffBlockTime_15m'] = pd.to_datetime(df3['actualOffBlockTime_15m'])



    # Maak een figuur met 1 rij en 2 kolommen voor de grafieken
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))  # Pas de grootte van de figuur aan

    # Plot de eerste grafiek
    ax1.hist(df3['landingDelay'], bins=150)
    ax1.set_title("Vertraging aankomsten")
    ax1.set_xlabel("Vertraging in minuten")
    ax1.set_ylabel("Frequentie")

    # Plot de tweede grafiek
    ax2.hist(df3['vertrekDelay'], bins=150)
    ax2.set_title("Vertraging vertrekken")
    ax2.set_xlabel("Vertraging in minuten")
    ax2.set_ylabel("Frequentie")

    # Toon de grafieken in Streamlit
    st.pyplot(fig)


    # Dictionary van pieren
    pieren = {"A-Pier": "A", "B-Pier": "B", "C-Pier": "C", "D-Pier": "D", 
            "E-Pier": "E", "F-Pier": "F", "G-Pier": "G", "H-Pier": "H"}

    # Streamlit-app
    st.title("vertrek Delay per Pier")

    # Keuzemenu
    selected_pier = st.selectbox("Selecteer een pier:", ["Alle"] + list(pieren.keys()))

    # Plotly figuur
    fig4 = go.Figure()

    if selected_pier == "Alle":
        for pier_name, pier_code in pieren.items():
            subset = df3[df3['pier'] == pier_code]['vertrekDelay']
            fig4.add_trace(go.Histogram(x=subset, name=pier_name))
    else:
        pier_code = pieren[selected_pier]
        subset = df3[df3['pier'] == pier_code]['vertrekDelay']
        fig4.add_trace(go.Histogram(x=subset, name=selected_pier))

    # Layout instellen
    fig4.update_layout(
        title=f"Vertraging voor {selected_pier}",
        xaxis_title="Landing Delay (minuten)",
        yaxis_title="Frequentie",
        barmode="overlay"
    )

    # Toon figuur in Streamlit
    st.plotly_chart(fig4)


    # Stel je voor dat df3 al is geladen en je hebt alle eerdere stappen uitgevoerd


    # Dropdown menu in Streamlit om de keuze voor de pier te maken
    pier_keuze = st.selectbox('Kies een pier', ['Alle piers', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

    # Filter de data op basis van de selectie
    if pier_keuze != 'Alle piers':
        df_filtered = df3[df3['pier'] == pier_keuze]
    else:
        df_filtered = df3  # Als 'Alle piers' is geselecteerd, toon dan alles

    # Bereken het gemiddelde van vertrekvertragingen per tijdsinterval (15 minuten)
    df_avg = df_filtered.groupby('actualOffBlockTime_15m').agg({'vertrekDelay': 'mean'}).reset_index()

    # Scatterplot maken van vertrekvertragingen voor alle 15-minuten intervallen
    fig2 = px.scatter(df_filtered, 
                    x='actualOffBlockTime_15m', 
                    y='vertrekDelay',
                    color='pier',  # Hier wordt 'pier' gebruikt als hue (kleur)
                    title='Vertrekvertragingen van Vluchten door de Tijd',
                    labels={'actualOffBlockTime_15m': 'Tijd van Aankomst',
                            'vertrekDelay': 'Vertrekvertraging (minuten)', 
                            'pier': 'Pier'},
                    color_continuous_scale='Viridis')  

    # Voeg de lijn toe voor het gemiddelde van vertrekvertraging per tijdsinterval
    fig2.add_scatter(x=df_avg['actualOffBlockTime_15m'], 
                    y=df_avg['vertrekDelay'], 
                    mode='lines', 
                    name='Gemiddelde Vertrekvertraging',
                    line=dict(color='red', width=2))

    # Stel de X-as in van 5:30 tot 9:30
    fig2.update_xaxes(
        tickangle=45,
        tickmode='linear',  # Zorg dat de X-as lineair is
        range=[pd.Timestamp("2025-04-03 05:00:00"), pd.Timestamp("2025-04-03 10:00:00")],  # Gebruik pd.Timestamp voor de range
        tickformat="%H:%M"   # Formatteer de tijd in uren:minuten
    )

    # Verhoog de grootte van de plot voor betere leesbaarheid
    fig2.update_layout(
        width=1000,  # Verhoog de breedte van de plot
        height=600   # Verhoog de hoogte van de plot
    )

    # Toon de plot
    st.plotly_chart(fig2)

elif pagina == 'Correlatie':
    st.title("In welke mate bestaat er een correlatie tussen de drukte en de vertraging per pier?")

