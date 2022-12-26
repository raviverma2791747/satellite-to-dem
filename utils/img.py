import matplotlib.pyplot as plt
from PIL import Image
import gdal

img = Image.open('data\img\img_1.tif')

plt.imshow(img)

plt.plot()