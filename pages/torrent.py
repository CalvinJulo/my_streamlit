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


magnet_link = 'magnet:?xt=urn:btih:f9de776f6eee9386892b7ed4ef29c373fd705aaa&dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1dygod.org.%e7%a2%9f%e4%b8%ad%e8%b0%8d8%ef%bc%9a%e6%9c%80%e7%bb%88%e6%b8%85%e7%ae%97.2025.HD.1080P.%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97.mkv&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce'

def download_magnet_link(magnet_link, download_path='.'):
    
    # Create a session
    ses = lt.session()
    ses.listen_on(6881, 6891)  # Listen on a port range
    
    # Set up the download parameters
    params = {
        'save_path': download_path,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
    }
    
    # Add the magnet link to the session
    handle = lt.add_magnet_uri(ses, magnet_link, params)
    
    st.write(f"Downloading: {handle.name()}")
    
    # Loop until the download is complete
    while not handle.is_seed():
        s = handle.status()
        
        # Print download status
        st.write(f"\rProgress: {s.progress * 100:.2f}% | "
              f"Download speed: {s.download_rate / 1000:.2f} kB/s | "
              f"Peers: {s.num_peers} | "
              f"ETA: {s.eta / 60 if s.eta is not None else 'N/A':.2f} min", end="")
        
    
    st.write("\nDownload complete!")

# Example usage (replace with your magnet link)
magnet_link_example = magnet_link
st.write('start...')
download_magnet_link(magnet_link_example, './downloads')
st.write('Done')

