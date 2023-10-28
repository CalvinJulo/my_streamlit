# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description： 爬取股票信息，用streamlit进行可视化
"""

# CMD Run Command ： streamlit run /Users/stock/st_stock.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from stock import stock_info
from stock import tonghuashun_stock

st.set_page_config(page_title="股票基本面分析 App", page_icon="🧊", layout="wide")

st.write('### Stock Basic Analysis')
stock_code = st.text_input('Input Stock Code', '000001')

if st.button('Code'):
    st.text(stock_code)
    tonghuashun_url = 'http://stockpage.10jqka.com.cn/' + stock_code
    components.iframe(tonghuashun_url, height=600, width=1200, scrolling=True)


if st.button('From cninfo Get Stock Profile '):
    profile = stock_info.stock_profile(stock_code)
    st.write(profile)
    executives = stock_info.stock_executives(stock_code)
    st.table(executives)
    st.write('### Main Indicator')
    indicator_data = pd.DataFrame(stock_info.stock_indicators_data(stock_code))
    st.table(indicator_data.astype('str'))
    st.write('### Finance Data')
    finance_data = pd.DataFrame(stock_info.stock_finance_data(stock_code))
    st.table(finance_data.astype('str'))
if st.button('From cninfo Get Anniversary Report '):
    reports = stock_info.periodic_report(stock_code)
    st.table(reports)

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    if st.button('From tonghuashun download Main Indicator'):
        st.write(tonghuashun_stock.get_excel_url(code=stock_code, export='main', type_='year'))
with col2:
    if st.button('From tonghuashun download Income'):
        st.write(tonghuashun_stock.get_excel_url(code=stock_code, export='benefit', type_='year'))
with col3:
    if st.button('From tonghuashun download balance'):
        st.write(tonghuashun_stock.get_excel_url(code=stock_code, export='debt', type_='year'))
with col4:
    if st.button('From tonghuashun download cash flow'):
        st.write(tonghuashun_stock.get_excel_url(code=stock_code, export='cash', type_='year'))
