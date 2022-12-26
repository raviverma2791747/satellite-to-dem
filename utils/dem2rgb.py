import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import stl
img = np.asarray(Image.open('output_NASADEM.tif'))#.convert('L'))

imgplot = plt.imshow(img,cmap='Spectral')
plt.colorbar(label="Elevation", orientation="horizontal")
plt.axis('off')
plt.show()