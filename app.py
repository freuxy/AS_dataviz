import streamlit as st
from pages.home import display_home
from pages.dataviz import display_data_viz
from pages.Onto_API_REST import display_onto_api

# ---- PAGE SETUP ----
st.set_page_config(page_title="Multi Page App", layout="wide")

# ---- MENU DE NAVIGATION ----
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Sélectionner une page", [" :material/home: Home", " :material/analytics: DataViz", " :material/cloud: Onto_API_REST"])

# ---- Affichage de la page en fonction de la sélection ----
if menu == " :material/home: Home":
    display_home()

elif menu == " :material/analytics: DataViz":
    display_data_viz()

elif menu == " :material/cloud: Onto_API_REST":
    display_onto_api()
