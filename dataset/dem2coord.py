import rasterio
import glob
import json
import pandas as pd

dataset = rasterio.open(".\\raw_dem\\1.tif")

print([dataset.bounds.left,dataset.bounds.bottom,dataset.bounds.right,dataset.bounds.top,])
