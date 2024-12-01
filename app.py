import streamlit as st
from pages.home import display_home
from pages.dataviz import display_data_viz
from pages.Onto_API_REST import display_onto_api


# ---- PAGE SETUP ----
st.set_page_config(page_title="ArcaScience Test", layout="wide")


# ---- LOGO DANS LA BARRE LATÉRALE ----
st.sidebar.image(
    "./files/images.png",
    use_container_width=True,
    caption="ArcaScience.io"
)

# ---- Définir les pages sans exécuter immédiatement leurs fonctions ---
home_page = st.Page(
    page=display_home,  # Référence à la fonction, pas un appel
    title="Home",
    icon=":material/home:"
)

dataviz = st.Page(
    page=display_data_viz,  # Référence à la fonction
    title="KOL dataviz",
    icon=":material/analytics:"
)

onto_api_rest = st.Page(
    page=display_onto_api,  # Référence à la fonction
    title="Onto_api_rest",
    icon=":material/cloud:"
)

# ---- NAVIGATION SETUP ----
pg = st.navigation(
    [
        home_page, dataviz, onto_api_rest
    ]
)

pg.run()
