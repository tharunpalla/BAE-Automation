import xarray as xr

file = './grib/nam.t00z.conusnest.hiresf00.tm00.grib2'

data = xr.open_dataset(file, engine="cfgrib")
print(data)

print(data.to_dataframe())