"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""
# CMD Run Command ： streamlit run /Users/xx.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import streamlit as st
import libtorrent as lt

magnet_link = st.text_input("Paste Magnet Link here:", placeholder="magnet:?xt=urn:btih:...")

if st.button("Start Download", use_container_width=True):
    if magnet_link:
        ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        params = {}
        params = lt.parse_magnet_uri(magnet_link)
        # params['save_path'] = os.getcwd()
        params['storage_mode'] = lt.storage_mode_t.storage_mode_sparse
        handle = ses.add_torrent(params)
        st.write('Handle')
        while not handle.is_seed():
            s = handle.status()
            st.write('Progress:',s.progress)
            st.write('Velocity:',s.download_rate)

