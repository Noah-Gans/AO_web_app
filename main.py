import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import math
import geopandas as gpd  # Import geopandas

# Load the data
state_file = "data/us-state-boundaries.geojson"
cd_file = "data/CD.geojson"


@st.cache
def data_creation():
    state_gdf = gpd.read_file(state_file)
    cd_gdf = gpd.read_file(cd_file)
    state_gdf["coordinates"] = state_gdf["geometry"].apply(get_coordinates)
    state_gdf["fill_color"] = state_gdf["objectid"].apply(color_scale)
    cd_gdf["coordinates"] = cd_gdf["geometry"].apply(get_coordinates)
    cd_gdf["fill_color"] = cd_gdf["GEOID"].apply(color_scale2)

    states = pdk.Layer(
    "PolygonLayer",
    data=state_gdf,
    id="geojson",
    opacity=0.1,
    get_polygon="coordinates",
    filled=True,
    stroked=True,
    wireframe = True,
    lineWidthUnits= 'pixels',
    lineWidthMaxPixels = 10000,
    lineWidthScale = 1000,
    get_fill_color="fill_color",
    get_line_color= [80, 80, 80],
    highlight_color=[0, 0, 0, 128],
    auto_highlight=True,
    pickable=True,
    )

    congresional_district = pdk.Layer(
    "PolygonLayer",
    data=cd_gdf,
    id="geojson",
    opacity=0.5,
    get_polygon="coordinates",
    filled=True,
    stroked=True,
    wireframe = True,
    lineWidthUnits= 'pixels',
    lineWidthMaxPixels = 10000,
    lineWidthScale = 1000,
    get_fill_color="fill_color",
    get_line_color= [80, 80, 80],
    highlight_color=[0, 0, 0, 128],
    auto_highlight=True,
    pickable=True,
    )

    tooltip = {"html": "{name}"}
# Create the map
    st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-95.4,
        zoom=3,
        pitch=0,
    ),
    effects=[lighting_effect],
    map_style=pdk.map_styles.LIGHT,
    tooltip=tooltip,
    layers=[congresional_district]
    ))

COLOR_RANGE = [
    [255, 245, 188],  # PaleGoldenRod
    [250, 235, 168],  # Khaki
    [250, 225, 128],  # LightGoldenrod
    [240, 190, 40],   # Goldenrod
    [255, 225, 0],    # Gold
    [255, 180, 0],    # Orange
    [255, 140, 0],    # DarkOrange
    [210, 120, 80],   # Peru
    [210, 95, 50],    # Chocolate
    [165, 80, 40],    # SaddleBrown
    [190, 100, 60],   # Sienna
    [255, 240, 0],    # Additional color 1 (More Yellow)
    [255, 200, 0],    # Additional color 2 (Yellow)
]
sunlight = {
    "@@type": "_SunLight",
    "timestamp": 1564696800000,  # Date.UTC(2019, 7, 1, 22),
    "color": [255, 255, 255],
    "intensity": 1.0,
    "_shadow": True,
}
ambient_light = {"@@type": "AmbientLight", "color": [255, 255, 255], "intensity": 1.0}
lighting_effect = {
    "@@type": "LightingEffect",
    "shadowColor": [0, 0, 0, 0.5],
    "ambientLight": ambient_light,
    "directionalLights": [sunlight],
}

# Breaks for the color scale
BREAKS = [1, 4.92,  8.84, 12.76, 16.68, 20.6, 24.52, 28.44, 32.36, 36.28, 40.2,  44.12, 48.04]

def color_scale(val):
    for i, b in enumerate(BREAKS):
        if int(val) < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]

def color_scale2(val):
    for i, b in enumerate(BREAKS):
        if int(val)/500 < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]

def get_coordinates(geom):
   
    if geom.geom_type == 'Polygon':
        return geom.exterior.coords[:]
    elif geom.geom_type == 'MultiPolygon':
        return [polygon.exterior.coords[:] for polygon in geom]
    else:
        return None

# Calculate coordinates and fill color



# Set up the map layer


data_creation()
