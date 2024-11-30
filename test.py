import streamlit as st
import pandas as pd
import duckdb

# Chargement des données
data = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx')

# CSS pour le style des métriques
st.markdown(
    """
    <style>
    .rect-metric {
        padding: 20px;
        margin: 10px;
        border-radius: 8px;
        background-color: #f3f3f3;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        font-size: 18px;
    }
    .rect-metric-title {
        font-size: 18px;
        margin-bottom: 5px;
        color: #333;
    }
    .rect-metric-value {
        font-size: 32px;
        color: #007bff;
        font-weight: bold;
    }
    .rect-metric-delta {
        font-size: 18px;
        margin-top: 5px;
        color: #28a745;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction pour afficher une métrique stylisée
def display_big_metric(title, value, delta=None):
    delta_html = f"<div class='rect-metric-delta'>{delta}</div>" if delta else ""
    st.markdown(
        f"""
        <div class='rect-metric'>
            <div class='rect-metric-title'>{title}</div>
            <div class='rect-metric-value'>{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# Menu de navigation
menu = st.sidebar.radio("Navigation", ["Home", "DataViz", "Onto_API_REST"])

if menu == "Home":
    st.title("🏠 Home")
    st.write("Bienvenue dans l'application.")

elif menu == "DataViz":
    st.title("📊 Data Visualization")
    st.write("Visualisez vos données ici.")

    # Requête DuckDB pour les affiliations par pays
    pays_q = """
    SELECT Country, COUNT(*) AS Affiliation_by_country
    FROM data
    GROUP BY Country
    """
    pays = duckdb.sql(pays_q).df()  # Convertir en DataFrame Pandas

    # Afficher les métriques en grille (3 colonnes)
    col1, col2, col3 = st.columns(3)

    with col1:
        display_big_metric("Affiliation", data['Affiliation ID'].shape[0])

    with col2:
        display_big_metric("Countries", pays.shape[0])

    with col3:
        display_big_metric("Records", data.shape[0])

    # Création des graphiques et affichage des données
    st.bar_chart(pays, x="Country", y="Affiliation_by_country")
    st.dataframe(data)

elif menu == "Onto_API_REST":
    st.title("🌐 Ontology API REST")

    st.write("Cette section est dédiée à la documentation et à l'interaction avec l'API REST.")

    st.markdown("""
    **Points de terminaison disponibles :**
    - `/` : Obtenir des informations principales.
    - `/get_parents` : Récupérer les relations parents-enfants.

    **Exemple d'utilisation via `curl` :**
    ```bash
    curl -X GET "http://127.0.0.1:8000/?id=http://entity/CST/OCCLUS%20CAROTID"
    ```
    """)

    # Widgets supplémentaires pour interagir avec l'API (à personnaliser selon vos besoins)

# Pied de page
st.sidebar.markdown("---")
st.sidebar.write("**Made with ❤️ in Streamlit**")
