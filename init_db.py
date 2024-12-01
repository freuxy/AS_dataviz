import io

import duckdb
import pandas as pd


def init_db():

    con = duckdb.connect(database="data/database.duckdb", read_only=False)


    onto = pd.read_csv("../AS_Test_API/data/onto_x.csv")
    con.execute("CREATE TABLE IF NOT EXISTS onto AS SELECT * FROM onto")

    data = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx')
    con.execute("CREATE TABLE IF NOT EXISTS data AS SELECT * FROM data")

    authors = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx', sheet_name="Authors")
    con.execute("CREATE TABLE IF NOT EXISTS authors AS SELECT * FROM authors")


    publications = pd.read_excel('./data/kol_csv_29_07_2024_drug_and_kol_standardized.xlsx', sheet_name="Publications")
    con.execute("CREATE TABLE IF NOT EXISTS publications AS SELECT * FROM publications")

    con.close()