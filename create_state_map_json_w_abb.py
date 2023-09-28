import pandas as pd
import random
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

right = -71
right_start = 38
spacing = 1.5
fab = 1.5

us_shapefile_path = ("https://github.com/TheCGO/KS-FlatTax/raw/main/data/" +
                     "cb_2018_us_state_20m/cb_2018_us_state_20m.shp")

gdf = gpd.GeoDataFrame.from_file(us_shapefile_path)
gdf_json = gdf.to_json()
gjson = json.loads(gdf_json)

# Remove Puerto Rico from data
del(gjson["features"][7])

# Alaska
# Fix positive longitudes
min_lat_ak = 140  # initial value that will be adjusted
min_abs_lon_ak = 180  # initial value that will be adjusted
coords_list = gjson["features"][24]["geometry"]["coordinates"]
for ind_isl, island in enumerate(coords_list):
    for ind_pnt, point in enumerate(island[0]):
        min_lat_ak = np.minimum(min_lat_ak, point[1])
        if point[0] > 0:
            gjson["features"][24]["geometry"][
                "coordinates"
            ][ind_isl][0][ind_pnt][0] = -180 - (180 - point[0])
        else:
            min_abs_lon_ak = np.minimum(min_abs_lon_ak, -point[0])

# Shrink the size of Alaska relative to its southestern most minimum lattitude
# and longitude
shrink_pct_ak = 0.78
coords_list_ak = gjson["features"][24]["geometry"]["coordinates"]
for ind_isl, island in enumerate(coords_list_ak):
    for ind_pnt, point in enumerate(island[0]):
        gjson["features"][24]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][0] = point[0] - shrink_pct_ak * (point[0] +
                                                                min_abs_lon_ak)
        gjson["features"][24]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][1] = point[1] - shrink_pct_ak * (point[1] -
                                                                min_lat_ak)


# Move Alaska closer to the mainland such that the minimum minimum absolute
# longitude and lattitude are (-127, 44)
min_lat_ak_new = 24
min_abs_lon_ak_new = 112.5
for ind_isl, island in enumerate(coords_list):
    for ind_pnt, point in enumerate(island[0]):
        gjson["features"][24]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][0] = point[0] + (min_abs_lon_ak -
                                                min_abs_lon_ak_new)
        gjson["features"][24]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][1] = point[1] - (min_lat_ak - min_lat_ak_new)


horizontal_scale = 1 # Adjust this percentage for horizontal scaling
vertical_scale = horizontal_scale * 1.6    # Adjust this percentage for vertical scaling

coords_list_ak = gjson["features"][24]["geometry"]["coordinates"]

# Calculate the center of Alaska
center_x = sum(point[0] for island in coords_list_ak[0][0]) / len(coords_list_ak[0][0])
center_y = sum(point[1] for island in coords_list_ak[0][0]) / len(coords_list_ak[0][0])

# Iterate through the coordinates and apply scaling
for ind_isl, island in enumerate(coords_list_ak):
    for ind_pnt, point in enumerate(island[0]):
        # Calculate new x and y coordinates based on scaling factors
        new_x = center_x + (point[0] - center_x) * horizontal_scale
        new_y = center_y + (point[1] - center_y) * vertical_scale
        gjson["features"][24]["geometry"]["coordinates"][ind_isl][0][ind_pnt][0] = new_x
        gjson["features"][24]["geometry"]["coordinates"][ind_isl][0][ind_pnt][1] = new_y


# Hawaii
list_ind_hi = 47
# Get minimum lattitude and minimum absolute longitude for Hawaii
min_lat_hi = 180  # initial value that will be adjusted
min_abs_lon_hi = 180  # initial value that will be adjusted
coords_list = gjson["features"][list_ind_hi]["geometry"]["coordinates"]
for ind_isl, island in enumerate(coords_list):
    for ind_pnt, point in enumerate(island[0]):
        min_lat_hi = np.minimum(min_lat_hi, point[1])
        min_abs_lon_hi = np.minimum(min_abs_lon_hi, -point[0])
# print("Minimum lattitude for Hawaii is", min_lat_hi)
# print("Minimum absolute longitude for Hawaii is", min_abs_lon_hi)

# Increase the size of Hawaii
incr_pct_hi = 0.4
coords_list_hi = gjson["features"][list_ind_hi]["geometry"]["coordinates"]
for ind_isl, island in enumerate(coords_list_hi):
    for ind_pnt, point in enumerate(island[0]):
        gjson["features"][list_ind_hi]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][0] = point[0] + incr_pct_hi * (point[0] +
                                                              min_abs_lon_hi)
        gjson["features"][list_ind_hi]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][1] = point[1] + incr_pct_hi * (point[1] -
                                                              min_lat_hi)

# Move Hawaii closer to the mainland such that the minimum minimum absolute
# longitude and lattitude are (-125, 27)
min_lat_hi_new = 25
min_abs_lon_hi_new = 104
for ind_isl, island in enumerate(coords_list):
    for ind_pnt, point in enumerate(island[0]):
        gjson["features"][list_ind_hi]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][0] = point[0] + (min_abs_lon_hi -
                                                min_abs_lon_hi_new)
        gjson["features"][list_ind_hi]["geometry"][
            "coordinates"
        ][ind_isl][0][ind_pnt][1] = point[1] - (min_lat_hi - min_lat_hi_new)

st_list_num = 2
de_coord_list = [gjson["features"][st_list_num]["geometry"]["coordinates"]]
new_box_de = [
    [
        [right + fab, 39],
        [right + fab + 3, 39],
        [right + fab + 3, 38],
        [right + fab, 38],
        [right + fab, 39]
    ]
]
de_coord_list.append(new_box_de)

gjson["features"][st_list_num]["geometry"]["coordinates"] = de_coord_list
gjson["features"][st_list_num]["geometry"]["type"] = "MultiPolygon"

# Add a state box around Washington, DC (District of Columbia) abbreviation DC
st_list_num = 35
dc_coord_list = [gjson["features"][st_list_num]["geometry"]["coordinates"]]
new_box_dc = [[
        [right + fab, 37.5],
        [right + fab + 3, 37.5],
        [right + fab + 3, 36.5],
        [right + fab, 36.5],
        [right + fab, 37.5]
]]
dc_coord_list.append(new_box_dc)
gjson["features"][st_list_num]["geometry"]["coordinates"] = dc_coord_list
gjson["features"][st_list_num]["geometry"]["type"] = "MultiPolygon"

# Add a state box around Massachusetts abbreviation MD
st_list_num = 0
md_coord_list = gjson["features"][st_list_num]["geometry"]["coordinates"]
new_box_md = [[
        [right + fab, 36],
        [right + fab + 3, 36],
        [right + fab + 3, 35],
        [right + fab, 35],
        [right + fab, 36]
]]
md_coord_list.append(new_box_md)
gjson["features"][st_list_num]["geometry"]["coordinates"] = md_coord_list

# Add a state box around Massachusetts abbreviation MA
st_list_num = 29
ma_coord_list = gjson["features"][st_list_num]["geometry"]["coordinates"]
new_box_ma = [[
        [right + fab, 34.5],
        [right + fab + 3, 34.5],
        [right + fab + 3, 33.5],
        [right + fab, 33.5],
        [right + fab, 34.5]
]]
ma_coord_list.append(new_box_ma)
gjson["features"][st_list_num]["geometry"]["coordinates"] = ma_coord_list

# Add a state box around New Jersey abbreviation NJ
st_list_num = 34
nj_coord_list = [gjson["features"][st_list_num]["geometry"]["coordinates"]]
new_box_nj = [[
        [right + fab, 33],
        [right + fab + 3, 33],
        [right + fab + 3, 32],
        [right + fab, 32],
        [right + fab, 33]
]]
nj_coord_list.append(new_box_nj)
gjson["features"][st_list_num]["geometry"]["coordinates"] = nj_coord_list
gjson["features"][st_list_num]["geometry"]["type"] = "MultiPolygon"

# Add a state box around Rhode Island abbreviation RI
st_list_num = 50
ri_coord_list = gjson["features"][st_list_num]["geometry"]["coordinates"]
new_box_ri = [[
        [right + fab, 31.5],
        [right + fab + 3, 31.5],
        [right + fab + 3, 30.5],
        [right + fab, 30.5],
        [right + fab, 31.5]
]]
ri_coord_list.append(new_box_ri)
gjson["features"][st_list_num]["geometry"]["coordinates"] = ri_coord_list


# Add a state box around Vermont abbreviation VT
st_list_num = 32
vt_coord_list = [gjson["features"][st_list_num]["geometry"]["coordinates"]]
new_box_vt = [[
        [-77 + fab, 48],
        [-77 + fab + 3, 48],
        [-77 + fab + 3, 47],
        [-77 + fab, 47],
        [-77 + fab, 48]
]]
vt_coord_list.append(new_box_vt)
gjson["features"][st_list_num]["geometry"]["coordinates"] = vt_coord_list
gjson["features"][st_list_num]["geometry"]["type"] = "MultiPolygon"

# Add a state box around New Hampshire abbreviation NH
st_list_num = 48
nh_coord_list = [gjson["features"][st_list_num]["geometry"]["coordinates"]]
new_box_nh = [[
        [-77 + fab, 46.5],
        [-77 + fab + 3, 46.5],
        [-77 + fab + 3, 45.5],
        [-77 + fab, 45.5],
        [-77 + fab, 46.5]
]]
nh_coord_list.append(new_box_nh)
gjson["features"][st_list_num]["geometry"]["coordinates"] = nh_coord_list
gjson["features"][st_list_num]["geometry"]["type"] = "MultiPolygon"


# Add state abbreviation data
your_dataframe = pd.read_csv("state_abbr.csv")
your_dataframe = pd.DataFrame(your_dataframe)



for feature in gjson["features"]:
    state_abbrev = feature["properties"]["STUSPS"]

    # Add longitude and latitude data
    ab_lon = float(your_dataframe[your_dataframe["Abbrev"] == state_abbrev]["ab_lon"].values[0])
    ab_lat = float(your_dataframe[your_dataframe["Abbrev"] == state_abbrev]["ab_lat"].values[0])
    
    # Add the longitude and latitude as separate properties
    feature["properties"]["ab_lon"] = ab_lon
    feature["properties"]["ab_lat"] = ab_lat


# export as json file
with open("state_map_w_abb.json", "w") as outfile:
    json.dump(gjson, outfile)