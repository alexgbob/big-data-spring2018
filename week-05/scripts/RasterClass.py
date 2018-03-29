import sys
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

Data = "/Users/abob/Downloads/ws04_materials"

b4_raster = os.path.join(Data, 'b4.tif')
b5_raster = os.path.join(Data, 'b5.tif')

# Load in Red band
red_data = gdal.Open(b4_raster)
red_band = red_data.GetRasterBand(1)
red = red_band.ReadAsArray()

# Load in Near-infrasred band
nir_data = gdal.Open(b5_raster)
nir_band = nir_data.GetRasterBand(1)
nir = nir_band.ReadAsArray()

plt.imshow(nir)
plt.colorbar()

def ndvi_calc(red, nir):
    """ Calculate NDVI"""
    return (nir - red) / (nir + red)

plt.imshow(ndvi_calc(red, nir), cmap="YlGn")
plt.colorbar()

red.dtype
nir.dtype

red = red.astype(np.float32)
nir = nir.astype(np.float32)

plt.imshow(ndvi_calc(red, nir), cmap='YlGn')
plt.colorbar()

ndvi = ndvi_calc(red, nir)

# Path of TIRS Band
b10_raster = os.path.join(Data, 'b10.TIF')

# Load in TIRS Band
tirs_data = gdal.Open(b10_raster)
tirs_band = tirs_data.GetRasterBand(1)
tirs = tirs_band.ReadAsArray()
tirs = tirs.astype(np.float32)

# make this path the local path to your MTL.txt file that you downloaded at the start of the workshop
meta_file = '/Users/abob/Downloads/ws04_materials/MTL.txt'

with open(meta_file) as f:
    meta = f.readlines()

# Define terms to match
matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']

[s for s in meta if any(xs in s for xs in matchers)]

def process_string (st):
    return float(st.split(' = ')[1].strip('\n'))

matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]

rad_mult_b10, rad_add_b10, k1_b10, k2_b10 = matching

rad = rad_mult_b10 * tirs + rad_add_b10
plt.imshow(rad, cmap='RdYlGn')
plt.colorbar()

bt = k2_b10 / np.log((k1_b10/rad) + 1) - 273.15
plt.imshow(bt, cmap='RdYlGn')
plt.colorbar()

plt.imshow(ndvi, cmap='YlGn')
plt.colorbar()

pv = (ndvi - 0.2) / (0.5 - 0.2) ** 2
plt.imshow(pv, cmap='RdYlGn')
plt.colorbar()

def emissivity_reclass (pv, ndvi):
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

emis = emissivity_reclass(pv, ndvi)

plt.imshow(emis, cmap='RdYlGn')
plt.colorbar()

wave = 10.8E-06
# PLANCK'S CONSTANT
h = 6.626e-34
# SPEED OF LIGHT
c = 2.998e8
# BOLTZMANN's CONSTANT
s = 1.38e-23
p = h * c / s

lst = bt / (1 + (wave * bt / p) * np.log(emis))

plt.imshow(lst, cmap='RdYlGn')
plt.colorbar()

# Invoke the GDAL Geotiff driver
driver = gdal.GetDriverByName('GTiff')

# Use the driver to create a new file.
# It has the same dimensions as our original rasters
# so we can use the tirs_data size properties
# Note that tirs_data = gdal.Open(b10_raster)
# This is not the numpy array!
new_dataset = driver.Create('/Users/abob/Downloads/ws04_materials/lst.tif',
                    tirs_data.RasterXSize,
                    tirs_data.RasterYSize,
                    1,
                    gdal.GDT_Float32)
# Set projection - same logic as above.
new_dataset.SetProjection(tirs_data.GetProjection())
# Set transformation - same logic as above.
new_dataset.SetGeoTransform(tirs_data.GetGeoTransform())
# Set up a new band.
new_band = new_dataset.GetRasterBand(1)
# Set NoData Value
new_band.SetNoDataValue(-1)
# Write our Numpy array to the new band!
new_band.WriteArray(lst)
