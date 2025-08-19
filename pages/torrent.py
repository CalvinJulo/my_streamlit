

import streamlit as st
import subprocess
import os
import time
import uuid

# --- Configuration ---
# Directory where torrents will be downloaded
DOWNLOAD_BASE_DIR = "downloads"
# File used for communication between Streamlit app and download script
STATUS_FILE = "download_status.txt"
# Temporary file to pass torrent info to the download script
TORRENT_INFO_FILE = "torrent_info.txt"
# The background download script
DOWNLOAD_SCRIPT = "download_script.py"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_BASE_DIR):
    os.makedirs(DOWNLOAD_BASE_DIR)

# Set Streamlit page configuration for wider layout
st.set_page_config(layout="wide")

st.title("Simple Torrent Downloader & Player 🚀")
st.markdown("---")

# --- Session State Initialization ---
# Initialize session state variables if they don't exist
if "download_active" not in st.session_state:
    st.session_state["download_active"] = False
if "download_finished" not in st.session_state:
    st.session_state["download_finished"] = False
if "download_progress" not in st.session_state:
    st.session_state["download_progress"] = 0
if "download_message" not in st.session_state:
    st.session_state["download_message"] = "Waiting for input..."
if "download_output_dir" not in st.session_state:
    st.session_state["download_output_dir"] = "" # Stores the unique directory of the current download

# --- Input Section ---
st.subheader("1. Enter Magnet Link or Upload Torrent File")
magnet_link = st.text_input("Paste Magnet Link here:", placeholder="magnet:?xt=urn:btih:...")
uploaded_file = st.file_uploader("Upload .torrent file", type="torrent")

if st.button("Start Download", key="start_download_button"):
    if magnet_link or uploaded_file:
        st.session_state["download_active"] = True
        st.session_state["download_finished"] = False
        st.session_state["download_progress"] = 0
        st.session_state["download_message"] = "Starting download..."
        st.session_state["download_output_dir"] = "" # Reset for new download

        # Save torrent information to a temporary file for the download script
        try:
            with open(TORRENT_INFO_FILE, "w") as f:
                if magnet_link:
                    # Write magnet link with a prefix
                    f.write(f"magnet:{magnet_link}")
                elif uploaded_file:
                    # Save the uploaded .torrent file to the downloads folder
                    # Ensure unique name to prevent conflicts
                    unique_torrent_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
                    torrent_path = os.path.join(DOWNLOAD_BASE_DIR, unique_torrent_filename)
                    with open(torrent_path, "wb") as t_f:
                        t_f.write(uploaded_file.getbuffer())
                    # Write file path with a prefix
                    f.write(f"file:{torrent_path}")
            
            # Clear previous status file content before starting new download
            if os.path.exists(STATUS_FILE):
                os.remove(STATUS_FILE)

            # Start the download script in a separate, non-blocking subprocess
            # This ensures the Streamlit UI remains responsive
            subprocess.Popen(["python", DOWNLOAD_SCRIPT, TORRENT_INFO_FILE, DOWNLOAD_BASE_DIR])
            
            st.session_state["download_message"] = "Download initiated in background. Waiting for progress updates..."
            # Force a rerun immediately to show the initial message and start polling
            st.experimental_rerun() 
            
        except Exception as e:
            st.error(f"Error preparing or starting download: {e}")
            st.session_state["download_active"] = False
    else:
        st.warning("Please enter a magnet link or upload a .torrent file.")

st.markdown("---")

# --- Download Status Section ---
st.subheader("2. Download Status")
progress_bar = st.progress(st.session_state["download_progress"])
status_text = st.empty()

# Display current status message
status_text.write(st.session_state["download_message"])

# Logic to update progress if a download is active but not finished
if st.session_state["download_active"] and not st.session_state["download_finished"]:
    # Loop to continuously check and update download status
    # This loop will cause Streamlit to rerun periodically
    while True:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                status_content = f.read().strip()
            
            if status_content.startswith("PROGRESS:"):
                try:
                    # Extract percentage and detailed message
                    parts = status_content.split(":", 1) # Split only on the first colon
                    percent_part = parts[1].split("\n")[0] # Get percentage from first line
                    percent = int(percent_part)
                    
                    st.session_state["download_progress"] = percent
                    st.session_state["download_message"] = f"Downloading: {percent}%... ({parts[1].splitlines()[1] if len(parts[1].splitlines()) > 1 else 'No details'})"
                except (ValueError, IndexError):
                    st.session_state["download_message"] = "Reading progress..."
            elif status_content.startswith("DONE:"):
                # Download finished, update state and output directory
                st.session_state["download_progress"] = 100
                st.session_state["download_message"] = "Download complete! 🎉"
                st.session_state["download_finished"] = True
                st.session_state["download_output_dir"] = status_content.split(":", 1)[1] # Get the download path
                break # Exit the polling loop as download is done
            elif status_content.startswith("ERROR:"):
                # Handle error reported by download script
                st.session_state["download_message"] = f"Error: {status_content.split(':', 1)[1]}"
                st.session_state["download_active"] = False
                st.session_state["download_finished"] = True
                break
            else:
                # Any other message from the script
                st.session_state["download_message"] = status_content

        # Update the progress bar and status text on the UI
        progress_bar.progress(st.session_state["download_progress"])
        status_text.write(st.session_state["download_message"])
        
        # If download is finished, break the polling loop
        if st.session_state["download_finished"]:
            break
        
        time.sleep(1) # Wait for 1 second before checking status again
        st.experimental_rerun() # Rerun the app to update the UI with the latest status

st.markdown("---")

# --- Playback and Local Download Section ---
# This section only appears once the download is finished
if st.session_state["download_finished"] and st.session_state["download_progress"] == 100:
    st.subheader("3. Playback & Local Download")
    output_dir_for_display = st.session_state["download_output_dir"]

    if output_dir_for_display and os.path.exists(output_dir_for_display):
        st.write(f"Files downloaded to: `{output_dir_for_display}`")
        # List all files in the unique download directory
        downloaded_files = [f for f in os.listdir(output_dir_for_display) if os.path.isfile(os.path.join(output_dir_for_display, f))]

        if downloaded_files:
            # Display each file with options to play or download
            for file_name in sorted(downloaded_files):
                file_path = os.path.join(output_dir_for_display, file_name)
                file_ext = os.path.splitext(file_name)[1].lower()

                # Use columns for better layout of file options
                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

                with col1:
                    st.write(f"📁 {file_name}")

                with col2:
                    # Provide playback options for known media types
                    if file_ext in [".mp4", ".mov", ".webm", ".ogg"]:
                        # Using a unique key for each button is crucial in Streamlit loops
                        if st.button(f"▶️ Play Video", key=f"play_video_{file_name}"):
                            st.video(file_path)
                    elif file_ext in [".mp3", ".wav", ".ogg", ".flac"]:
                        if st.button(f"🎧 Play Audio", key=f"play_audio_{file_name}"):
                            st.audio(file_path)
                    else:
                        st.write("No player available")

                with col3:
                    # Provide a download button for any file
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download",
                            data=f.read(),
                            file_name=file_name,
                            key=f"download_{file_name}"
                        )
        else:
            st.write("No files found in the download directory for this torrent.")
    else:
        st.write("Download directory not found or empty after completion.")
elif st.session_state["download_active"] and not st.session_state["download_finished"]:
    st.info("Download is in progress or pending...")
else:
    st.info("Enter a magnet link or upload a .torrent file to start your download!")

