import streamlit as st

def display_onto_api():
    st.title("🌐 Ontology API REST")
    st.subheader("Interact with the REST API here.", divider=True)

    user_input = st.text_input(
        label="Please enter your request id",
        key="user_input",
        placeholder="http://entity/CST/OCCLUS%20CAROTID"
    )

    validation=   st.button("View ancestors", type="primary")
    if user_input:
        if validation:
            st.write(f"Vous avez saisi : {user_input}")

    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)




    st.subheader("Information on using api", divider=True)
    st.markdown("""
    **Points de terminaison disponibles :**
    - `/` : Obtenir des informations principales.
    - `/get_parents` : Récupérer les relations parents-enfants.

    **Exemple d'utilisation via `curl` :**
    ```bash
    curl -X GET "http://127.0.0.1:8000/?id=http://entity/CST/OCCLUS%20CAROTID"
    ```
    """)

