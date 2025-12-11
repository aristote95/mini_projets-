import streamlit as st
import pandas as pd
import altair as alt

# 1) Configuration de la page 
# ==============================
st.set_page_config(
    page_title="Exploration Bitcoin",
    layout="wide"
)


# 2) Chargement des données
# ==============================
@st.cache_data
def load_data():
    # On suppose que btc_daily.csv a une colonne 'Timestamp' ou 'Unnamed: 0'
    df = pd.read_csv("btc_daily.csv")
    
    # Si le timestamp est dans une colonne nommée 'Unnamed: 0' (cas courant d'index sauvegardé)
    if "Timestamp" not in df.columns and "Unnamed: 0" in df.columns:
        df = df.rename(columns={"Unnamed: 0": "Timestamp"})
    
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp")
    
    # Colonnes attendues : Timestamp, Open, High, Low, Close, Volume
    return df

df = load_data()

st.title("📈 Mini application d'exploration du Bitcoin")
st.markdown(
    """  Analyse exploratoire et temporelle des données historiques du Bitcoin """
)
st.markdown(
    """ 
    Cette application permet d'explorer l'évolution du prix du Bitcoin ainsi que la relation
    entre **prix** et **volume** avec des filtres temporels.
    """
)


# 3) Sidebar : filtres
# ==============================

st.sidebar.header("⚙️ Filtres")

min_date = df["Timestamp"].min().date()
max_date = df["Timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Période à analyser",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date = date_range
    end_date = date_range

mask = (df["Timestamp"].dt.date >= start_date) & (df["Timestamp"].dt.date <= end_date)
df_filtered = df.loc[mask].copy()

st.sidebar.write(f"Nombre de jours sélectionnés : {len(df_filtered)}")

# 4) Stats rapides
# ==============================

st.subheader("📊 Statistiques rapides sur la période sélectionnée")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Prix minimum (Close)", f"{df_filtered['Close'].min():.2f} $")

with col2:
    st.metric("Prix maximum (Close)", f"{df_filtered['Close'].max():.2f} $")

with col3:
    st.metric("Volume total", f"{df_filtered['Volume'].sum():,.0f}")


# 5) Courbe de prix interactive
# ==============================

st.subheader("📉 Courbe de prix (Close)")

price_chart = (
    alt.Chart(df_filtered)
    .mark_line()
    .encode(
        x=alt.X("Timestamp:T", title="Date"),
        y=alt.Y("Close:Q", title="Prix de clôture (USD)"),
        tooltip=["Timestamp:T", "Open:Q", "High:Q", "Low:Q", "Close:Q", "Volume:Q"]
    )
    .interactive()
)

st.altair_chart(price_chart, use_container_width=True)


# 6) Graphique Volume / Prix
# ==============================

st.subheader("📊 Relation Volume / Prix")

view_type = st.radio(
    "Type de visualisation volume/prix :",
    ("Scatter (Volume vs Close)", "Courbes synchronisées (Prix & Volume)")
)

if view_type == "Scatter (Volume vs Close)":
    scatter = (
        alt.Chart(df_filtered)
        .mark_circle(size=40, opacity=0.5)
        .encode(
            x=alt.X("Volume:Q", title="Volume échangé"),
            y=alt.Y("Close:Q", title="Prix de clôture (USD)"),
            color=alt.Color("Close:Q", legend=None),
            tooltip=["Timestamp:T", "Close:Q", "Volume:Q"]
        )
        .interactive()
    )
    st.altair_chart(scatter, use_container_width=True)

else:
    base = alt.Chart(df_filtered).encode(
        x=alt.X("Timestamp:T", title="Date")
    )

    line_price = base.mark_line(color="steelblue").encode(
        y=alt.Y("Close:Q", title="Prix (USD)")
    )

    bar_volume = base.mark_bar(opacity=0.3).encode(
        y=alt.Y("Volume:Q", title="Volume")
    )

    st.altair_chart(
        alt.layer(line_price, bar_volume).resolve_scale(
            y='independent'
        ).interactive(),
        use_container_width=True
    )

# ==============================
# 7) Table des données filtrées
# ==============================

with st.expander("Voir les données filtrées"):
    st.dataframe(df_filtered.head(200))

