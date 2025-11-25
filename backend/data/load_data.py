import os
import django
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()



import json
import pandas as pd
from songs.models import Playlist

FILE_PATH = 'data/playlist.json'

with open(FILE_PATH, "r") as f:
    raw = json.load(f)

# Convert JSON maps → DataFrame
df = pd.DataFrame({k: pd.Series(v) for k, v in raw.items()})

# Normalize column names
df.columns = [col.lower() for col in df.columns]

for _, row in df.iterrows():
    Playlist.objects.create(
        song_id=row.get("id"),
        title=row.get("title"),
        danceability=row.get("danceability"),
        energy=row.get("energy"),
        mode=row.get("mode"),
        acousticness=row.get("acousticness"),
        tempo=row.get("tempo"),
        duration_ms=row.get("duration_ms"),
        num_sections=row.get("num_sections"),
        num_segments=row.get("num_segments"),
    )

print("Data Loaded Successfully!")
