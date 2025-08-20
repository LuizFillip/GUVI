import xarray as xr 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 

fn = 'GUVI/data/201512/timed_guvi_l3-on2_2015351234453_2015352235730_REV76012_Av0100r000.nc'
ds = xr.open_dataset(fn)

ds['GRID_LONGITUDE'] = ds['GRID_LONGITUDE'] - 180

lat_min = -10
lat_max = 10

lon_min = -70
lon_max = -40 

ds_sel = ds.where(
    (ds['GRID_LONGITUDE'] > lon_min) & 
    (ds['GRID_LONGITUDE'] < lon_max) & 
    (ds['GRID_LATITUDE'] > lat_min) & 
    (ds['GRID_LATITUDE'] < lat_max),
    drop = True  
)   

# orbits = np.unique(ds['ORBIT'].values)

# orbit  = orbits[1]


# # ds = ds.where( ds['ORBIT'] == orbit)
 
# year = 2015
# datetimes = [pd.Timestamp(year, 1, 1) + pd.Timedelta(days=day-1) for day in ds["FRACTIONAL_DOY"].values]

# # adiciona como coordenada
# ds = ds.assign_coords(
#     datetime = ("time", pd.to_datetime(datetimes))
#     )

orbit_id = int(np.asarray(ds.ORBIT)[0])
# orbit_id = 10523  # <- descomente e defina manualmente, se preferir

# 2) filtrar o dataset para essa órbita e ordenar por tempo (FRACTIONAL_DOY)
track = ds.sel(length_default=ds.ORBIT == orbit_id).sortby('FRACTIONAL_DOY')

# 3) limpeza rápida (remove NaNs em lat/lon)
valid = np.isfinite(track.LATITUDE) & np.isfinite(track.LONGITUDE)
lat = np.asarray(track.LATITUDE[valid])
lon = np.asarray(track.LONGITUDE[valid])

# --- PLOT 1: trajetória da órbita (lon vs lat) ---
plt.figure(figsize=(7,4.5))
plt.plot(lon, lat, marker='.', lw=0.8, ms=3)
plt.title(f'Trajetória da órbita {orbit_id}')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- PLOT 2: trajetória colorida por SZA (ou troque por outra variável) ---
cvar = np.asarray(track['SOLAR ZENITH ANGLE'][valid])  # troque por track.ON2[valid] se quiser
plt.figure(figsize=(7,4.5))
sc = plt.scatter(lon, lat, c=cvar, s=10)
plt.title(f'Órbita {orbit_id} — cor = Solar Zenith Angle')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')
plt.grid(True, alpha=0.3)
cbar = plt.colorbar(sc)
cbar.set_label('Solar Zenith Angle (°)')
plt.tight_layout()
plt.show()