import folium
from folium import plugins
import streamlit as st
from streamlit_folium import folium_static

post_coordinates = {
    "GME": (36.766390866134046, 3.2225848178649237),
    "sebdou": (36.684458669042044, 2.797788077388803),
    "Z'bair": (36.48248578919991, 2.8285360908923227),
    "Tlemcen": (35.68230930701206, -0.6047486532459292),
    "Remchi": (35.682387704347285, -0.6046521379038244),
    "Ain Timouchent 1": (35.295096277086884, -1.1512875346690785),
    "Ain Timouchent 2": (35.295096277086884, -1.1512875346690785),
    "S.Yacoub": (36.43327085492939, 2.688897290894736),
    "Boutlelis": (35.581594187670554, -0.940054587904635),
    "Messerghine": (35.682343797127054, -0.6047858704367539),
    "Oran Sud": (35.6822570396884, -0.6047432920774143),
    "Bousfer": (35.688167219951765, -0.6019735262534326),
    "Sidi el kbir": (36.5499140774171, 2.8516390332553216),
    "Sidi bel Abbes": (35.19367532686726, -0.6076450955511757),
    "Telagh": (35.23186322680193, -0.5709383674829289),
    "sidi bel abbes ville": (35.19365779147318, -0.6076665532222845),
    "mecheria": (36.54405401666144, 1.8130474975030708),
    "Mekera": (36.30829125033852, 1.848205762065421),
    "hadjout": (36.54467361434589, 2.4303818664032244),
    "Bouhanifia": (36.37792424296307, 1.8436863512901156),
    "draa ben khedda": (36.79691427852457, 3.9694977448229714),
    "ain sekhouna": (34.547993949359615, 0.8145332933347224),
    "El bayadh": (33.71225086459003, 1.035617919860697),
    "tizi medane": (36.58879270493575, 4.017219660404906),
    "mostaganem port": (35.93269715526, 0.07871744674182776),
    "mostaganem port sablette": (35.932366930563404, 0.07830975149176232),
    "ain tadeles": (35.997848517371686, 0.26480007372545816),
    "relizane": (35.78680094895221, 0.5394780677963403),
    "tissemsilte": (35.61791888130047, 1.7708158647348218),
    "Bordj bou naama": (35.86086825967805, 1.6187184692231407),
    "mahdia": (35.41711667378253, 1.7462782332735334),
    "khemis miliana": (36.28997956431238, 2.205425694678707),
    "mouzaia": (36.455840231595715, 2.6833309445642026)
}

# Coordinates for each site
site_coordinates = {
    "Abadla": (30.4299, 2.8594),
    "Kenadsa": (30.9217, 6.4714),
    "Aflou": (34.1087, 2.1016),
    "Nakhla": (33.3119, 7.2432),
    "Taleb Larbi": (33.6848, 7.3422),
    "Touggourt": (33.1247, 5.9396),
    "Leghrous": (34.7944, 5.1431),
    "Tolga": (34.7361, 5.3747),
    "Khenguet Sidi Nadji": (34.7922, 6.7309),
    "Batmete": (35.464, 3.5677),
    "M Ghaier": (34.0335, 5.8535),
    "Guerrara": (32.7834, 4.4365)
}

# Function to create a map with the locations of sites and posts
def create_map(sites, site_coordinates, post_coordinates, best_solution):
    # Create a map centered on Algeria
    m = folium.Map(location=[28.0339, 1.6596], zoom_start=6)

    # Add the locations of sites with their corresponding posts to the map
    for i, poste in enumerate(best_solution):
        site = sites[i]
        if poste != -1:
            site_coord = site_coordinates[site]
            if poste in post_coordinates:
                post_coord = post_coordinates[poste]
                folium.Marker(location=site_coord, popup=site, icon=folium.Icon(color='green')).add_to(m)
                folium.Marker(location=post_coord, popup=poste, icon=folium.Icon(color='blue')).add_to(m)
                folium.PolyLine(locations=[site_coord, post_coord], color='red').add_to(m)

    return m

sites = ["Abadla", "Kenadsa", "Aflou", "Nakhla", "Taleb Larbi", "Touggourt", "Leghrous", "Tolga", "Khenguet Sidi Nadji", "Batmete", "M Ghaier", "Guerrara"]
postes = ["GME", "sebdou", "Z'bair", "Tlemcen", "Remchi", "Beni Saf", "Ain Timouchent 1", "Ain Timouchent 2", "S.Yacoub", "Boutlelis", "Messerghine", "Oran Sud", "Bousfer", "Sidi el kbir", "Sidi bel Abbes", "Telagh", "sidi bel abbes ville", "mecheria", "Mekera", "hadjout", "Bouhanifia", "draa ben khedda", "ain sekhouna", "El bayadh", "tizi medane", "mostaganem port", "mostaganem port sablette", "ain tadeles", "relizane", "tissemsilte", "Bordj bou naama", "mahdia", "khemis miliana", "mouzaia"]

best_solution=[18, 31, -1, -1, 27, 25, -1, 9, 6, -1, -1, 22]

# Use the function to create and display the map with the locations of sites and posts
st.header("Carte des Emplacements des Sites et des Postes")
map = create_map(sites, site_coordinates, post_coordinates, best_solution)
folium_static(map)
