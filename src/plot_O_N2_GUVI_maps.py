import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import xarray as xr 
import cartopy.crs as ccrs
import GEO as gg 
import numpy as np 

path = 'GUVI/data/201512/'


def dataset(fn):
    
    ds = xr.open_dataset(path + fn)
    
    ds['GRID_LONGITUDE'] = ds['GRID_LONGITUDE'] - 180
    
    frac_days = ds['FRACTIONAL_DOY'].values 
    
    # times = convert_frac_days(frac_days, year = 2015)
    
    ds_sel = ds.where(
        (ds['GRID_LONGITUDE'] > -70) & 
        (ds['GRID_LONGITUDE'] < -30) & 
        (ds['GRID_LATITUDE'] > -15) & 
        (ds['GRID_LATITUDE'] < 10),
        drop = True  
    )   
    
    return 
fig = plt.figure(
     dpi = 300,
     figsize = (14, 18),
     layout = "constrained"
     )

gs2 = GridSpec(2, 4)

gs2.update(hspace = 0.1, wspace = 0)

for i in range(4):
    ax3 = plt.subplot(
        gs2[0, i], 
        projection = ccrs.PlateCarree(
            )
        )
    
    gg.map_attrs(
        ax3, 2015, 
        grid = False,
        degress = None
        )
    
    if i != 0:
        
        ax3.set(
            yticklabels = [], 
            xticklabels = [], 
            xlabel = '', 
            ylabel = ''
            )
    else:
        ax3.set(
            xticks = np.arange(-90, -35, 15)
            )