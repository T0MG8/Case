import requests
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import st_folium


GeoCoö = {
    "ATL": {"latitude": 33.6407, "longitude": -84.4277},
    "PEK": {"latitude": 40.0799, "longitude": 116.6031},
    "LAX": {"latitude": 33.9416, "longitude": -118.4085},
    "HND": {"latitude": 35.5494, "longitude": 139.7798},
    "DXB": {"latitude": 25.2532, "longitude": 55.3657},
    "ORD": {"latitude": 41.9742, "longitude": -87.9073},
    "LHR": {"latitude": 51.4700, "longitude": -0.4543},
    "PVG": {"latitude": 31.1443, "longitude": 121.8083},
    "CDG": {"latitude": 49.0097, "longitude": 2.5479},
    "DFW": {"latitude": 32.8998, "longitude": -97.0403},
    "CAN": {"latitude": 23.3925, "longitude": 113.2988},
    "AMS": {"latitude": 52.3105, "longitude": 4.7683},
    "HKG": {"latitude": 22.3080, "longitude": 113.9185},
    "ICN": {"latitude": 37.4602, "longitude": 126.4407},
    "FRA": {"latitude": 50.0379, "longitude": 8.5622},
    "DEN": {"latitude": 39.8561, "longitude": -104.6737},
    "SIN": {"latitude": 1.3644, "longitude": 103.9915},
    "DEL": {"latitude": 28.5562, "longitude": 77.1000},
    "CGK": {"latitude": -6.1256, "longitude": 106.6559},
    "BKK": {"latitude": 13.6899, "longitude": 100.7501},
    "JFK": {"latitude": 40.6413, "longitude": -73.7781},
    "KUL": {"latitude": 2.7456, "longitude": 101.7099},
    "MAD": {"latitude": 40.4983, "longitude": -3.5676},
    "SFO": {"latitude": 37.6213, "longitude": -122.3790},
    "CTU": {"latitude": 30.5785, "longitude": 103.9471},
    "SZX": {"latitude": 22.6393, "longitude": 113.8107},
    "BCN": {"latitude": 41.2974, "longitude": 2.0833},
    "IST": {"latitude": 41.2753, "longitude": 28.7519},
    "SEA": {"latitude": 47.4502, "longitude": -122.3088},
    "LAS": {"latitude": 36.0840, "longitude": -115.1537},
    "MCO": {"latitude": 28.4312, "longitude": -81.3081},
    "YYZ": {"latitude": 43.6777, "longitude": -79.6248},
    "MEX": {"latitude": 19.4361, "longitude": -99.0719},
    "CLT": {"latitude": 35.2140, "longitude": -80.9431},
    "SVO": {"latitude": 55.9726, "longitude": 37.4146},
    "TPE": {"latitude": 25.0797, "longitude": 121.2342},
    "KMG": {"latitude": 25.1019, "longitude": 102.9292},
    "MUC": {"latitude": 48.3538, "longitude": 11.7861},
    "MNL": {"latitude": 14.5086, "longitude": 121.0194},
    "XIY": {"latitude": 34.4471, "longitude": 108.7516},
    "LGW": {"latitude": 51.1537, "longitude": -0.1821},
    "EWR": {"latitude": 40.6895, "longitude": -74.1745},
    "PHX": {"latitude": 33.4342, "longitude": -112.0116},
    "MIA": {"latitude": 25.7959, "longitude": -80.2870},
    "BOM": {"latitude": 19.0896, "longitude": 72.8656},
    "SYD": {"latitude": -33.9399, "longitude": 151.1753},
    "GRU": {"latitude": -23.4356, "longitude": -46.4731},
    "FCO": {"latitude": 41.7999, "longitude": 12.2462},
    "KIX": {"latitude": 34.4347, "longitude": 135.2448},
    "BOS": {"latitude": 42.3656, "longitude": -71.0096},
    "SGN": {"latitude": 10.8189, "longitude": 106.6519},
    "MEL": {"latitude": -37.6690, "longitude": 144.8410},
    "DME": {"latitude": 55.4088, "longitude": 37.9063},
    "JED": {"latitude": 21.6796, "longitude": 39.1565},
    "FLL": {"latitude": 26.0726, "longitude": -80.1527},
    "SLC": {"latitude": 40.7899, "longitude": -111.9791},
    "MSP": {"latitude": 44.8848, "longitude": -93.2223},
    "DTW": {"latitude": 42.2124, "longitude": -83.3534},
    "BWI": {"latitude": 39.1754, "longitude": -76.6684},
    "MAN": {"latitude": 53.3650, "longitude": -2.2728},
    "DUB": {"latitude": 53.4273, "longitude": -6.2436},
    "YVR": {"latitude": 49.1947, "longitude": -123.1792},
    "PHL": {"latitude": 39.8744, "longitude": -75.2424},
    "ORY": {"latitude": 48.7262, "longitude": 2.3652},
    "CPH": {"latitude": 55.6180, "longitude": 12.6560},
    "FUK": {"latitude": 33.5859, "longitude": 130.4500},
    "KBP": {"latitude": 50.3450, "longitude": 30.8947},
    "SJU": {"latitude": 18.4394, "longitude": -66.0018},
    "GIG": {"latitude": -22.8090, "longitude": -43.2506},
    "LIM": {"latitude": -12.0219, "longitude": -77.1143},
    "HNL": {"latitude": 21.3187, "longitude": -157.9225},
    "VIE": {"latitude": 48.1103, "longitude": 16.5697},
    "WUH": {"latitude": 30.7760, "longitude": 114.2081},
    "SCL": {"latitude": -33.3930, "longitude": -70.7858},
    "BOG": {"latitude": 4.7016, "longitude": -74.1469},
    "LGA": {"latitude": 40.7769, "longitude": -73.8740},
    "FLL": {"latitude": 26.0726, "longitude": -80.1527},
    "STL": {"latitude": 38.7487, "longitude": -90.3700},
    "BNE": {"latitude": -27.3842, "longitude": 153.1175},
    "MCT": {"latitude": 23.5933, "longitude": 58.2844},
    "WAW": {"latitude": 52.1657, "longitude": 20.9671},
    "ATH": {"latitude": 37.9364, "longitude": 23.9475},
    "HEL": {"latitude": 60.3172, "longitude": 24.9633},
    "OSL": {"latitude": 60.1976, "longitude": 11.1004},
    "ARN": {"latitude": 59.6498, "longitude": 17.9238},
    "ZRH": {"latitude": 47.4581, "longitude": 8.5555},
    "MXP": {"latitude": 45.6301, "longitude": 8.7231},
    "SVO": {"latitude": 55.9726, "longitude": 37.4146},
    "LED": {"latitude": 59.8003, "longitude": 30.2625},
    "GVA": {"latitude": 46.2381, "longitude": 6.1089},
    "DUS": {"latitude": 51.2895, "longitude": 6.7668},
    "HAM": {"latitude": 53.6304, "longitude": 9.9882},
    "TXL": {"latitude": 52.5597, "longitude": 13.2877},
    "MRS": {"latitude": 43.4367, "longitude": 5.2150},
    "LYS": {"latitude": 45.7256, "longitude": 5.0811},
    "NCE": {"latitude": 43.6584, "longitude": 7.2159},
    "PMI": {"latitude": 39.5517, "longitude": 2.7388},
    "HRG": {"latitude": 27.1780, "longitude": 33.7983},  # Hurghada International
    "DXB": {"latitude": 25.2532, "longitude": 55.3657},  # Dubai International
    "TFS": {"latitude": 28.0402, "longitude": -16.5725},  # Tenerife-Sur
    "NRT": {"latitude": 35.7614, "longitude": 140.3850},  # Narita
    "LEJ": {"latitude": 51.4239, "longitude": 12.2403},  # Leipzig/Halle Airport
    "CDG": {"latitude": 49.0097, "longitude": 2.5479},  # Charles de Gaulle
    "ICN": {"latitude": 37.4602, "longitude": 126.4407},  # Incheon
    "PBM": {"latitude": 5.4448, "longitude": -55.1878},  # Johan Adolf Pengel
    "CGK": {"latitude": -6.1256, "longitude": 106.6559},  # Soekarno-Hatta Intl
    "ACC": {"latitude": 5.6050, "longitude": -0.2050},  # Kotoka Accra
    "ATL": {"latitude": 33.6407, "longitude": -84.4277},  # Hartsfield-Jackson Int
    "JFK": {"latitude": 40.6413, "longitude": -73.7781},  # John F Kennedy Intl
    "ACE": {"latitude": 28.9445, "longitude": -13.6052},  # Lanzarote
    "DTW": {"latitude": 42.2124, "longitude": -83.3534},  # Detroit Metropolitan Wayne Co.
    "LOS": {"latitude": 6.5722, "longitude": 3.3219},  # Murtala Muhammed
    "FNC": {"latitude": 32.6986, "longitude": -16.7740},  # Madeira
    "HKG": {"latitude": 22.3080, "longitude": 113.9185},  # Hongkong
    "AGP": {"latitude": 36.6749, "longitude": -4.4991},  # Malaga Airport
    "VLC": {"latitude": 39.4894, "longitude": -0.4818},  # Valencia Airport
    "OSL": {"latitude": 60.1976, "longitude": 11.1004},  # Gardermoen
    "SIN": {"latitude": 1.3644, "longitude": 103.9915},  # Changi
    "BRU": {"latitude": 50.9014, "longitude": 4.4844},  # Brussels
    "ZRH": {"latitude": 47.4581, "longitude": 8.5555},  # Zurich Airport
    "PRG": {"latitude": 50.1008, "longitude": 14.2600},  # Ruzyne
    "MSP": {"latitude": 44.8848, "longitude": -93.2223},  # Minneapolis/St Paul International
    "ALC": {"latitude": 38.2822, "longitude": -0.5585},  # Alicante Airport
    "PVG": {"latitude": 31.1443, "longitude": 121.8083},  # Pudong Sjanghai
    "FCO": {"latitude": 41.7999, "longitude": 12.2462},  # Fiumicino
    "GVA": {"latitude": 46.2381, "longitude": 6.1089},  # Geneva International
    "HAM": {"latitude": 53.6304, "longitude": 9.9882},  # Hamburg Airport
    "DUS": {"latitude": 51.2895, "longitude": 6.7668},  # Duesseldorf International
    "ARN": {"latitude": 59.6498, "longitude": 17.9238},  # Arlanda
    "LCA": {"latitude": 35.1580, "longitude": 33.9983},  # Larnaca
    "ORD": {"latitude": 41.9742, "longitude": -87.9073},  # O'Hare International
    "WAW": {"latitude": 52.1657, "longitude": 20.9671},  # Frederic Chopin
    "BCN": {"latitude": 41.2974, "longitude": 2.0833},  # Barcelona-el Prat
    "PMO": {"latitude": 38.1750, "longitude": 13.0916},  # Punta Raisi
    "CPH": {"latitude": 55.6180, "longitude": 12.6560},  # Kastrup
    "RAI": {"latitude": 16.7411, "longitude": -22.9604},  # Rabil
    "LIS": {"latitude": 38.7810, "longitude": -9.1349},  # Lisbon Airport
    "SZG": {"latitude": 47.7984, "longitude": 13.0045},  # W.A. Mozart
    "BRE": {"latitude": 53.0472, "longitude": 8.7869},  # Bremen
    "LHR": {"latitude": 51.4700, "longitude": -0.4543},  # Heathrow
    "MUC": {"latitude": 48.3538, "longitude": 11.7861},  # Muenich International
    "LIN": {"latitude": 45.4654, "longitude": 9.2740},  # Linate
    "LCY": {"latitude": 51.5074, "longitude": -0.0544},  # London City Airport
    "VIE": {"latitude": 48.1103, "longitude": 16.5697},  # Schwechat Intl
    "IAD": {"latitude": 38.9531, "longitude": -77.4565},  # Dulles Intl
    "HAJ": {"latitude": 52.4611, "longitude": 9.6853},  # Hannover Airport
    "MAD": {"latitude": 40.4983, "longitude": -3.5676},  # Adolfo Suarez-Barajas
    "RUH": {"latitude": 24.9575, "longitude": 46.6986},  # Riyad
    "YYZ": {"latitude": 43.6777, "longitude": -79.6248},  # Toronto Pearson
    "RAK": {"latitude": 31.6295, "longitude": -7.9811},  # Menara
    "NAP": {"latitude": 40.8852, "longitude": 14.2908},  # Capodichino
    "MXP": {"latitude": 45.6301, "longitude": 8.7231},  # Malpensa
    "NBO": {"latitude": -1.3192, "longitude": 36.9273},  # Jomo Kenyatta Intl
    "LUX": {"latitude": 49.6267, "longitude": 6.2111},  # Luxembourg
    "BLL": {"latitude": 55.5392, "longitude": 8.6161},  # Billund
    "EWR": {"latitude": 40.6895, "longitude": -74.1745},  # Newark Liberty Intl
    "TOS": {"latitude": 69.6833, "longitude": 18.9167},  # Tromsø
    "FRA": {"latitude": 50.0379, "longitude": 8.5622},  # Frankfurt International
    "SVQ": {"latitude": 37.4230, "longitude": -5.8934},  # Sevilla Airport
    "NUE": {"latitude": 49.4983, "longitude": 11.0780},  # Nuremberg Airport
    "DUB": {"latitude": 53.4273, "longitude": -6.2436},  # Dublin International
    "FAO": {"latitude": 37.0179, "longitude": -7.9659},  # Faro Airport
    "BER": {"latitude": 52.3667, "longitude": 13.5033},  # Brandenburg
    "AAL": {"latitude": 57.0927, "longitude": 9.8497},  # Aalborg Airport
    "BJL": {"latitude": 13.3386, "longitude": -16.6525},  # Banjul International
    "LGW": {"latitude": 51.1537, "longitude": -0.1821},  # Gatwick
    "INN": {"latitude": 47.2633, "longitude": 11.1756},  # Innsbruck Airport
    "STR": {"latitude": 48.6891, "longitude": 9.2211},  # Stuttgart Airport
    "BSL": {"latitude": 47.5982, "longitude": 7.5292},  # EuroAirport Swiss
    "MIA": {"latitude": 25.7959, "longitude": -80.2870},  # Miami International
    "SVG": {"latitude": 58.8783, "longitude": 5.6364},  # Stavanger Sola
    "GOT": {"latitude": 57.6628, "longitude": 12.2928},  # Landvetter
    "JRO": {"latitude": -3.3720, "longitude": 36.6850},  # Kilimanjaro International
    "IAH": {"latitude": 29.9844, "longitude": -95.3414},  # George Bush Intercont.
    "BGO": {"latitude": 60.2936, "longitude": 5.2181},  # Bergen Flesland
    "STN": {"latitude": 51.8892, "longitude": 0.2671},  # Stansted
    "BOM": {"latitude": 19.0896, "longitude": 72.8656},  # Chhatrapati Shivaji
    "CUR": {"latitude": 12.1740, "longitude": -68.9591},  # Hato Intl
    "NTE": {"latitude": 47.2192, "longitude": -1.6091},  # Atlantique
    "BOD": {"latitude": 44.8297, "longitude": -0.7053},  # Merignac
    "PTY": {"latitude": 9.0733, "longitude": -79.3833},  # Tocumen
    "PDX": {"latitude": 45.5887, "longitude": -122.5951},  # Portland International
    "TPE": {"latitude": 25.0797, "longitude": 121.2342},  # Taiwan Taoyuan
    "LPI": {"latitude": 58.4220, "longitude": 15.4147},  # Linkoping City Airport
    "KRS": {"latitude": 58.2214, "longitude": 8.0389},  # Kristiansand Kjevik
    "ABZ": {"latitude": 57.2012, "longitude": -2.1978},  # Dyce
    "MAN": {"latitude": 53.3650, "longitude": -2.2728},  # Manchester Airport
    "GLA": {"latitude": 55.8711, "longitude": -4.4344},  # Glasgow International
    "KRK": {"latitude": 50.0783, "longitude": 19.7844},  # John Paul II - Balice
    "OTP": {"latitude": 44.5711, "longitude": 26.0853},  # Henri Coandă
    "BOS": {"latitude": 42.3656, "longitude": -71.0096},  # Edward L. Logan Intl
    "TLS": {"latitude": 43.6292, "longitude": 1.3639},  # Blagnac
    "NWI": {"latitude": 52.6750, "longitude": 1.2783},  # Norwich International
    "EDI": {"latitude": 55.9500, "longitude": -3.3725},  # Edinburgh Airport
    "BRS": {"latitude": 51.3822, "longitude": -2.7192},  # Bristol
    "YYC": {"latitude": 51.1300, "longitude": -114.0110},  # Calgary
    "WRO": {"latitude": 51.1074, "longitude": 16.8856},  # Nicolaus Copernicus
    "MME": {"latitude": 54.5077, "longitude": -1.2611},  # Tees Valley
    "HUY": {"latitude": 53.7392, "longitude": -0.3583},  # Humberside
    "BOH": {"latitude": 50.7808, "longitude": -1.8419},  # Bournemouth International
    "NCL": {"latitude": 54.9780, "longitude": -1.6907},  # Newcastle International
    "BHX": {"latitude": 52.4527, "longitude": -1.7482},  # Birmingham Airport
    "TRN": {"latitude": 45.2001, "longitude": 7.6497},  # Caselle
    "DEL": {"latitude": 28.5562, "longitude": 77.1000},  # Indira Gandhi
    "AAR": {"latitude": 56.2925, "longitude": 10.6192},  # Aarhus Airport
    "GDN": {"latitude": 54.3770, "longitude": 18.4661},  # Lech Walesa
    "DPS": {"latitude": -8.7482, "longitude": 115.1670},  # Ngurah Rai
    "LBA": {"latitude": 53.8667, "longitude": -1.6600},  # Leeds/Bradford Airport
    "CUN": {"latitude": 21.0367, "longitude": -86.8773},  # Cancun International
    "RMF": {"latitude": 25.5619, "longitude": 34.5875},  # Marsa Alam International
    "HER": {"latitude": 35.3385, "longitude": 25.1804},  # Eleftherios Venizelos
    "BEG": {"latitude": 44.8197, "longitude": 20.3069},  # Belgrado Nikola Tesla
    "NCE": {"latitude": 43.6584, "longitude": 7.2159},  # Cote d'Azur
    "BLQ": {"latitude": 44.5381, "longitude": 11.2811},  # Guglielmo Marconi
    "TBS": {"latitude": 41.6699, "longitude": 44.9542},  # Luchthaven Tbilisi
    "GUW": {"latitude": 47.0924, "longitude": 51.9267},  # Atyrau
    "MRS": {"latitude": 43.4367, "longitude": 5.2150},  # Provence
    "VCE": {"latitude": 45.5056, "longitude": 12.3556},  # Marco Polo
    "ZAG": {"latitude": 45.7423, "longitude": 16.0670},  # Franjo Tudman
    "TRD": {"latitude": 63.4575, "longitude": 10.9227},  # Vaernes AB
    "LTN": {"latitude": 51.8747, "longitude": -0.3683},  # Luton
    "BUD": {"latitude": 47.4335, "longitude": 19.2614},  # Liszt Ferenc Int'l
    "HEL": {"latitude": 60.3172, "longitude": 24.9633},  # Helsinki-Vantaa
    "OPO": {"latitude": 41.2421, "longitude": -8.6801},  # Francisco Sa Carneiro
    "LYS": {"latitude": 45.7256, "longitude": 5.0811},  # Saint-Exupéry
    "ORK": {"latitude": 51.8419, "longitude": -8.4917},  # Cork International
    "CAN": {"latitude": 23.3925, "longitude": 113.2988},  # Guangzhou Baiyun
    "CTU": {"latitude": 30.5794, "longitude": 103.9555},  # Chengdu Shuangliu
    "FLR": {"latitude": 43.8103, "longitude": 11.2059},  # Peretola
    "SOF": {"latitude": 42.6975, "longitude": 23.4114},  # Sofia
    "RIX": {"latitude": 56.9236, "longitude": 23.9714},  # Riga
    "BHD": {"latitude": 54.6182, "longitude": -5.8725},  # George Best City Apt
    "BIO": {"latitude": 43.3019, "longitude": -2.9106},  # Bilbao Airport
    "PUJ": {"latitude": 18.5731, "longitude": -68.3639},  # Punta Cana International
    "SFO": {"latitude": 37.6213, "longitude": -122.3790},  # San Francisco International
    "LAX": {"latitude": 33.9416, "longitude": -118.4085},  # Los Angeles International
    "SEA": {"latitude": 47.4502, "longitude": -122.3088},  # Seattle-Tacoma Intl
    "CPT": {"latitude": -33.9648, "longitude": 18.6019},  # Cape Town
    "SSH": {"latitude": 27.9774, "longitude": 34.3909},  # Sharm-el-Sheikh International
    "TLL": {"latitude": 59.4139, "longitude": 24.8328},  # Lennart Meri Tallinn
    "SLC": {"latitude": 40.7884, "longitude": -111.9772},  # Salt Lake City International
    "VNO": {"latitude": 54.6349, "longitude": 25.2850},  # Vilnius
    "BVC": {"latitude": 16.1783, "longitude": -22.8197},
    "FUE": {"latitude": 28.3561, "longitude": -13.8633},  
    "NKG": {"latitude": 32.0500, "longitude": 118.8097}
}

# De base URL en headers
url = "https://api.schiphol.nl/public-flights/flights?includedelays=false&page={}&sort=%2BscheduleTime"
headers = {
    "app_id": "c93492b2",
    "app_key": "16a5764ed747d28fc0c58196e7322a04",
    'ResourceVersion': 'v4'
}

# Een lege lijst om alle vluchtdata op te slaan
all_flights_data = []

# Loop over de pagina's (0 tot 29, dus 30 pagina's)
for page in range(50):
    # Stel de volledige URL samen met de pagina
    page_url = url.format(page)
    
    # Haal de gegevens op van de API
    response = requests.get(page_url, headers=headers)
    data = response.json()  # Verkrijg de JSON reactie
    
    # Haal de 'flights' lijst op uit de response
    flights_data = data.get('flights', [])
    
    # Voeg de gegevens toe aan de lijst
    all_flights_data.extend(flights_data)

# Normaliseer de vluchtgegevens naar een DataFrame
df = pd.json_normalize(all_flights_data)

url = "https://nl.wikipedia.org/wiki/Vliegvelden_gesorteerd_naar_IATA-code"

# Set the headers with a User-Agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Fetch the HTML content with requests
response = requests.get(url, headers=headers)

# Use StringIO to convert the HTML content to a file-like object
html_content = StringIO(response.text)

# Use pandas to read the table from the HTML content
tables = pd.read_html(html_content)

# Select the table you want (in your case, the correct one based on the structure of the page)
vliegvelden = tables[1]  # Adjust the index based on the correct table

# Zet de lijstkolom om naar een stringkolom door het eerste element te selecteren:
df['route.destinations'] = df['route.destinations'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)

# Verwijder dubbele IATA-codes en behoud alleen de laatste instantie
vliegvelden_clean = vliegvelden.drop_duplicates(subset='IATA', keep='last')

# Maak een mapping van IATA-code naar de bijbehorende luchthavennaam
mapping = vliegvelden_clean.set_index('IATA')['Luchthaven']
mapping2 = vliegvelden_clean.set_index('IATA')['Stad']
mapping3 = vliegvelden_clean.set_index('IATA')['Land']

# Voeg een nieuwe kolom toe aan df door de afkorting te mappen op de juiste luchthavennaam
df['Luchthaven'] = df['route.destinations'].map(mapping)
df['Stad'] = df['route.destinations'].map(mapping2)
df['Land'] = df['route.destinations'].map(mapping3)

# Functie om latitude en longitude toe te voegen
def add_coordinates(row):
    country = row['route.destinations']
    if country in GeoCoö:
        return pd.Series(GeoCoö[country])
    else:
        return pd.Series({"latitude": None, "longitude": None})

# Voeg nieuwe kolommen 'latitude' en 'longitude' toe aan je DataFrame
df[['latitude', 'longitude']] = df.apply(add_coordinates, axis=1)

# Zet de kolommen om naar datetime
df['actualLandingTime'] = pd.to_datetime(df['actualLandingTime'], errors='coerce')
df['estimatedLandingTime'] = pd.to_datetime(df['estimatedLandingTime'], errors='coerce')

# Bereken het tijdsverschil tussen actualLandingTime en estimatedLandingTime
df['landingDelay'] = df['actualLandingTime'] - df['estimatedLandingTime']

# Zet het tijdsverschil om naar seconden
df['landingDelay'] = df['landingDelay'].dt.total_seconds()


#STREAMLIT

# Streamlit titel
st.title("Schiphol Vluchtdata Dashboard")

continenten = {
    "Afrika": [
        "Algerije", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Comoren", "Congo-Brazzaville",
        "Congo-Kinshasa", "Djibouti", "Egypte", "Eritrea", "Eswatini", "Ethiopië", "Gabon", "Gambia", "Ghana",
        "Guinee", "Guinee-Bissau", "Ivoorkust", "Kaapverdië", "Kameroen", "Kenia", "Lesotho", "Liberia", "Libië",
        "Madagaskar", "Malawi", "Mali", "Marokko", "Mauritanië", "Mauritius", "Mozambique", "Namibië", "Niger",
        "Nigeria", "Oeganda", "Rwanda", "Sao Tomé en Principe", "Senegal", "Seychellen", "Sierra Leone",
        "Soedan", "Somalië", "Tanzania", "Togo", "Tsjaad", "Tunesië", "Zambia", "Zimbabwe", "Zuid-Afrika",
        "Zuid-Soedan"
    ],
    "Azië": [
        "Afghanistan", "Armenië", "Azerbeidzjan", "Bahrein", "Bangladesh", "Bhutan", "Brunei", "Cambodja",
        "China", "Cyprus", "Filipijnen", "Georgië", "India", "Indonesië", "Irak", "Iran", "Israël", "Japan",
        "Jemen", "Jordanië", "Kazachstan", "Kirgizië", "Koeweit", "Laos", "Libanon", "Maldiven", "Maleisië",
        "Mongolië", "Myanmar", "Nepal", "Noord-Korea", "Oezbekistan", "Oman", "Pakistan", "Qatar", "Rusland",
        "Saoedi-Arabië", "Singapore", "Sri Lanka", "Syrië", "Tadzjikistan", "Taiwan", "Thailand", "Turkije",
        "Turkmenistan", "Verenigde Arabische Emiraten", "Vietnam", "Zuid-Korea"
    ],
    "Europa": [
        "Albanië", "Andorra", "België", "Bosnië en Herzegovina", "Bulgarije", "Denemarken", "Duitsland",
        "Estland", "Finland", "Frankrijk", "Griekenland", "Hongarije", "Ierland", "IJsland", "Italië", "Kosovo",
        "Kroatië", "Letland", "Liechtenstein", "Litouwen", "Luxemburg", "Malta", "Moldavië", "Monaco",
        "Montenegro", "Nederland", "Noord-Macedonië", "Noorwegen", "Oekraïne", "Oostenrijk", "Polen", "Portugal",
        "Roemenië", "San Marino", "Servië", "Slovenië", "Slowakije", "Spanje", "Tsjechië", "Vaticaanstad",
        "Verenigd Koninkrijk", "Wit-Rusland", "Zweden", "Zwitserland"
    ],
    "Noord-Amerika": [
        "Antigua en Barbuda", "Bahama's", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica",
        "Dominicaanse Republiek", "El Salvador", "Grenada", "Guatemala", "Haïti", "Honduras", "Jamaica",
        "Mexico", "Nicaragua", "Panama", "Saint Kitts en Nevis", "Saint Lucia", "Saint Vincent en de Grenadines",
        "Trinidad en Tobago", "Verenigde Staten"
    ],
    "Zuid-Amerika": [
        "Argentinië", "Bolivia", "Brazilië", "Chili", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru",
        "Suriname", "Uruguay", "Venezuela"
    ],
    "Oceanië": [
        "Australië", "Fiji", "Kiribati", "Marshalleilanden", "Micronesia", "Nauru", "Nieuw-Zeeland", "Palau",
        "Papoea-Nieuw-Guinea", "Samoa", "Salomonseilanden", "Tonga", "Tuvalu", "Vanuatu"
    ]
}

# Verwijder rijen met NaN in de 'longitude' kolom
df = df.dropna(subset=['longitude'])


# Functie om een land naar een continent te mappen
def land_naar_continent(land):
    for continent, landen in continenten.items():
        if land in landen:
            return continent
    return "Oceanië"

df['Continent'] = df['Land'].apply(land_naar_continent)

# Streamlit app
st.title("Landen per Continent Histogram")

# Selectie van continent
geselecteerd_continent = st.selectbox("Selecteer een continent", ["Alle"] + list(continenten.keys()))

# Filter data
if geselecteerd_continent == "Alle":
    subset = df
else:
    subset = df[df['Continent'] == geselecteerd_continent]

# Plot
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=subset['Land'],
    name=geselecteerd_continent if geselecteerd_continent != "Alle" else "Alle"
))

fig.update_layout(title=f"Histogram van landen in {geselecteerd_continent}")
st.plotly_chart(fig)

# Functie om een land naar een continent te mappen
def land_naar_continent(land):
    for continent, landen in continenten.items():
        if land in landen:
            return continent
    return "Onbekend"

df["Continent"] = df["Land"].apply(land_naar_continent)

# Groepeer de data per continent en bereken gemiddelde landingDelay
df_grouped = df.groupby(["Continent", "Land"])["landingDelay"].mean().reset_index()

# Streamlit UI
st.title("Histogram van Landing Delay per Continent")

# Selectie van continent
geselecteerd_continent = st.selectbox("Selecteer een continent:", ["Alle"] + list(df_grouped["Continent"].unique()))

# Plot maken
fig = go.Figure()

if geselecteerd_continent == "Alle":
    for continent in df_grouped["Continent"].unique():
        subset = df_grouped[df_grouped["Continent"] == continent]
        fig.add_trace(go.Histogram(
            x=subset["landingDelay"],
            name=continent,
            opacity=0.75
        ))
else:
    subset = df_grouped[df_grouped["Continent"] == geselecteerd_continent]
    fig.add_trace(go.Histogram(
        x=subset["landingDelay"],
        name=geselecteerd_continent,
        opacity=0.75
    ))

# Layout aanpassen
fig.update_layout(
    title=f"Histogram van Landing Delay in {geselecteerd_continent}",
    xaxis_title="Landing Delay (minuten)",
    yaxis_title="Aantal landen",
    barmode="overlay",
    legend_title="Continent",
)

# Toon de grafiek in Streamlit
st.plotly_chart(fig)


#  **Pie-chart: Aantal vluchten per pier**
if 'pier' in df.columns:
    st.subheader("Aantal Vluchten per Pier")
    df_pier_count = df['pier'].value_counts().reset_index()
    df_pier_count.columns = ['Pier', 'Aantal Vluchten']
    fig_pier = px.pie(df_pier_count, names='Pier', values='Aantal Vluchten', 
                      title="Verdeling Vluchten per Pier", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_pier)


#  **Grafiek: Aantal vluchten per bestemming**
if 'Luchthaven' in df.columns:
    st.subheader("Aantal Vluchten per Bestemming")
    df_dest_count = df['Luchthaven'].value_counts().reset_index()
    df_dest_count.columns = ['Bestemming', 'Aantal Vluchten']
    fig_dest = px.bar(df_dest_count, x='Bestemming', y='Aantal Vluchten', 
                      color='Aantal Vluchten', 
                      text_auto=True, 
                      title="Top Bestemmingen",
                      color_continuous_scale="blues")
    st.plotly_chart(fig_dest)




st.title("Animatie van vluchten vanuit Schiphol")

# Zorg ervoor dat 'actualLandingTime' een datetime-object is.
df['actualLandingTime'] = pd.to_datetime(df['actualLandingTime'])

# Schiphol-coördinaten (vast)
schiphol_lat = 52.3086
schiphol_lon = 4.7639

# Sorteer de DataFrame op landingstijd
df = df.sort_values('actualLandingTime')

# Verkrijg alle unieke landingstijden
unique_times = df['actualLandingTime'].sort_values().unique()

# Maak de frames voor de animatie: voor elk uniek tijdstip tonen we cumulatief de vluchten
frames = []
for t in unique_times:
    current_flights = df[df['actualLandingTime'] <= t]
    lats = []
    lons = []
    # Voeg voor iedere vlucht een lijn toe van Schiphol naar de bestemming
    for _, flight in current_flights.iterrows():
        lats.extend([schiphol_lat, flight['latitude'], None])
        lons.extend([schiphol_lon, flight['longitude'], None])
    
    frame = go.Frame(
        data=[go.Scattergeo(
            lat=lats,
            lon=lons,
            mode='lines',
            line=dict(width=2, color='blue'),
            hoverinfo='none'
        )],
        name=str(t)
    )
    frames.append(frame)

# Begin met de eerste frame
initial_flights = df[df['actualLandingTime'] <= unique_times[0]]
lats = []
lons = []
for _, flight in initial_flights.iterrows():
    lats.extend([schiphol_lat, flight['latitude'], None])
    lons.extend([schiphol_lon, flight['longitude'], None])

fig = go.Figure(
    data=[go.Scattergeo(
        lat=lats,
        lon=lons,
        mode='lines',
        line=dict(width=2, color='blue')
    )],
    frames=frames
)

# Voeg een play-knop en slider toe voor de animatie
fig.update_layout(
    title_text='Animatie van vluchten vanuit Schiphol',
    geo=dict(
        projection_type='natural earth',
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)"
    ),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        x=0.1,
        y=0,
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None, {"frame": {"duration": 500, "redraw": True},
                                   "fromcurrent": True,
                                   "transition": {"duration": 300, "easing": "quadratic-in-out"}}]
                     )]
    )],
    sliders=[{
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 12},
            'prefix': 'Landing time: ',
            'visible': True,
            'xanchor': 'center'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': [{
            'args': [[str(t)], {'frame': {'duration': 500, 'redraw': True},
                                  'mode': 'immediate',
                                  'transition': {'duration': 300}}],
            'label': str(t),
            'method': 'animate'
        } for t in unique_times]
    }]
)

# Toon de Plotly-figuur in Streamlit
st.plotly_chart(fig, use_container_width=True)

