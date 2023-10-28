# -*-coding:utf-8 -*-

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import os

file_path = os.path.abspath(__file__)
file_path = os.path.dirname(file_path)
with open(os.path.join(file_path, 'myweb/myweb.json'), 'r') as f:
    weblist = json.load(f)


web_df = pd.DataFrame(weblist).transpose()
web_df['tab'] = False
disabled_list = web_df.columns.to_list().remove('tab')
if disabled_list is None:
    disabled_list = []
edited_df = st.data_editor(web_df,
                           column_config={"url": st.column_config.LinkColumn("url")},
                           hide_index=True, disabled=disabled_list)


select_list = edited_df.loc[edited_df["tab"] == True]
select_name = select_list['name'].to_list()
select_url = select_list['url'].to_list()
st.write('I am here')
for i, j in enumerate(st.tabs(select_name)):
    with j:
        components.iframe(select_url[i], width=900, height=500, scrolling=True)

# url = 'https://whoer.net/'
# tab1, tab2 =st.tabs(['tab1','tab2'])
# components.iframe(url, width=900, height=500, scrolling=True)
# with tab1:
#     components.iframe(url, width=900, height=500, scrolling=True)






