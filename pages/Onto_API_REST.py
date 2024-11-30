import streamlit as st

def display_onto_api():
    st.title("🌐 Ontology API REST")
    st.write("Interagissez avec l'API REST ici.")

    st.markdown("""
    **Points de terminaison disponibles :**
    - `/` : Obtenir des informations principales.
    - `/get_parents` : Récupérer les relations parents-enfants.

    **Exemple d'utilisation via `curl` :**
    ```bash
    curl -X GET "http://127.0.0.1:8000/?id=http://entity/CST/OCCLUS%20CAROTID"
    ```
    """)
