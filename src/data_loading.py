import pandas as pd
from astropy.io import fits
import csv
import ast

def load_saga_hosts():
    return pd.read_parquet('data/xSAGA-hosts_2021-09-28.parquet', engine='auto')

def load_satellites():
    return pd.read_csv('data/xSAGA-lowz_2021-08-30.csv')

def load_galspec_extra():
    gse = fits.getdata('data/galSpecExtra-dr8.fits')
    return pd.DataFrame({
        "PLATE": gse.PLATEID.byteswap().newbyteorder(),
        "MJD": gse.MJD.byteswap().newbyteorder(),
        "FIBERID": gse.FIBERID.byteswap().newbyteorder(),
        "Metalicity": gse.OH_P50.byteswap().newbyteorder(),
        "SFR": gse.SFR_TOT_P50.byteswap().newbyteorder(),
        "BPT_CLASS": gse.BPTCLASS.byteswap().newbyteorder()
    })

def load_satellite_host_pairs(file_path='data/hostpairsnew.csv'):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        pairs = {}
        for row in reader:
            key = int(row[0])  # Convert to int as NSAID is typically an integer
            # Convert the string representation of a list to an actual list
            value = ast.literal_eval(row[1])
            pairs[key] = value
    return pairs