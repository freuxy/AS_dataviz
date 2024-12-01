import streamlit as st
import requests
import duckdb
import os
import logging
from init_db import init_db

def display_onto_api():
    st.title("🌐 Ontology API REST")
    st.subheader("Interact with the REST API here.", divider=True)


    if "data" not in os.listdir():
        logging.error(os.listdir())
        logging.error("creating data repository")
        os.mkdir("data")

    if "database.duckdb" not in os.listdir("data"):
        init_db()

    con = duckdb.connect(database="data/database.duckdb", read_only=False)

    user_input = st.text_input(
        label="Please enter your request id",
        key="user_input",
        placeholder="http://entity/CST/OCCLUS%20CAROTID"
    )

    validation=   st.button("View ancestors", type="primary")
    if user_input and validation:
            #st.write(f"Vous avez saisi : {user_input}")

            # URL de l'API que vous souhaitez appeler
            api_url = f"https://as-test-api.onrender.com/?id={user_input}"
            st.write(api_url)

            # Appel de l'API REST
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    # Si la requête réussit, afficher les résultats
                    st.write("Résultats de l'API :")
                    st.json(response.json())  # Affiche la réponse JSON
                else:
                    st.error(f"Erreur lors de la récupération des données. Code d'état : {response.status_code}")
            except requests.exceptions.RequestException as e:
                # Si une erreur de connexion ou autre se produit
                st.error(f"Erreur lors de l'appel API : {e}")

    onto_q = """
            SELECT *
            FROM onto
            """
    onto = con.execute(onto_q).df()
    st.dataframe(onto)


    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)




    st.subheader("Information on using api", divider=True)
    st.markdown("""
    **Points de terminaison disponibles :**
    - `/` : Récupérer les relations parents-enfants.

    **Exemple d'utilisation via `curl` :**
    ```bash
    curl -X GET "http://127.0.0.1:8000/?id=http://entity/CST/OCCLUS%20CAROTID"
    ```
    """)

