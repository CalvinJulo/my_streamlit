# -*-coding:utf-8 -*-

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import streamlit as st
from pages.analysis.methods import *


st.write('# 数据分析思维和方法')
question = ['情景描述', '将复杂问题简单化', '行业分析', '多角度思考', '对比', '如何分析原因',
            'A和B有什么关系', '留存和流失分析', '用户价值分类', '用户行为分析', '转化分析']

st.table([question[3*i:3*i+3] for i in range(4)])


tab_names = method()
tab_list = dict()
for i, j in enumerate(st.tabs(tab_names)):
    tab_list[tab_names[i]] = j


with tab_list['5W2H分析']:
    method_title, method_capt, method_cases = wh_analysis()
    st.write(f'## {method_title}')
    st.write(method_capt[0],method_capt[1])
    st.caption(method_capt[2])
    with st.expander('case1'):
        st.write(f"#### {method_cases['case1']['title']}")
        st.write(f"{method_cases['case1']['context']}")
    with st.expander('case2'):
        st.write(f"#### {method_cases['case2']['title']}")
        st.write(f"{method_cases['case2']['context']}")


with tab_list['逻辑树分析']:
    method_title, method_capt, method_cases = logictree_analysis()
    st.write(f'## {method_title}')
    st.graphviz_chart(method_cases['graphviz_chart'])
    st.write(method_capt)
    with st.expander('费米问题'):
        st.write(f"#### {method_cases['feimi']['title']}")
        st.write(method_cases['feimi']['intro'][0])
        st.caption(method_cases['feimi']['intro'][1:])
        st.write(f"{method_cases['feimi']['context']}")


with tab_list['行业分析PEST']:
    method_title, method_capt, method_cases = industry_pest_analysis()
    st.write(f'## {method_title}')
    st.write(method_capt)
    with st.expander('PEST分析方法'):
        for i, j in enumerate(st.columns(4)):
            with j:
                name = list(method_cases.keys())[i]
                st.write(name)
                st.write(method_cases[name])


with tab_list['行业分析SWOT']:
    method_title, method_capt, method_cases = industry_swot_analysis()
    st.write(f'## {method_title}')
    st.write(method_capt)
    with st.expander('SWOT分析方法'):
        for i, j in enumerate(st.columns(4)):
            with j:
                name = list(method_cases.keys())[i]
                st.write(name)
                st.write(method_cases[name])

with tab_list['多维度拆解分析']:
    method_title, method_capt, method_cases = multidimensional_analysis()
    st.write(f'## {method_title}')
    for i in method_capt:
        st.write(i)
    for i in method_cases:
        with st.expander(i):
            st.write(method_cases[i])



with tab_list['对比分析']:
    method_title, method_capt, method_cases = comparative_analysis()
    st.write(f'## {method_title}')
    for i, j in enumerate(st.columns(3)):
        with j:
            name = list(method_cases.keys())[i]
            st.write(name)
            st.write(method_cases[name])

with tab_list['假设检验分析']:
    method_title, method_capt, method_cases = hypothesis_analysis()
    st.write(f'## {method_title}')
    for i in method_capt:
        st.write(i)
    with st.expander('企业管理'):
        st.write(method_cases['企业管理'])

with tab_list['相关分析']:
    method_title, method_capt, method_cases = correlation_analysis()
    st.write(f'## {method_title}')
    for i in method_capt:
        st.write(i)
    st.write(method_cases)

with tab_list['群组分析']:
    method_title, method_capt, method_cases = cluster_analysis()
    st.write(f'## {method_title}')
    st.write(method_capt)
    st.write(method_cases)


with tab_list['RFM分析']:
    method_title, method_capt, method_cases = rfm_analysis()
    st.write(f'## {method_title}')
    st.write(method_capt['RFM缩写'])
    for i, j in enumerate(st.columns(3)):
        with j:
            name = list(method_capt.keys())[1:][i]
            st.write(name)
            st.write(method_capt[name])
    with st.expander('RFM分析使用'):
        st.write(method_cases)

with tab_list['AARRR模型分析']:
    method_title, method_capt, method_cases = aarrr_analysis()
    st.write(f'## {method_title}')
    st.write(method_capt)
    with st.expander('AARRR模型分析'):
        st.write(method_cases)

with tab_list['漏斗分析']:
    method_title, method_capt, method_cases = funnel_analysis()
    st.write(f'## {method_title}')
    for i in method_capt:
        st.write(i)
    st.dataframe(method_cases['举例'])
