import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

volcanoes_df_raw = load_data(path="./data/raw/volcano_ds_pop.csv")
df = deepcopy(volcanoes_df_raw)
df.drop(columns=["Unnamed: 0"], inplace=True)
df['Country'] = df['Country'].replace({'United States':'United States of America',
                                       'Tanzania':'United Republic of Tanzania',
                                        'Martinique':'Martinique',
                                        'Sao Tome & Principe':'Sao Tome and Principe',
                                        'Guadeloupe':'Guadeloupe',
                                        'Wallis & Futuna':'Wallis and Futuna'})

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df.groupby('Last Known').Number.count()

mapping = {
    'Unknown': 0,
    'D1': 1,
    'D2': 2,
    'D3': 3,
    'D4': 4,
    'D5': 5,
    'D6': 6,
    'D7': 7,
    'U': 0,
    'Q': 0,
    'P': 0,
    'U1': 0,
    'U7': 0
}

df['Active State'] = df['Last Known'].map(mapping)

st.title("Volcanoes of the World")
st.header("Use the sidebar to explore the data")
countries = ["All"]+sorted(pd.unique(df['Country']))
left_column, right_column = st.columns(2)
country = left_column.selectbox("Choose a country", countries)

if st.sidebar.checkbox("Show Dataframe"):
    st.subheader("Feel free to explore it :)")
    st.dataframe(data=df)

if st.sidebar.checkbox("Amount of Volcanoes per Type"):
    st.subheader("Amount of Volcanoes per Type")
    if country == "All":
        reduced_df = df
    else:
        reduced_df = df[df["Country"] == country]
    plot_types = ["Matplotlib", "Plotly"]
    plot_type = right_column.radio("Choose Plot Type", plot_types)
    if plot_type == "Matplotlib":
        type_counts = reduced_df['Type'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        type_counts.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_xlabel('Type', fontsize=12)
        ax.set_ylabel('Amount', fontsize=12)
        st.pyplot(fig)
    else:
        fig = px.bar(
            reduced_df['Type'].value_counts().reset_index(),
            x="Type",y="count",
            labels={'index': 'Volcano Type', 'Type': 'Amount'},
        )
        st.plotly_chart(fig)

if st.sidebar.checkbox("Map of the world"):
    st.subheader("Map of the World´s volcanoes")
    if country == "All":
        reduced_df = df
    else:
        reduced_df = df[df["Country"] == country]
    reduced_df["latitude"] = reduced_df["Latitude"]
    reduced_df["longitude"] = reduced_df["Longitude"]
    st.map(reduced_df)
    
if st.sidebar.checkbox("Active & Inactive"):
    st.subheader("Active & Inactive volcanoes per Country")
    if country == "All":
        reduced_df = df
    else:
        reduced_df = df[df["Country"] == country]
    plot_types = ["Matplotlib", "Plotly"]
    plot_type = right_column.radio("Choose Plot Type", plot_types)
    active_inactive = reduced_df.groupby(['Country', 'Active State']).size().reset_index(name='Count')
    if plot_type == "Plotly":
        fig = px.bar(
            active_inactive, x='Country', y='Count', color='Active State',
            labels={'Count': 'Amount', 'Country': 'Country', 'Active State': 'Active State'}
        )
        st.plotly_chart(fig)
    else:
        active_inactive_pivot = active_inactive.pivot(index='Country', columns='Active State', values='Count').fillna(0)
        fig, ax = plt.subplots(figsize=(12, 6))
        active_inactive_pivot.plot(kind='bar', stacked=True, color=['lightblue', 'orange'], ax=ax)
        ax.set_xlabel('Country', fontsize=12)
        ax.set_ylabel('Amount', fontsize=12)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        


















