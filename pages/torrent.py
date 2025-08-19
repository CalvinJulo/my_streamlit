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

magnet_link = st.text_input("Paste Magnet Link:", placeholder="magnet:?xt=urn:btih:...")
uploaded_file = st.file_uploader("Upload .torrent file", type="torrent")


def download_magnet_link(magnet_link, download_path='.'):
    ses = lt.session()
    ses.listen_on(6881, 6891)  
    params = {}
    params['save_path']=download_path
    params['storage_mode']=lt.storage_mode_t.storage_mode_sparse
    handle = lt.add_magnet_uri(ses, magnet_link, params)
    
    st.write(f"Downloading: {handle.name()}")
    while not handle.is_seed():
        s = handle.status()
        st.write(f"\rProgress: {s.progress * 100:.2f}% | "
              f"Download speed: {s.download_rate / 1000:.2f} kB/s | "
              f"Peers: {s.num_peers} | "
              #f"ETA: {s.eta / 60 if s.eta is not None else 'N/A':.2f} min", end=""
                )
    st.write("\nDownload complete!")

# Example usage (replace with your magnet link)
magnet_link_example = magnet_link
st.write('start...')
download_magnet_link(magnet_link_example, './downloads')
st.write('Done')

