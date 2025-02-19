import folium
import json
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from shapely.geometry import shape

# Charger les données depuis la base de données ou un fichier CSV
@st.cache_data
def load_data():
    #Chargement du dataset and changement de types
    data = pd.read_csv('./dataset/updated_data.csv')
    data['annee'] = data['annee'].astype('object')
    data['taux_pour_mille'] = data['taux_pour_mille'].astype(float)
    return data


# Fonction pour déterminer la couleur en fonction de taux_pour_mille
def get_color(taux):  
    if taux < 2:
        return 'green'
    elif 2 <= taux <5:  # Fix condition to avoid duplication
        return 'blue'
    else:
        return 'red'


# Charger les données
data = load_data()

# Charger le fichier GeoJSON
with open('./departements.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Créer un dictionnaire pour mapper les codes aux noms
code_to_name = {}
code_names = []
code_to_position = {}
for feature in geojson_data['features']:
    code = feature['properties']['code']
    name = feature['properties']['nom']
    code_to_name[code] = name
    code_names.append(code+'-'+name)
    geom = shape(feature['geometry'])  # Convert GeoJSON geometry to a Shapely object
    centroid = geom.centroid  # Get centroid of the polygon
    code_to_position[code] = [centroid.y, centroid.x]  # Convert to (lat, lon)
 
# Exemple d'utilisation
code_departement = "49"
nom_departement = code_to_name.get(code_departement, "Inconnu")
print(f"Le département {code_departement} est {nom_departement}.")



# Titre de l'application
st.title("Carte interactive des délits par département")

# Filtre pour sélectionner un département
departement_selectionne = st.selectbox(
    "Sélectionnez un département",
    options=code_names
)

# Filtrer les données pour le département sélectionné
select_code = departement_selectionne.split('-')[0]
data_filtree = data[data['Code_departement']==select_code]

# Centrer la carte sur le département sélectionné
m = folium.Map(location=code_to_position[select_code],  zoom_start=5, zoom_control=False)

# Ajouter un marqueur pour le département sélectionné
for _, row in data_filtree.iterrows():
    taux = row['taux_pour_mille']
    indicateur = row['indicateur']
    unite_de_compte = row['unite_de_compte']
    nombre = row['nombre']
    annee = row['annee']

    folium.CircleMarker(
        location=code_to_position[select_code], 
        radius=10,
        color=get_color(taux),
        fill=True,
        fill_color=get_color(taux),
        popup=f"""
            Département: {departement_selectionne}<br>
            Taux pour mille: {taux}<br>
            Indicateur: {indicateur}<br>
            Unité de compte: {unite_de_compte}<br>
            Nombre de crimes: {nombre}
            Année: {annee}
        """
    ).add_to(m)

# Ajouter une couche choroplèthe pour colorer les départements
folium.Choropleth(
    geo_data=geojson_data,
    name="choropleth",
    data=data,
    columns=["Code_departement", "taux_pour_mille"],
    key_on="feature.properties.code",
    fill_color="YlOrRd",  # Palette de couleurs
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Taux de criminalité pour mille habitants (%)",
).add_to(m)

#Legende de la carte
legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 90px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; padding: 10px;">
        <b>Légende</b><br>
        <i style="background:green; width: 20px; height: 20px; display: inline-block;"></i> < 2<br>
        <i style="background:violet; width: 20px; height: 20px; display: inline-block;"></i> 2-5<br>
        <i style="background:red; width: 20px; height: 20px; display: inline-block;"></i> > 5
    </div>
"""
#Ajoute la legende sur la carte
m.get_root().html.add_child(folium.Element(legend_html))


# Afficher la carte dans Streamlit
st.write(f"Carte du département {departement_selectionne}")
folium_static(m)

# Tableau interactif pour filtrer par indicateur et unité de compte
st.title("Tableau des délits")

# Filtres pour indicateur et unité de compte
indicateur_filter = st.selectbox(
    "Filtrer par indicateur",
    options=data_filtree['indicateur'].unique()
)
unite_de_compte_filter = st.selectbox(
    "Filtrer par unité de compte",
    options=data_filtree['unite_de_compte'].unique()
)

# Appliquer les filtres
filtered_data = data_filtree[
    (data_filtree['indicateur'] == indicateur_filter) &
    (data_filtree['unite_de_compte'] == unite_de_compte_filter)
]

# Afficher le tableau filtré
st.write(filtered_data[['Code_departement', 'indicateur', 'unite_de_compte', 'nombre', 'taux_pour_mille', 'annee']])