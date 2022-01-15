# https://spire.com/tutorial/spire-weather-tutorial-intro-to-processing-grib2-data-with-python/

import xarray as xr

file = './grib/nam.t00z.conusnest.hiresf00.tm00.grib2'

data = xr.open_dataset(file, engine="cfgrib")
# print(data)

for v in data:
    print("{}, {}, {}".format(v, data[v].attrs["long_name"], data[v].attrs["units"]))

print(data.get('tp'))

df = data.to_dataframe()
print(df)

# latitudes = df.index.get_level_values("lat_0")
# longitudes = df.index.get_level_values("lon_0")

# map_function = lambda lon: (lon - 360) if (lon > 180) else lon
# remapped_longitudes = longitudes.map(map_function)

# df["longitude"] = remapped_longitudes
# df["latitude"] = latitudes

# min_lat = 10.2
# max_lat = 48.9
# min_lon = -80
# max_lon = -8.3

# lat_filter = (df["latitude"] >= min_lat) & (df["latitude"] <= max_lat)
# lon_filter = (df["longitude"] >= min_lon) & (df["longitude"] <= max_lon)

# df = df.loc[lat_filter & lon_filter]

df = df.loc[:, ["latitude", "longitude", "time", 'tp']]

df.to_csv("output_data.csv", index=False)



