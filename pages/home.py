import streamlit as st

def display_home():
    st.title("🏠 ArcaScience technical test")
    st.write("How to use this app")

    # Afficher les graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Dataviz demo", divider=True)
        st.write("“This space is dedicated to exploring data relating to Key Opinion Leaders (KOLs) in the biomedical and scientific fields. Discover dynamic visualizations that highlight trends, connections and key insights. Navigate through interactive graphs to get an overview of the data.  Please click on Kol dataviz tab”")
        col_left.image(
            "./files/dataviz.png",
            use_container_width=True,
            caption="ArcaScience.io"
        )

    with col_right:
        st.subheader("Api demo", divider=True)
        st.write("“Welcome to the Ontology API REST tab. Here you can interact directly with our REST API to explore ontologies and their relationships. Use this tool to search for entities, explore their ancestors, and get detailed information. This space is designed to make the analysis of semantic structures easy and straightforward.  Please click on Onto_API_REST tab”")
        col_right.image(
            "./files/onto.png",
            use_container_width=True,
            caption="ArcaScience.io"
        )
