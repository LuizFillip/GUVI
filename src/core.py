import xarray as xr 
import os 
import matplotlib.pyplot as plt 
import datetime as dt 
import pandas as pd 

path = 'GUVI/data/201512/'


files = os.listdir(path)


def convert_frac_days(frac_days, year = 2015):
    datetimes = [
        dt.datetime(year, 1, 1) + 
        dt.timedelta(days = day - 1) for day in frac_days]

    return [dt.isoformat() for dt in datetimes]
    

def mean_from_region(files):
    
    out = {
           'ON2': [], 
           'dn': []
           }
    for fn in files:
        
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
            
        avg = ds_sel['ON2_GRID'].values.mean()
        
        out['ON2'].append(avg)
        out['dn'].append(dn)
        
       
    df = pd.DataFrame(out)
    
    df.set_index('dn', inplace = True)
    
    df  = df.sort_index()
    
    df = df.loc[df.index.month == 12]
    
    return df 

df  = mean_from_region(files)

df.to_csv('ON2')