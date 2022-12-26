import rasterio
import glob
import json
import pandas as pd
count = 0
meta_data = { "exents_format" : "[minX,minY,maxX,maxY]" , "extents":[]}
df = pd.DataFrame(columns=['tile','minX','minY','maxX','maxY'])

for file_name in glob.glob('.\\raw_dem_tiles\\*.tif'):
    dataset = rasterio.open(file_name)
    #print([dataset.bounds.left,dataset.bounds.bottom,dataset.bounds.right,dataset.bounds.top,])
    meta_data['extents'].append([dataset.bounds.left,dataset.bounds.bottom,dataset.bounds.right,dataset.bounds.top,])
    df.loc[len(df)] = [count,dataset.bounds.left,dataset.bounds.bottom,dataset.bounds.right,dataset.bounds.top,]
    count += 1
with open('meta_data.json','w') as file:
    json.dump(meta_data,file,indent=4)
df.to_csv('meta_data.csv',index=False)