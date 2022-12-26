import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import surf2stl
import glob

files = list(glob.glob(".\\dem\\*.tif"))



for file_name in files:
    img = np.asarray(Image.open(file_name))#.convert('L'))
    img = img * 255/img.max()
    img = img.astype(int)
    xx,yy=np.mgrid[0:img.shape[0],0:img.shape[1]]
    fig=plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(xx,yy,img,cmap='terrain')
    plt.show()
    print(file_name.split('\\')[-1].split('.')[0])
    surf2stl.write('.\\stl\\{}.stl'.format(file_name.split('\\')[-1].split('.')[0]), xx, yy, img)