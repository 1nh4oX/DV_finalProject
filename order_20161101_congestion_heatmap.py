import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
try:
    import folium
    from folium.plugins import HeatMap, HeatMapWithTime
except ImportError:  # Folium is optional; we can still render the static map
    folium = None
    HeatMap = None
    HeatMapWithTime = None


DATA_FILE = Path("original/order_20161101.csv")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
ASSUME_GCJ02_INPUT = True  # Raw data is likely GCJ-02 (Mars) coordinates.


def out_of_china(lng, lat):
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)


def transform_lat(x, y):
    ret = (
        -100.0
        + 2.0 * x
        + 3.0 * y
        + 0.2 * y * y
        + 0.1 * x * y
        + 0.2 * math.sqrt(abs(x))
    )
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def transform_lng(x, y):
    ret = (
        300.0
        + x
        + 2.0 * y
        + 0.1 * x * x
        + 0.1 * x * y
        + 0.1 * math.sqrt(abs(x))
    )
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    a = 6378245.0
    ee = 0.00669342162296594323
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrt_magic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrt_magic * math.cos(radlat) * math.pi)
    mlat = lat - dlat
    mlng = lng - dlng
    return mlng, mlat


def convert_gcj02_columns(df):
    if not ASSUME_GCJ02_INPUT:
        return df
    df = df.copy()
    for prefix in ("start", "end"):
        lng_col = f"{prefix}_long"
        lat_col = f"{prefix}_lat"
        coords = df[[lng_col, lat_col]].to_numpy()
        converted = np.array([gcj02_to_wgs84(lng, lat) for lng, lat in coords])
        df[lng_col] = converted[:, 0]
        df[lat_col] = converted[:, 1]
    return df


def haversine_km(lat1, lon1, lat2, lon2):
    """Return the great-circle distance in kilometers (vectorized)."""
    r = 6371.0  # Earth radius in km
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return r * c


def load_with_metrics(path):
    df = pd.read_csv(path)
    df = convert_gcj02_columns(df)
    df["duration_min"] = (df["end_time"] - df["start_time"]) / 60
    df = df[df["duration_min"] > 0]
    df["distance_km"] = haversine_km(
        df["start_lat"],
        df["start_long"],
        df["end_lat"],
        df["end_long"],
    )
    df = df[df["distance_km"] > 0.05]
    df["speed_kmh"] = df["distance_km"] / (df["duration_min"] / 60)
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["speed_kmh"])
    df["mid_lat"] = (df["start_lat"] + df["end_lat"]) / 2
    df["mid_long"] = (df["start_long"] + df["end_long"]) / 2
    # Higher congestion score for slower trips, cap to reduce outliers.
    df["congestion_score"] = np.clip(40 - df["speed_kmh"], 0, 40)
    max_score = df["congestion_score"].max()
    if max_score > 0:
        df["congestion_weight"] = df["congestion_score"] / max_score
    else:
        df["congestion_weight"] = 0
    return df


def plot_heatmap(df):
    plt.figure(figsize=(8, 8))
    hb = plt.hexbin(
        df["mid_long"],
        df["mid_lat"],
        C=df["congestion_score"],
        reduce_C_function=np.mean,
        gridsize=40,
        cmap="inferno",
        mincnt=5,
    )
    plt.colorbar(hb, label="Average congestion score (lower speed = worse)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Didi congestion heatmap – 2016-11-01")
    plt.tight_layout()
    out_path = OUTPUT_DIR / "order_20161101_congestion_heatmap.png"
    plt.savefig(out_path, dpi=200)
    plt.close()
    return out_path


def create_folium_map(df):
    if folium is None or HeatMap is None:
        return None

    center = [df["mid_lat"].mean(), df["mid_long"].mean()]
    fmap = folium.Map(location=center, zoom_start=12, tiles="cartodbpositron")
    heat_data = df[["mid_lat", "mid_long", "congestion_weight"]].values.tolist()
    HeatMap(
        heat_data,
        radius=13,
        blur=18,
        max_zoom=15,
        min_opacity=0.3,
    ).add_to(fmap)
    out_path = OUTPUT_DIR / "order_20161101_congestion_map.html"
    fmap.save(out_path)
    return out_path


def create_time_heatmap(df, freq="1h", min_samples=25):
    if folium is None or HeatMapWithTime is None:
        return None

    df = df.copy()
    df["start_dt"] = pd.to_datetime(df["start_time"], unit="s", utc=True).dt.tz_convert("Asia/Shanghai")
    df["time_bin"] = df["start_dt"].dt.floor(freq)

    # Build heatmap frames per time window.
    frames = []
    labels = []
    for bin_time, group in df.groupby("time_bin"):
        if len(group) < min_samples:
            continue
        frames.append(group[["mid_lat", "mid_long", "congestion_weight"]].values.tolist())
        labels.append(bin_time.strftime("%Y-%m-%d %H:%M"))

    if not frames:
        return None

    center = [df["mid_lat"].mean(), df["mid_long"].mean()]
    fmap = folium.Map(location=center, zoom_start=12, tiles="cartodbpositron")
    HeatMapWithTime(
        frames,
        index=labels,
        radius=13,
        auto_play=False,
        max_opacity=0.8,
        min_opacity=0.3,
    ).add_to(fmap)
    out_path = OUTPUT_DIR / "order_20161101_congestion_time_map.html"
    fmap.save(out_path)
    return out_path


def main():
    df = load_with_metrics(DATA_FILE)
    out_path = plot_heatmap(df)
    print(f"Saved congestion heatmap to {out_path}")
    folium_out = create_folium_map(df)
    if folium_out:
        print(f"Saved interactive congestion map to {folium_out}")
    else:
        print("Folium not installed, skipped interactive map (pip install folium).")
    time_out = create_time_heatmap(df)
    if time_out:
        print(f"Saved time-sliced congestion map to {time_out}")
    elif folium is not None:
        print("Not enough data per time bin to build time slider map.")


if __name__ == "__main__":
    main()
