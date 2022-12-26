import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import glob

files = list(glob.glob(".\\raw_dem_tiles\\*.tif"))

count = 0
for file in files:
    img = np.asarray(Image.open(file))#.convert('L'))
    img = img * 255/3819
    img = img.astype(int)
    img_out = Image.fromarray(img)
    img_out = img_out.convert("RGB")
    file_name = file.split("\\")[-1].split(".")[0]
    img_out.save(f".\\dem\\dem_{count}.png")
    print(file_name)
    count += 1
    #xx,yy=np.mgrid[0:img.shape[0],0:img.shape[1]]
    #fig=plt.figure()
    #ax = fig.add_subplot(projection='3d')
    #ax.plot_surface(xx,yy,img,cmap='terrain')
    #plt.show()
    #print(file_name.split('\\')[-1].split('.')[0])
    #surf2stl.write('.\\stl\\{}.stl'.format(file_name.split('\\')[-1].split('.')[0]), xx, yy, img)