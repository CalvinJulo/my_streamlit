import libtorrent as lt
import time
import sys
import os
import uuid # For unique download directory names

# This script expects two command-line arguments:
# 1. Path to a file containing the magnet link or torrent file path.
# 2. Base directory where downloads should be saved.
if len(sys.argv) != 3:
    # Error if arguments are missing
    print("Error: Usage: python download_script.py <torrent_info_file> <download_base_dir>", file=sys.stderr)
    sys.exit(1)

torrent_info_file_path = sys.argv[1]
download_base_dir = sys.argv[2]
status_file_path = "download_status.txt" # Must match app.py

# Helper to write status to a file for Streamlit app to read
def write_status(message):
    try:
        with open(status_file_path, "w") as f:
            f.write(message)
    except Exception as e:
        print(f"Error writing status: {e}", file=sys.stderr)

write_status("Initializing torrent client...")

try:
    # Initialize libtorrent session
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    
    # Read torrent info from the file created by app.py
    with open(torrent_info_file_path, "r") as f:
        torrent_input = f.read().strip()

    params = {}
    if torrent_input.startswith("magnet:"):
        params = lt.parse_magnet_uri(torrent_input)
    elif torrent_input.startswith("file:"):
        torrent_file_path = torrent_input[len("file:"):]
        info = lt.torrent_info(torrent_file_path)
        params = {'ti': info}
    else:
        write_status("ERROR: Invalid input. Must be 'magnet:' or 'file:'.")
        sys.exit(1)

    # Create a unique directory for this download to avoid conflicts
    unique_download_dir = os.path.join(download_base_dir, str(uuid.uuid4()))
    if not os.path.exists(unique_download_dir):
        os.makedirs(unique_download_dir)
    
    params['save_path'] = unique_download_dir
    params['storage_mode'] = lt.storage_mode_t.storage_mode_sparse 
    
    # Add the torrent to the session
    handle = ses.add_torrent(params)

    write_status("Torrent added. Waiting for metadata...")

    # Wait for magnet link metadata to be acquired
    if not handle.has_metadata():
        while not handle.has_metadata():
            s = handle.status()
            write_status(f"Waiting for metadata... Peers: {s.num_peers}, DL: {s.download_rate/1000:.1f} KB/s")
            time.sleep(1)
        write_status("Metadata acquired. Starting download...")

    # Main download loop until complete
    while (not handle.is_seed()): 
        s = handle.status()
        progress_percent = int(s.progress * 100)
        download_speed = s.download_rate / 1000
        upload_speed = s.upload_rate / 1000

        # Simple ETA calculation
        eta_str = "N/A"
        if download_speed > 0 and handle.torrent_file():
            remaining_bytes = handle.torrent_file().total_size() - s.total_done
            eta_seconds = remaining_bytes / (s.download_rate + 0.001)
            hours, remainder = divmod(int(eta_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            eta_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        # Status message format: PROGRESS:<percent>\n<details>
        status_message = (
            f"PROGRESS:{progress_percent}\n"
            f"State: {s.state}, Peers: {s.num_peers}, "
            f"DL: {download_speed:.1f} KB/s, UL: {upload_speed:.1f} KB/s, ETA: {eta_str}"
        )
        write_status(status_message)
        
        time.sleep(1) # Pause for 1 second

    # Once download is complete, write final status and output directory
    write_status(f"DONE:{unique_download_dir}")
    print(f"Torrent download complete: {handle.name() if handle.torrent_file() else 'Unknown'}", file=sys.stderr)

except Exception as e:
    # Report any errors to the status file
    error_message = f"ERROR: Torrent download failed: {e}"
    write_status(error_message)
    print(f"Critical Error in download_script: {e}", file=sys.stderr)
    sys.exit(1)

finally:
    # Ensure the libtorrent session is shut down
    if 'ses' in locals():
        ses.abort()

