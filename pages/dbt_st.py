# -*-coding:utf-8 -*-

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import streamlit as st

import json
file_path = os.path.abspath(__file__)
file_path = os.path.dirname(file_path)

with open(os.path.join(file_path, 'dbt/exercise.json'), 'r') as f:
    exercise = json.load(f)

st.header(' The Dialectical Behavior Therapy')
st.caption(" ### Life isn't about hopes or intentions. It’s about doing. It’s about being effective.")
st.divider()

practices = {
        'Mindfulness': ['Mindful breathing', 'Wise-mind meditation'],
        'Deep relaxation': ['Cue-controlled relaxation', 'Band of light', 'Safe-place visualization'],
        'Self-observation': ['Thought defusion', 'Be mindful of your emotions without judgment'],
        'Affirmation': ['Self-affirmation'],
        'Committed action': ['Implement committed action', 'Connect to your higher power']}

practices_dict = {
    'Daily Practices': practices.keys(),
    'Today 2020-04-01': practices.values(),
    'Time 11:00 am': ['3-5 min', '3 min', '3 min', '5 times', '3 min'], }

st.dataframe(practices_dict, hide_index=True, use_container_width=True)
st.info('What time each day will you do your practices? Please write down')
tab_names = list(practices.keys())
tab_names.append('Note')
tab_list = dict()
for i, j in enumerate(st.tabs(tab_names)):
    tab_list[tab_names[i]] = j


def expander(exer):
    with st.expander(exer):
        for i in exercise[exer]:
            st.write(i)


with tab_list['Mindfulness']:
    for i in practices['Mindfulness']:
        expander(i)
with tab_list['Deep relaxation']:
    for i in practices['Deep relaxation']:
        expander(i)


with tab_list['Self-observation']:
    for i in practices['Self-observation']:
        expander(i)

with tab_list['Affirmation']:
    for i in practices['Self-observation']:
        expander(i)

with tab_list['Committed action']:
    expander('Committed action')
    expander('The serenity prayer')
    expander('Your legitimate rights')

with tab_list['Note']:
  st.image(os.path.join(file_path, 'dbt/tip.jpg')
  st.image(os.path.join(file_path, 'dbt/DBT.001.jpeg')
  st.image(os.path.join(file_path, 'dbt/DBT.002.jpeg')
  st.image(os.path.join(file_path, 'dbt/DBT.003.jpeg')
  st.image(os.path.join(file_path, 'dbt/DBT.004.jpeg')


st.divider()
st.subheader('Depression & Bipolar Disorder')
st.divider()
st.subheader('Sadhguru & Yoga')
st.divider()
st.subheader('八部金刚功')
st.divider()


