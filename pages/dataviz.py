import streamlit as st
import pandas as pd
import duckdb

def display_data_viz():
    st.title(":material/analytics: Data Visualization")
    st.write("Visualisez vos données ici.")

    # Charger les données
    data = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx')
    authors = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx', sheet_name="Authors")
    publications = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx', sheet_name="Publications")

    # Renommer les colonnes dans le DataFrame local
    authors.rename(columns={'Author ID': 'ID'}, inplace=True)
    authors.rename(columns={'Number of occurrence': 'nb_occurence'}, inplace=True)

    # Charger les DataFrames dans DuckDB pour refléter les modifications
    duckdb.register('authors', authors)
    duckdb.register('data', data)

    # Requête DuckDB pour les auteurs
    authors_q = """   
    SELECT DISTINCT COUNT(ID) AS nb_authors
    FROM authors
    """

    top_authors_q = """
    SELECT Name AS Authors, nb_occurence AS Occurence
    FROM authors
    ORDER BY Occurence DESC
    LIMIT 10
    """

    nb_authors = duckdb.sql(authors_q).df()
    top_authors = duckdb.sql(top_authors_q).df()

    # Requête DuckDB countries
    pays_q = """
    SELECT Country, COUNT(*) AS Affiliation_by_country
    FROM data
    GROUP BY Country
    ORDER BY Affiliation_by_country DESC
    LIMIT 10
    """
    pays = duckdb.sql(pays_q).df()

    pays_count_q = """
    SELECT Country, COUNT(*) AS Affiliation_by_country
    FROM data
    GROUP BY Country
    """
    pays_count = duckdb.sql(pays_q).df()

    # CSS pour le style des métriques
    st.markdown(
        """
        <style>
        .rect-metric {
            padding: 10px;
            margin: 24px;
            margin-bottom: 24px;
            border-radius: 8px;
            border: 1px solid black;
            text-align: left;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            font-size: 18px;
        }
        .rect-metric-title {
            font-size: 18px;
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

    # Afficher les métriques en grille (4 colonnes)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_big_metric("Authors", nb_authors['nb_authors'].iloc[0])

    with col2:
        display_big_metric("Countries", pays_count.shape[0])

    with col3:
        display_big_metric("Publications", publications.shape[0])

    with col4:
        display_big_metric("Affilitions", data.shape[0])

    # Afficher les graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top 10 Authors", divider=True)
        st.bar_chart(top_authors, x="Authors", y="Occurence", color="Authors", horizontal=True)

    with col_right:
        st.subheader("Top 10 Countries", divider=True)
        st.bar_chart(pays, x="Country", y="Affiliation_by_country")



    st.bar_chart(pays, x="Country", y="Affiliation_by_country", color="Country")

    # Afficher les données
    st.dataframe(data)
    st.dataframe(authors)
    st.dataframe(publications)
