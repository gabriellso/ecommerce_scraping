import streamlit as st
import pandas as pd

st.title("📦 Painel de Produtos E-commerce")

try:
    df = pd.read_csv('results_produtos.csv')
except FileNotFoundError:
    st.error("Arquivo 'results_produtos.csv' não encontrado. Rode o scraper primeiro.")
    st.stop()

df["price"] = df["price"].astype(str).fillna("0")
df["price_float"] = df["price"].astype(float)

st.dataframe(df)

nome_filtro = st.text_input("🔍 Buscar por nome:")
if nome_filtro:
    df_filtered = df[df["name"].str.contains(nome_filtro, case=False, na=False)]
else:
    df_filtered = df

st.write("📈 Resumo de preços:")
st.bar_chart(df_filtered["price_float"])
