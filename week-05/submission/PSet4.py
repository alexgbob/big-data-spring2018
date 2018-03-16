##PSet 4 - Alex Bob
import sys
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

DATA = "/Users/abob/Desktop/github/big-data-spring2018/week-05/LC08_L1TP_012031_20170801_20170811_01_T1"

##My Functions

def tif2array(location):
    ls_data = gdal.Open(location)
    ls_band = ls_data.GetRasterBand(1)
    band = ls_band.ReadAsArray()
    band = band.astype(np.float32)
    return band


def process_string (st):
    return float(st.split(' = ')[1].strip('\n'))

def retrieve_meta(meta_text):
    with open(meta_text) as f:
        meta = f.readlines()
        matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
        matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
        return matching


def rad_calc(tirs, var_list):
    """
    Calculate Top of Atmosphere Spectral Radiance
    Note that you'll have to access the metadata variables by
    their index number in the list, instead of naming them like we did in class.
    """
    rad = var_list[0] * tirs + var_list[1]
    return rad
    #plt.imshow(rad, cmap='RdYlGn')
    #plt.colorbar()


def bt_calc(rad, var_list):
    """
    Calculate Brightness Temperature
    Again, you'll have to access appropriate metadata variables
    by their index number.
    """
    bt = (var_list[3] / np.log(var_list[2]/rad) + 1) - 273.15
    return bt
    #plt.imshow(bt, cmap='RdYlGn')
    #plt.colorbar()


def ndvi_calc(red, nir):
    """
    Calculate NDVI
    """
    ndvi = (nir - red) / (nir + red)
    return ndvi


def pv_calc(ndvi, ndvi_s, ndvi_v):
    """
    Calculate Proportional Vegetation
    """
    pv = (ndvi - ndvi_s) / (ndvi_v - ndvi_s) ** 2
    return pv
    #plt.imshow(pv, cmap='RdYlGn')
    #plt.colorbar()

def emissivity_calc (pv, ndvi):
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

#lst calculation

def lst_calc(location):
    ## 1. Define necessary constants
    wave = 10.8E-06
    # PLANCK'S CONSTANT
    h = 6.626e-34
    # SPEED OF LIGHT
    c = 2.998e8
    # BOLTZMANN's CONSTANT
    s = 1.38e-23
    p = h * c / s
    # 2. Read in appropriate tifs (using tif2array)
    tirs = tif2array(os.path.join(location, "LC08_L1TP_012031_20170801_20170811_01_T1_B10.TIF"))
    red = tif2array(os.path.join(location, 'LC08_L1TP_012031_20170801_20170811_01_T1_B4.TIF'))
    nir = tif2array(os.path.join(location, 'LC08_L1TP_012031_20170801_20170811_01_T1_B5.TIF'))
    # 3. Retrieve needed variables from metadata (retrieve_meta)
    var_list = retrieve_meta(os.path.join(location, "LC08_L1TP_012031_20170801_20170811_01_T1_MTL.txt"))
    # 4. Calculate ndvi, rad, bt, pv, emis using appropriate functions
    ndvi = ndvi_calc(red, nir)
    rad = rad_calc(tirs, var_list)
    bt = bt_calc(rad, var_list)
    pv = pv_calc(ndvi, 0.2, 0.5)
    emis = emissivity_calc(pv, ndvi)
    # 5. Calculate land surface temperature and return it.
    lst = bt / (1 + (wave * bt / p) * np.log(emis))
    return lst

# define plot function and array2tif

def plotarray(array):
    plt.imshow(array, cmap='RdYlGn')
    plt.colorbar()

def array2tif(raster_file, new_raster_file, array):
    """
    Writes 'array' to a new tif, 'new_raster_file',
    whose properties are given by a reference tif,
    here called 'raster_file.'
    """
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

# define lst array, plot it, and save to tif

lst = lst_calc(DATA)
plotarray(lst)

tirs_path = os.path.join(DATA, "LC08_L1TP_012031_20170801_20170811_01_T1_B10.TIF")
lst_outpath = os.path.join(DATA, 'bob_lst_20170811.tif')
array2tif(tirs_path, lst_outpath, lst)

# define ndvi array, plot it, and save to tif

red = tif2array(os.path.join(DATA, 'LC08_L1TP_012031_20170801_20170811_01_T1_B4.TIF'))
nir = tif2array(os.path.join(DATA, 'LC08_L1TP_012031_20170801_20170811_01_T1_B5.TIF'))

ndvi = ndvi_calc(red, nir)
plotarray(ndvi)

tirs_path = os.path.join(DATA, "LC08_L1TP_012031_20170801_20170811_01_T1_B10.TIF")
ndvi_outpath = os.path.join(DATA, 'bob_ndvi_20170811.tif')
array2tif(tirs_path, ndvi_outpath, ndvi)

# define lst cloud filter array, plot it, and save to tif

bqa = tif2array(os.path.join(DATA, "LC08_L1TP_012031_20170801_20170811_01_T1_BQA.TIF"))

def cloud_filter(array, bqa):
    array_dest = array.copy()
    array_dest[np.where((bqa != 2720) & (bqa != 2724) & (bqa != 2728) & (bqa != 2732))] = 'nan'
    return array_dest

lst_filter = cloud_filter(lst, bqa)
plotarray(lst_filter)

tirs_path = os.path.join(DATA, "LC08_L1TP_012031_20170801_20170811_01_T1_B10.TIF")
lst_filter_outpath = os.path.join(DATA, 'bob_lst_filter_20170811.tif')
array2tif(tirs_path, lst_filter_outpath, lst_filter)

# define ndvi cloud filter array, plot it, and save to tif

ndvi_filter = cloud_filter(ndvi, bqa)
plotarray(ndvi_filter)

tirs_path = os.path.join(DATA, "LC08_L1TP_012031_20170801_20170811_01_T1_B10.TIF")
ndvi_filter_outpath = os.path.join(DATA, 'bob_ndvi_filter_20170811.tif')
array2tif(tirs_path, ndvi_filter_outpath, ndvi_filter)
