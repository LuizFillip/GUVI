import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import xarray as xr 
import cartopy.crs as ccrs
import GEO as gg 
import numpy as np 
import os 
from GUVI import fn2dn 
import datetime as dt 
import base as b 

b.config_labels()

path = 'GUVI/data/201512/'


def dataset(fn):
    
    ds = xr.open_dataset(path + fn)
    
    ds['GRID_LONGITUDE'] = ds['GRID_LONGITUDE'] - 180
        
    ds_sel = ds.where(
        (ds['GRID_LONGITUDE'] > -90) & 
        (ds['GRID_LONGITUDE'] < -30) & 
        (ds['GRID_LATITUDE'] > -50) & 
        (ds['GRID_LATITUDE'] < 20),
        drop = True  
    )   
    
    return ds_sel

def plot_ON2_GUVI_maps(ax, ds, i):
     
    levels = np.arange(0.2, 0.8, 0.01)
    img = ax.contourf(
        ds['GRID_LONGITUDE'], 
        ds['GRID_LATITUDE'], 
        ds['ON2_GRID_INTERPOLATED'], 
        levels = levels
        )
    
    gg.plot_square_area(
        ax,
        lat_min = -10,
        lon_min = -50,
        lat_max = 5, 
        lon_max = -40, 
        color = 'white'
        )
        
    gg.map_attrs(
        ax, 2015, 
        grid = False,
        degress = None
        )
    
    if i != 0:
        
        ax.set(
            yticklabels = [], 
            xticklabels = [], 
            xlabel = '', 
            ylabel = ''
            )
           
    else:
        ax.set(
            xticks = np.arange(-90, -25, 30), 
            yticks = np.arange(-40, 30, 20)
            )
    
    ticks = np.arange(0.2, 0.8, .1)
    
    if i == 3:
        
        b.colorbar(
                img, 
                ax, 
                ticks, 
                label = '$O/N_2$', 
                height = "100%", 
                width = "10%",
                orientation = "vertical", 
                anchor = (.25, 0., 1, 1)
                )
    return img 

def plot_ON2_timeseries(ax, dn_start, dn_end):
       
    df = b.load('GUVI/data/ON2')
    
    ax.plot(
        df * 1e2,
        lw = 2, 
        marker = 'o', 
        markersize = 20, 
        fillstyle = 'none'
        )
    
    
    ax.set(
        xlim = [dn_start, dn_end ],
        # ylim = [0.01, 0.06], 
        ylabel = '$[O/N_2] \\times 10^{-2}$'
        )
    
    b.format_time_axes(
        ax, 
        hour_locator = 12, 
        translate = True, 
        pad = 85, 
        format_date = '%d/%m/%y'
        )
    
    return None 


dates_str = os.listdir(path)

dn_start = dt.datetime(2015, 12, 19)
dn_end = dt.datetime(2015, 12, 23)
  
dates_filtered = [
    fn for fn in dates_str if 
    dn_start <= fn2dn(fn) <= dn_end
    ]

fig = plt.figure(dpi = 300, figsize = (14, 8))

gs2 = GridSpec(2, 4, figure=fig)

gs2.update(hspace = 0.5, wspace = 0)

for col, fn in enumerate(dates_filtered):
    
    ds = dataset(fn)
    
    ax = plt.subplot(
        gs2[0, col], 
        projection = ccrs.PlateCarree()
        )
    
    img = plot_ON2_GUVI_maps(ax, ds, col)
    
    
    
ax = plt.subplot(gs2[1, :])
    
plot_ON2_timeseries(ax, dn_start, dn_end)