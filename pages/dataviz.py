import streamlit as st
import pandas as pd
import duckdb
import os
import logging
from init_db import init_db




def display_data_viz():

    st.markdown(
        """
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )


    if "data" not in os.listdir():
        logging.error(os.listdir())
        logging.error("creating data repository")
        os.mkdir("data")

    if "database.duckdb" not in os.listdir("data"):
        init_db()

    con = duckdb.connect(database="data/database.duckdb", read_only=False)

    st.title(":material/analytics: Data Visualization")
    st.write("View your data here.")

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
    SELECT DISTINCT COUNT("Author ID") AS nb_authors
    FROM authors
    """

    top_authors_q = """
    SELECT Name AS Authors, "Number of occurrence" AS Occurence
    FROM authors
    ORDER BY Occurence DESC
    LIMIT 10
    """

    nb_authors = con.execute(authors_q).df()
    top_authors = con.execute(top_authors_q).df()

    # Requête DuckDB countries
    pays_q = """
    SELECT Country, COUNT(*) AS Affiliation_by_country
    FROM data
    GROUP BY Country
    ORDER BY Affiliation_by_country DESC
    """
    pays = con.execute(pays_q).df()

    # Requête DuckDB recruting statut

    statut_q = """
        SELECT "Recruitment status", COUNT(*) AS nb_status
        FROM data
        GROUP BY "Recruitment status"
        ORDER BY nb_status DESC
        """
    statut = con.execute(statut_q).df()

    # Requête DuckDB duration by publication type

    pub_q="""
    SELECT 
    "Publication type" AS type, 
    COUNT(*) AS duration_count
    FROM publications
    GROUP BY type
    ORDER BY type ASC;
    """
    pub = con.execute(pub_q).df()

    # Requête DuckDB population age

    pop_age_q = """
        SELECT 
        "Population age" AS Age, 
        COUNT(*) AS age_count
        FROM authors
        GROUP BY Age
        HAVING Age not null
        ORDER BY age_count ASC;
        """
    pop_age = con.execute(pop_age_q).df()

    # CSS pour le style des métriques
    st.markdown(
        """
        <style>
        .rect-metric {
            padding: 10px;
            margin: 24px;
            margin-bottom: 24px;
            background-color: white;
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
        
        .material-icons{
            font-size:28px; 
            vertical-align:middle; 
            color: #007BFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    def display_big_metric(title, value, delta=None, icon=None):
        icon_html = f"<span class='material-icons'>{icon}</span>" if icon else ""
        delta_html = f"<div class='rect-metric-delta' style='font-size:12px; color:green;'>{delta}</div>" if delta else ""

        st.markdown(
            f"""
            <div class='rect-metric' style='display: flex; align-items: center; margin-bottom: 16px;'>
                {icon_html} <!-- Insertion de l'icône ici -->
                <div style='margin-left: 8px;'> <!-- Ajout d'un espace entre l'icône et le texte -->
                    <div class='rect-metric-title' style='font-size: 14px; color: #6c757d;'>{title}</div>
                    <div class='rect-metric-value' style='font-size: 24px; font-weight: bold;'>{value}</div>
                    {delta_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Afficher les métriques en grille (4 colonnes)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_big_metric(
            title="Authors",
            value=nb_authors['nb_authors'].iloc[0],
            delta="+0%",
            icon="group"
        )
        #display_big_metric("Authors", nb_authors['nb_authors'].iloc[0], "")

    with col2:
        display_big_metric(
            title="Countries",
            value=pays.shape[0],
            delta="+0%",
            icon="flag"
        )

    with col3:
        display_big_metric(
            title="Publications",
            value=publications.shape[0],
            delta="+0%",
            icon="auto_stories"
        )



    with col4:
        display_big_metric(
            title="Affiliations",
            value=data.shape[0],
            delta="+0%",
            icon="cloud"
        )

        #display_big_metric("Affilitions", data.shape[0])

    # Afficher les graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top Authors", divider=True)
        st.bar_chart(top_authors, x="Authors", y="Occurence", color="Authors", horizontal=True)

    with col_right:
        st.subheader("Top Countries", divider=True)
        st.bar_chart(pays.head(10), x="Country", y="Affiliation_by_country")


    # Afficher les graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Recruitment status", divider=True)
        st.bar_chart(statut, x="Recruitment status", y="nb_status", color="Recruitment status")



    with col_right:
        st.subheader("Age of population to be analyzed", divider=True)
        st.bar_chart(pop_age, x="Age", y="age_count", color="Age",horizontal=True)

    st.subheader("Duration by publication type", divider=True)
    st.bar_chart(pub, x="type", y="duration_count", color="type",horizontal=True)

    st.subheader("Countries by affiliation", divider=True)
    st.bar_chart(pays, x="Country", y="Affiliation_by_country", color="Country")

    # Afficher les données
    st.subheader("Data bases", divider=True)
    st.write("Affiliations")
    st.dataframe(data)
    st.write("Authors")
    st.dataframe(authors)
    st.write("Publications")
    st.dataframe(publications)
