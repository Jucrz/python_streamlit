import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")

def load_data():
    data = requests.get('http://127.0.0.1:5000/mydatabase').json()["data"]
    col = ["ID", "Date", "Open", "High", "Low", "Close", "Volume", "MarketCap", "Crypto"]
    data = pd.DataFrame(data, columns=col)
    return data


def bar_plot(x, y, data):
    fig = plt.figure(figsize=(20, 10))
    ax = sns.barplot(x=x, y=y, data=data, palette="Blues_d")
    ax.tick_params(axis='x', rotation=90, labelsize='20')
    ax.tick_params(axis='y', labelsize='20')
    st.pyplot(fig)


def heat_map(data):
    corr_data = data.corr()
    fig = plt.figure(figsize=(12, 8))
    ax = sns.heatmap(corr_data, vmin=-1, vmax=1)
    ax.tick_params(axis='x', rotation=90, labelsize='15')
    ax.tick_params(axis='y', labelsize='15')
    st.pyplot(fig)


def line_plot(data, data_x, data_y, data_z):
    fig = plt.figure(figsize=(20, 10))
    ax = sns.lineplot(x=data_x, y=data_y, data=data)
    ax = sns.lineplot(x=data_x, y=data_z, data=data)
    ax.tick_params(axis='x', rotation=90, labelsize='20')
    ax.tick_params(axis='y', labelsize='20')
    st.pyplot(fig)


# test = {
#     'Date': '00/00/00',
#     'Open': 1,
#     'High': 1,
#     'Low': 1,
#     'Close': 1,
#     'Volume': 1,
#     'MarketCap': 1,
#     'Crypto': "INC"
# }
# requests.post("http://127.0.0.1:5000/myapi/1",json=test).json()
# requests.delete('http://127.0.0.1:5000/myapi/542').json()
# requests.put("http://127.0.0.1:5000/myapi/1",json=test).json()
# requests.put("http://127.0.0.1:5000/myapi/1",json=test).json()


col1, col2, col3 = st.columns([1, 3, 1])
with col2:


    data = load_data()

    select_crypto = st.selectbox(
         'Selectionnez une crypto',
         (data['Crypto'].unique()))

    data = data.loc[data['Crypto'] == select_crypto]

    st.subheader("Crypto selectionnée : " + select_crypto)

    start_date = st.selectbox(
         'Date de début',
         (data['Date'].sort_index(ascending=False)))

    start_id = int(data.loc[data['Date'] == start_date]['ID'])

    end_date = st.selectbox(
         'Date de fin',
         (data[data['ID'] <= start_id]['Date'].sort_index(ascending=False)))

    end_id = int(data.loc[data['Date'] == end_date]['ID'])

    data = data.loc[data['ID'] <= start_id].loc[data['ID'] >= end_id]
    if st.checkbox('Show dataframe'):
        st.subheader('Crypto data between : ' + start_date + " and " + end_date)
        st.write(data)
        if data.shape[0] > 5:
            st.subheader('Heatmap du dataframe')
            heat_map(data.drop(columns='ID'))


col1, col2 = st.columns([1, 1])
with col1:
    st.subheader('Barplot du volume chaque jour (en dizaine de millions)')
    bar_plot(data['Date'], data['Volume'], data)
    st.subheader('En moyenne le volume était de *' + str(round((data['Volume'].mean()))) + '*')
with col2:
    st.subheader('Prix max du token chaque jour (en dollars)')
    data = data.sort_index(ascending=False)
    line_plot(data, data['Date'], data['High'], data['Low'])
    st.subheader('Le token à atteint une valeur **maximum** de *' + str(max(data['High'])) + '* dollars')
    st.subheader('Le token à atteint une valeur **minimum** de *' + str(min(data['Low'])) + '* dollars')

