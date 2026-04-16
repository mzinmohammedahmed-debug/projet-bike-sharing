import streamlit as st
import pandas as pd
import joblib

# 1. Configuration de la page
st.set_page_config(page_title="Prédiction Vélos", page_icon="🚲")
st.title("🚲 Dashboard : Prévision des locations de vélos")
st.markdown("Ajustez les paramètres ci-dessous pour voir la prédiction de l'IA en temps réel.")

# 2. Chargement du modèle
# On utilise st.cache_resource pour ne charger le modèle qu'une seule fois (plus rapide)
@st.cache_resource
def load_model():
    return joblib.load('modele_foret_velo.joblib')

modele = load_model()

# 3. Création de l'interface utilisateur (barre latérale)
st.sidebar.header("Météo et Horaires")

# On crée des curseurs pour les 3 variables les plus importantes (selon ton graphique !)
heure = st.sidebar.slider("Heure de la journée (hour)", min_value=0, max_value=23, value=12, step=1)
temp_ressentie = st.sidebar.slider("Température ressentie (atemp)", min_value=0.0, max_value=50.0, value=20.0, step=0.5)
jour_ouvrable = st.sidebar.selectbox("Est-ce un jour ouvrable ?", options=[0, 1], format_func=lambda x: "Oui" if x==1 else "Non")

# 4. Affichage des choix
st.write(f"**Heure choisie :** {heure}h")
st.write(f"**Température :** {temp_ressentie}°C")
st.write(f"**Jour ouvrable :** {'Oui' if jour_ouvrable == 1 else 'Non'}")

st.info("Le modèle est prêt ! La logique de prédiction sera ajoutée ici.")  