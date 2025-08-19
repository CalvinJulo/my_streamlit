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
st.write('torrent')


import subprocess
import os
import time
import uuid # For unique directory names

# --- Configuration ---
DOWNLOAD_BASE_DIR = "downloads" # Where torrents will be downloaded
STATUS_FILE = "download_status.txt" # File for communication
TORRENT_INFO_FILE = "torrent_info.txt" # Temp file for torrent data
DOWNLOAD_SCRIPT = "download_script.py" # The background script

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_BASE_DIR):
    os.makedirs(DOWNLOAD_BASE_DIR)

st.title("Simple Torrent Downloader ☁️")
st.markdown("---")

# --- Session State Initialization ---
# Streamlit's session_state helps maintain variables across reruns
if "download_active" not in st.session_state:
    st.session_state["download_active"] = False
if "download_finished" not in st.session_state:
    st.session_state["download_finished"] = False
if "download_progress" not in st.session_state:
    st.session_state["download_progress"] = 0
if "download_message" not in st.session_state:
    st.session_state["download_message"] = "Waiting for input..."
if "download_output_dir" not in st.session_state:
    st.session_state["download_output_dir"] = ""

# --- Input Section ---
st.subheader("1. Enter Magnet Link or Upload Torrent File")
magnet_link = st.text_input("Paste Magnet Link:", placeholder="magnet:?xt=urn:btih:...")
uploaded_file = st.file_uploader("Upload .torrent file", type="torrent")

if st.button("Start Download", use_container_width=True):
    if magnet_link or uploaded_file:
        st.session_state["download_active"] = True
        st.session_state["download_finished"] = False
        st.session_state["download_progress"] = 0
        st.session_state["download_message"] = "Starting download..."
        st.session_state["download_output_dir"] = "" # Reset for new download

        try:
            # Prepare torrent info for the background script
            with open(TORRENT_INFO_FILE, "w") as f:
                if magnet_link:
                    f.write(f"magnet:{magnet_link}")
                elif uploaded_file:
                    # Save uploaded file to temp location for download script
                    temp_torrent_path = os.path.join(DOWNLOAD_BASE_DIR, f"{uuid.uuid4()}_{uploaded_file.name}")
                    with open(temp_torrent_path, "wb") as t_f:
                        t_f.write(uploaded_file.getbuffer())
                    f.write(f"file:{temp_torrent_path}")
            
            # Clear previous status to ensure fresh start
            if os.path.exists(STATUS_FILE):
                os.remove(STATUS_FILE)

            # Start the download script in a non-blocking subprocess.
            # This is how the background download runs without freezing the UI.
            subprocess.Popen(["python", DOWNLOAD_SCRIPT, TORRENT_INFO_FILE, DOWNLOAD_BASE_DIR])
            
            st.session_state["download_message"] = "Download initiated. Checking progress..."
            st.experimental_rerun() # Rerun immediately to show initial message
            
        except Exception as e:
            st.error(f"Error starting download: {e}")
            st.session_state["download_active"] = False
    else:
        st.warning("Please enter a magnet link or upload a .torrent file.")

st.markdown("---")

# --- Download Status Section ---
st.subheader("2. Download Status")
progress_bar = st.progress(st.session_state["download_progress"])
status_text = st.empty()

status_text.write(st.session_state["download_message"])

# This loop continuously checks the status file for updates.
# Streamlit reruns every few seconds, allowing this to update the UI.
if st.session_state["download_active"] and not st.session_state["download_finished"]:
    while True:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                status_content = f.read().strip()
            
            if status_content.startswith("PROGRESS:"):
                try:
                    # Extract percentage and message from status file
                    parts = status_content.split(":", 1)
                    percent_line = parts[1].split("\n")[0]
                    percent = int(percent_line)
                    st.session_state["download_progress"] = percent
                    st.session_state["download_message"] = f"Downloading: {percent}% ({parts[1].splitlines()[1] if len(parts[1].splitlines()) > 1 else '...'})"
                except (ValueError, IndexError):
                    st.session_state["download_message"] = "Reading progress..."
            elif status_content.startswith("DONE:"):
                # Download complete! Store the output directory.
                st.session_state["download_progress"] = 100
                st.session_state["download_message"] = "Download complete! 🎉"
                st.session_state["download_finished"] = True
                st.session_state["download_output_dir"] = status_content.split(":", 1)[1]
                break # Exit polling loop
            elif status_content.startswith("ERROR:"):
                # Handle error from background script
                st.session_state["download_message"] = f"Error: {status_content.split(':', 1)[1]}"
                st.session_state["download_active"] = False
                st.session_state["download_finished"] = True
                break
            else:
                st.session_state["download_message"] = status_content # Generic status

        progress_bar.progress(st.session_state["download_progress"])
        status_text.write(st.session_state["download_message"])
        
        if st.session_state["download_finished"]:
            break # Stop polling once done
        
        time.sleep(1) # Wait a bit before checking again
        st.experimental_rerun() # Force rerun to update UI

st.markdown("---")

# --- Playback and Local Download Section ---
if st.session_state["download_finished"] and st.session_state["download_progress"] == 100:
    st.subheader("3. Playback & Local Download")
    output_dir_for_display = st.session_state["download_output_dir"]

    if output_dir_for_display and os.path.exists(output_dir_for_display):
        st.write(f"Files saved to: `{output_dir_for_display}`")
        downloaded_files = [f for f in os.listdir(output_dir_for_display) if os.path.isfile(os.path.join(output_dir_for_display, f))]

        if downloaded_files:
            for file_name in sorted(downloaded_files):
                file_path = os.path.join(output_dir_for_display, file_name)
                file_ext = os.path.splitext(file_name)[1].lower()

                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

                with col1:
                    st.write(f"📁 {file_name}")

                with col2:
                    # Provide playback for common media types
                    if file_ext in [".mp4", ".mov", ".webm", ".ogg"]:
                        if st.button(f"▶️ Video", key=f"play_video_{file_name}"):
                            st.video(file_path)
                    elif file_ext in [".mp3", ".wav", ".ogg", ".flac"]:
                        if st.button(f"🎧 Audio", key=f"play_audio_{file_name}"):
                            st.audio(file_path)
                    else:
                        st.write("No player")

                with col3:
                    # Allow downloading any file
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download",
                            data=f.read(),
                            file_name=file_name,
                            key=f"download_{file_name}"
                        )
        else:
            st.info("No files found in the download directory.")
    else:
        st.info("Download directory not found or empty.")
elif st.session_state["download_active"] and not st.session_state["download_finished"]:
    st.info("Download is in progress or pending...")
else:
    st.info("Enter a magnet link or upload a .torrent file to start!")


