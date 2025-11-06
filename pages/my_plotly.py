# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：
# Description： 
"""

# CMD Run Command ： streamlit run /Users/stock/st_stock.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)



import streamlit as st
import pandas as pd
import plotly.express as px



def pick_dataset(dataset_name):
        dataset_dict ={
                'iris':px.data.iris(),
                # 'absolute_import':px.data.absolute_import(),
                'carshare':px.data.carshare(),
                'election':px.data.election(),
                'election_geojson':px.data.election_geojson(),
                'experiment':px.data.experiment(), 
                'gapminder':px.data.gapminder(),
                'medals_long':px.data.medals_long(), 
                'medals_wide':px.data.medals_wide(), 
                'stocks':px.data.stocks(), 
                'tips':px.data.tips(), 
                'wind':px.data.wind() 
                
        }
        return dataset_dict[dataset_name]

dataset_list =['carshare', 'election', 'election_geojson', 'experiment', 'gapminder', 'iris', 'medals_long', 'medals_wide', 'stocks', 'tips', 'wind']

dataset = st.pills('Dataset',dataset_list)

df = pick_dataset(dataset)
# df = px.data.iris()
st.write(df.head())
st.write(df.describe())







        
    






