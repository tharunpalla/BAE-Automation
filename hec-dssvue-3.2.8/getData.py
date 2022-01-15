import xarray as xr

file = 'nam.t00z.conusnest.hiresf00.tm00.grib2'

data = xr.open_dataset(file, engine="cfgrib")
# print(data)

for v in data:
    print("{}, {}, {}".format(v, data[v].attrs["long_name"], data[v].attrs["units"]))

print(data.get('tp'))

df = data.to_dataframe()
df.to_csv('test.csv')
