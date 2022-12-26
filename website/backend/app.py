from flask import Flask,request
from flask import jsonify
from flask import send_file
from flask_cors import CORS,cross_origin
import uuid
import model
import surf2stl
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

MODEL_PATH = ".\\model\\model_1980.h5"


if not os.path.exists(".\\output"):
    os.mkdir(".\\output")
    os.mkdir(".\\output\\dem")
    os.mkdir(".\\output\\pdem")
    os.mkdir(".\\output\\model")

if not os.path.exists(".\\uploads"):
    os.mkdir(".\\uploads")

def img2stl(file_path):
    img = np.asarray(Image.open(file_path))#.convert('L'))
    #img = img *127.5/255
    img = img.astype(int)
    xx,yy=np.mgrid[0:img.shape[0],0:img.shape[1]]
    #print(img)
    #fig=plt.figure()
    #ax = fig.add_subplot(projection='3d')
    #ax.plot_surface(xx,yy,img,cmap='terrain')
    #plt.show()
    file_name = file_path.split('\\')[-1].split('.')[0]
    surf2stl.write('.\\output\\model\\{}.stl'.format(file_name), xx, yy, img)

app = Flask(__name__)
CORS(app)

model = model.Model(MODEL_PATH)

@app.route('/',methods=['GET'])
@cross_origin()
def index():
    return '<h1>Action Recognition API</h1>'

@app.route('/api/upload',methods=['POST'])
@cross_origin()
def predict():
    #try:
    img = request.files['image']
    _id = str(uuid.uuid4())
    img_path = f".\\uploads\\{_id}.png"
    img.save(img_path)
    print(img_path)
    dem = model.predict(img_path)
    output_path = f".\\output\\dem\\{_id}.png"
    dem.save(output_path)
    plt.imsave(f".\\output\\pdem\\{_id}.png",dem,cmap="terrain")
    img2stl(output_path)
    return jsonify({ 'status' : 200, 'data' : { "id" : _id  } ,'message':'result'})
    # except:
        # app.logger.info('[500]: Something went wrong!')
        # return jsonify({'status': 500 ,'data':None,'message':'Something went wrong!'})

@app.route('/api/dem/download/<dem_id>',methods=['GET'])
@cross_origin()
def get_dem_output(dem_id):
    try:
        dem_path = f'./output/dem/{dem_id}'
        print(dem_path)
        return send_file(dem_path,as_attachment=True)
    except:
        return jsonify({'status' : 404, 'message' : 'Image not found!'})

@app.route('/api/pdem/download/<pdem_id>',methods=['GET'])
@cross_origin()
def get_pdem_output(pdem_id):
    try:
        pdem_path = f'./output/pdem/{pdem_id}'
        print(pdem_path)
        return send_file(pdem_path,as_attachment=True)
    except:
        return jsonify({'status' : 404, 'message' : 'Image not found!'})


@app.route('/api/model/download/<model_id>',methods=['GET'])
@cross_origin()
def get_stl_output(model_id):
    try:
        model_path = f'./output/model/{model_id}'
        print(model_path)
        return send_file(model_path,as_attachment=True)
    except:
        return jsonify({'status' : 404, 'message' : 'Model not found!'})

if __name__ == '__main__':
    app.run(debug=True,threaded=True,port=5000)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300