from keras.models import load_model
from keras_preprocessing.image import img_to_array, load_img, array_to_img
import numpy as np
from numpy import  asarray,vstack
from PIL import ImageOps,Image
class Model:

    def __init__(self,model_path):
        self._model = load_model(model_path)
        
    def preprocess_data(self,data):
        # load compressed arrays
        # unpack arrays
        X = data
        # scale from [0,255] to [-1,1]
        X = (X - 127.5) / 127.5
        return X
    
    def load_images(self,path, size=(256,256)):
        src_list = list()
        sat_img = load_img(path , target_size=size)
        # convert to numpy array
        sat_img = img_to_array(sat_img)
        src_list.append(sat_img)
        return [asarray(src_list)]

    def predict(self,input_path):
        [src_image] = self.load_images(input_path)
        print(src_image.shape)
        src_image = self.preprocess_data(src_image)
        print(src_image.shape)
        #src_image.
        gen_image = self._model.predict(src_image)
        gen_image = np.squeeze(gen_image,axis = 0)
        gen_image = (gen_image + 1) / 2.0
        gen_image = gen_image.sum(axis=2)
        #gen_image = gen_image / 3
        gen_image = gen_image * 255/3
        gen_image = gen_image.astype(int)
        #print(gen_image)
        #gen_image = array_to_img(gen_image)
        gen_image = Image.fromarray(gen_image)
        #gen_image = ImageOps.grayscale(gen_image)
        return  gen_image

if __name__ == "__main__":
    pass
