from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

img = Image.open(".\\dem_grey\\1_0_0.png")

plt.imshow(img)

plt.show()

img = np.asarray(img)
img = img.astype(int)
xx,yy=np.mgrid[0:img.shape[0],0:img.shape[1]]
fig=plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(xx,yy,img,cmap='terrain')
plt.show()
