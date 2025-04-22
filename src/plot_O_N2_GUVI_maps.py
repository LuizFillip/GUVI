import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import xarray as xr 
import cartopy.crs as ccrs
import GEO as gg 
import numpy as np 
import os 
from GUVI import fn2dn 
import datetime as dt 

path = 'GUVI/data/201512/'


def dataset(fn):
    
    ds = xr.open_dataset(path + fn)
    
    ds['GRID_LONGITUDE'] = ds['GRID_LONGITUDE'] - 180
        
    ds_sel = ds.where(
        (ds['GRID_LONGITUDE'] > -90) & 
        (ds['GRID_LONGITUDE'] < -30) & 
        (ds['GRID_LATITUDE'] > -50) & 
        (ds['GRID_LATITUDE'] < 10),
        drop = True  
    )   
    
    return ds_sel

def plot_ON2_GUVI_maps():
    
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
            
            
dates_str = os.listdir(path)

datas = [fn2dn for data in dates_str]

# Definir intervalo de datas
date_start = dt.datetime(2015, 12, 19)
date_end = dt.datetime(2015, 12, 23)

# Filtrar datas dentro do intervalo
dates_filtered = [data for data in datas if date_start <= data <= date_end]