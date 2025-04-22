import datetime as dt 

def fn2dn(fn):
    date_str = fn.split('_')[3]
    
    fmt = '%Y%j%H%M%S'
    
    try:
        return dt.datetime.strptime(date_str, fmt)
    except:
        date_str = date_str.replace('60', '59')
        return dt.datetime.strptime(date_str, fmt)
    
def test_fn2dn():
    
    fn = 'timed_guvi_l3-on2_2015351234453_2015352235730_REV76012_Av0100r000.nc'
    
    return fn2dn(fn)
    

# test_fn2dn()

