# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description： 易经研究
"""

# CMD Run Command ： streamlit run /Users/calvinish/Documents/Py3/案例/Yi/st_yi.py --server.port 8501
import pandas as pd
import Yi
import streamlit as st

st.set_page_config(page_title="易经 App", page_icon="🧊", layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"})

sessionState_List = ['gua8_data', 'gua64_data', 'gua8_code_name', 'gua64_code_name']
for i in sessionState_List:
    if i not in st.session_state:
        st.session_state[i] = ''

st.session_state.gua8_data = Yi.gua8_data
st.session_state.gua8_code_name = Yi.gua8_code_name
st.session_state.gua64_data = Yi.gua64_data
st.session_state.gua64_code_name = Yi.gua64_code_name

gua8_data = st.session_state.gua8_data
gua8_code_name = st.session_state.gua8_code_name
gua64_data = st.session_state.gua64_data
gua64_code_name = st.session_state.gua64_code_name

# 起卦
st.write('***')
st.write('# 起卦')
yao_name = ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻']
yao_value_list = ['少阳', '少阴', '老阳', '老阴']


new_qi_gua = {}
for i, j in enumerate(st.columns(6)):
    with j:
        new_qi_gua[yao_name[i]] = st.selectbox(yao_name[i], options=yao_value_list)


yao_attr_list = new_qi_gua.values()
yao_attr_list = list(yao_attr_list)
m_qi_gua = Yi.make_qi_gua(yao_attr_list)
qi_gua = m_qi_gua
st.write(qi_gua)


def show_jie_gua64(qi_gua):
    ben_gua_name = gua64_code_name[qi_gua['本卦卦象']]
    bian_gua_name = gua64_code_name[qi_gua['变卦卦象']]
    ben_gua_profile = Yi.gua_profile(ben_gua_name)
    bian_gua_profile = Yi.gua_profile(bian_gua_name)
    bian_yao_list = qi_gua['本卦变爻']
    show_jie_gua = dict()
    li_sjq = ['卦辞', '上爻爻辞', '五爻爻辞', '四爻爻辞', '三爻爻辞', '二爻爻辞', '初爻爻辞']
    show_jie_gua['变爻'] = [f"{list(bian_yao_list).count('1')}"]+list(bian_yao_list)
    show_jie_gua['本卦'] = [ben_gua_profile['本卦']]+[ben_gua_profile[i] for i in yao_name]
    show_jie_gua['本卦辞'] = [gua64_data[ben_gua_name][i] for i in li_sjq]
    show_jie_gua['变卦'] = [bian_gua_profile['本卦']]+[bian_gua_profile[i] for i in yao_name]
    show_jie_gua['变卦辞'] = [gua64_data[bian_gua_name][i] for i in li_sjq]
    return show_jie_gua


st.dataframe(show_jie_gua64(qi_gua))
zhan_gua_intro, expl = Yi.zhan_gua(qi_gua)
st.write('解卦')
st.write(zhan_gua_intro)
st.write(expl)


st.write('***')
st.write('### 随机起卦')
if 'r_qi_gua_s' not in st.session_state:
    st.session_state['r_qi_gua_s'] = ''
if st.button('随机起卦'):
    r_qi_gua = Yi.random_qi_gua()
    st.session_state.r_qi_gua_s = r_qi_gua

if st.session_state.r_qi_gua_s:
    r_qi_gua = st.session_state.r_qi_gua_s
    st.dataframe(show_jie_gua64(r_qi_gua))
    r_zhan_gua_intro, r_expl = Yi.zhan_gua(r_qi_gua)
    st.write('解卦')
    st.write(r_zhan_gua_intro)
    st.write(r_expl)




st.write('***')
# 起始
gua64_list = list(gua64_data.keys())
st.table([gua64_list[8*i:8*i+8] for i in range(8)])
with st.expander('口诀'):
    st.write(Yi.phrase()[0])
    col1, col2 = st.columns(2)
    col1.write(Yi.phrase()[1])
    col2.write(Yi.phrase()[2])


# 输入卦
st.write('## 卦搜索')
gua64 = st.text_input('卦搜索', '乾')


def show_gua64_info(gua64):
    gua64_profile = Yi.gua_profile(gua64)
    yao_info = Yi.yao_info(gua64)
    li0 = ['卦辞', '上爻爻辞', '五爻爻辞', '四爻爻辞', '三爻爻辞', '二爻爻辞', '初爻爻辞']
    li1 = ['卦象辞', '上爻象辞', '五爻象辞', '四爻象辞', '三爻象辞', '二爻象辞', '初爻象辞']
    gua64_info = dict()
    gua64_info['本卦'] = gua64
    gua64_info['卦序号'] = gua64_data[gua64]['卦序号']
    gua64_info['彖辞'] = gua64_data[gua64]['彖辞']
    gua64_info['上下卦'] = gua64_profile['上卦'] + gua64_profile['下卦'] + gua64
    gua64_info['卦象'] = [gua64_info['上下卦']]+[gua64_profile[i] for i in yao_name]
    gua64_info['卦辞'] = [gua64_data[gua64][i] for i in li0]
    gua64_info['象辞'] = [gua64_data[gua64][i] for i in li1]
    gua64_info['爻位'] = ['乘比得应']+[i for i in yao_info.values()]
    for i in ['综卦', '错卦', '交互卦']:
        name = gua64_profile[i]
        gua64_info[i] = [name] + [Yi.gua_profile(name)[i] for i in yao_name]
    if gua64 in ['乾', '坤']:
        for i in ['文言', '用爻爻辞', '用爻象辞']:
            gua64_info[i] = gua64_data[gua64][i]
    return gua64_info


st.dataframe(show_gua64_info(gua64))

gua64_1 = st.text_input('卦搜索1', '乾')
st.dataframe(show_gua64_info(gua64_1))
gua64_2 = st.text_input('卦搜索2', '乾')
st.dataframe(show_gua64_info(gua64_2))
