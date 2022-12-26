import gdal
import matplotlib.pyplot as plt
import numpy as np
import glob 
import tqdm

files = list(glob.glob('.\\raw_img_tiles\\*.tif'))

count = 0
for file in tqdm.tqdm(files):
    # Open the GeoTIFF file
    ds = gdal.Open(file)

    # Get the number of bands in the file
    num_bands = ds.RasterCount

    # Check that there are 3 bands
    if num_bands != 3:
        print("Error: this file does not have 3 bands")
        #exit()

    # Get the data from each band
    band1 = ds.GetRasterBand(1).ReadAsArray()
    band2 = ds.GetRasterBand(2).ReadAsArray()
    band3 = ds.GetRasterBand(3).ReadAsArray()
    
    # Stack the bands into a single 3D array
    image = np.dstack((band3, band2, band1))
    
    
    # Display the image using matplotlib
    
    image = image * 255/image.max()
    image= image.astype(np.uint8)
    #print(image)
    #plt.axis(False)
    #plt.imshow(image)
    #plt.show()
    file_name = file.split("\\")[-1].split(".")[0]
    # Save the image as a PNG file
    plt.imsave(f'.\\img\\img_{count}.png', image)
    count += 1
