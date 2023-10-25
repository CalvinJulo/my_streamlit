# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""
# CMD Run Command ： streamlit run /Users/xx.py --server.port 8501

import streamlit as st
import subprocess
import os
import random

file_path = os.path.abspath(__file__)
file_path = os.path.dirname(file_path)
yi_path = os.path.join(file_path, 'zhouyi/st_yi.py')

st.write('hello world')
st.write(file_path)
subprocess.run(["python",yi_path])
