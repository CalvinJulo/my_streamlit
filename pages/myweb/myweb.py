import json
import os

file_path = os.path.abspath(__file__)
file_path = os.path.dirname(file_path)
with open(os.path.join(file_path, 'myweb.json'), 'r') as f:
    weblist = json.load(f)
