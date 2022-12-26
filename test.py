#Test trained model on a few images...
from os import listdir
from keras_preprocessing.image import img_to_array, load_img
from keras.models import load_model
from numpy.random import randint
from matplotlib import pyplot
from numpy import  asarray,vstack

# load all images in a directory into memory
def load_images(path, size=(256,256)):
	src_list, tar_list = list(), list()
	# enumerate filenames in directory, assume all are images

	for filename in listdir(path+"\\img"):
		# load and resize the image
		sat_img = load_img(path +"\\img\\"+ filename, target_size=size)
		# convert to numpy array
		sat_img = img_to_array(sat_img)
		map_img = load_img(path+"\\dem\\dem_"+filename.split(".")[0].split("_")[-1]+".png",target_size=size)
		map_img = img_to_array(map_img)
		# split into satellite and map
		#sat_img, map_img = pixels[:, :256], pixels[:, 256:]
		src_list.append(sat_img)
		tar_list.append(map_img)
	return [asarray(src_list), asarray(tar_list)]

# dataset path
path = '.\\dataset'
# load dataset
[src_images, tar_images] = load_images(path)
print('Loaded: ', src_images.shape, tar_images.shape)


n_samples = 3
for i in range(n_samples):
	pyplot.subplot(2, n_samples, 1 + i)
	pyplot.axis('off')
	pyplot.imshow(src_images[i].astype('uint8'))
# plot target image
for i in range(n_samples):
	pyplot.subplot(2, n_samples, 1 + n_samples + i)
	pyplot.axis('off')
	pyplot.imshow(tar_images[i].astype('uint8'))
pyplot.show()

#######################################

from pix2pix_model import (define_discriminator, define_gan, define_generator,
                           train)

# define input shape based on the loaded dataset
image_shape = src_images.shape[1:]
# define the models
d_model = define_discriminator(image_shape)
g_model = define_generator(image_shape)
# define the composite model
gan_model = define_gan(g_model, d_model, image_shape)

#Define data
# load and prepare training images
data = [src_images, tar_images]

def preprocess_data(data):
	# load compressed arrays
	# unpack arrays
	X1, X2 = data[0], data[1]
	# scale from [0,255] to [-1,1]
	X1 = (X1 - 127.5) / 127.5
	X2 = (X2 - 127.5) / 127.5
	return [X1, X2]

dataset = preprocess_data(data)

model = load_model('model_3980.h5')

# plot source, generated and target images
def plot_images(src_img, gen_img, tar_img):
	images = vstack((src_img, gen_img, tar_img))
	# scale from [-1,1] to [0,1]
	images = (images + 1) / 2.0
	titles = ['Source', 'Generated', 'Expected']
	# plot images row by row
	for i in range(len(images)):
		# define subplot
		pyplot.subplot(1, 3, 1 + i)
		# turn off axis
		pyplot.axis('off')
		# plot raw pixel data
		pyplot.imshow(images[i])
		# show title
		pyplot.title(titles[i])
	pyplot.show()



[X1, X2] = dataset
# select random example
ix = randint(0, len(X1), 1)
src_image, tar_image = X1[ix], X2[ix]
# generate image from source
print(src_image.shape)
gen_image = model.predict(src_image)
# plot all three images
plot_images(src_image, gen_image, tar_image)


pyplot.imshow(gen_image,cmap='terrain')
pyplot.plot()