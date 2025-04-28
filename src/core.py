import xarray as xr 
import os 
import matplotlib.pyplot as plt 
import datetime as dt 
import pandas as pd 

path = 'GUVI/data/201512/'





def convert_frac_days(frac_days, year = 2015):
    datetimes = [
        dt.datetime(year, 1, 1) + 
        dt.timedelta(days = day - 1) for day in frac_days]

    return [dt.isoformat() for dt in datetimes]
    

def mean_from_region(path):
    
    files = os.listdir(path)
    
    out = {
           'mean': [],
           'std': [],
           'dn': []
           }
    for fn in files:
        
        ds = xr.open_dataset(path + fn)
        
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
        
        try:
            date = ds.attrs['STARTING_TIME']
            dn = dt.datetime.strptime(
                date, 
                '%Y%j%H%M%S'
                )
            
            date = ds.attrs['STARTING_TIME']
        except:
            date = ds.attrs['STARTING_TIME'].replace('60', '59')
            dn = dt.datetime.strptime(
                date, 
                '%Y%j%H%M%S'
                )
            
        vls = ds_sel['ON2_GRID'].values
        
        out['mean'].append(vls.mean())
        out['std'].append(vls.std())
        out['dn'].append(dn)
        
       
    df = pd.DataFrame(out)
    
    df.set_index('dn', inplace = True)
    
    df  = df.sort_index()
    
    df = df.loc[df.index.month == 12]
    
    return df 

# df  = mean_from_region(path)

# df.to_csv('GUVI/data/ON2_SAA_2')

# df