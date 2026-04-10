#!/usr/bin/env python3
"""Generate data.json from metal_friday.csv."""
import csv, json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).parent
CSV = ROOT / "metal_friday.csv"
OUT = ROOT / "data.json"

with open(CSV, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

editions = OrderedDict()
for r in rows:
    key = (r["date"], r["curator"])
    if key not in editions:
        editions[key] = []
    editions[key].append({
        "artist": r["artist"],
        "track": r["track"],
        "genre": r["genre"],
        "youtube_url": r.get("youtube_url", ""),
        "youtube_music_url": r.get("youtube_music_url", ""),
        "spotify_url": r.get("spotify_url", ""),
        "bandcamp_url": r.get("bandcamp_url", ""),
        "soundcloud_url": r.get("soundcloud_url", ""),
        "tidal_url": r.get("tidal_url", ""),
    })

edition_list = sorted(
    [{"date": d, "curator": c, "tracks": t} for (d, c), t in editions.items()],
    key=lambda e: e["date"],
    reverse=True,
)

artists = {r["artist"] for r in rows}
genres = {r["genre"] for r in rows}
data = {
    "editions": edition_list,
    "stats": {
        "total_editions": len(edition_list),
        "total_tracks": len(rows),
        "unique_artists": len(artists),
        "unique_genres": len(genres),
        "date_range": [rows[-1]["date"], rows[0]["date"]] if rows else [],
    },
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Generated {OUT}: {len(edition_list)} editions, {len(rows)} tracks")
