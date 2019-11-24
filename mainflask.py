import os, os.path
from flask import Flask, render_template, request, redirect
from PIL import Image
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D, AveragePooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
# import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

app = Flask(__name__)
script_dir = os.path.dirname(__file__)


# @ signifies a decorator- way to wrap a fun and modify it
@app.route('/')
def index():
    return render_template("homepage.html")


app.config['ALLOWED_EXTENSION'] = ['PNG', 'JPG', 'JPEG']

def allowedImage(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext.upper() in app.config['ALLOWED_EXTENSION'] :
        return  True
    else:
        return False


def get_predicted_value(input_image):
    directory = script_dir + '/ModelData/'
    input_image = image.load_img(script_dir + '/static/' + input_image.filename)
    input_image = input_image.resize((128, 128))
    input_image = image.img_to_array(input_image)
    input_image = input_image / 255
    print(directory + 'Engine.h5')
    modelML = load_model(directory + 'Engine.h5')
    pred = modelML.predict(np.reshape(np.array(input_image), (1, 128, 128, 3)))
    index = pred[0].argmax(axis=0)
    print(pred)
    print(index)
    if index == 0:
        return "Non Viable tumor"
    elif index == 1:
        return "Viable tumor"
    else:
        return "Non tumor"


@app.route('/result', methods=['POST'])
def result():
    warning = ''
    typeOsteo = ''
    pred = False
    invalid = False
    input_image = request.files["image"]
    if input_image.filename != '':
        print(input_image)
        if not allowedImage(input_image.filename):
            warning = "The file must be an Image"
            print(warning)
            invalid = True
            #return redirect('http://localhost:5000')
        else:
            input_image.save(script_dir + '/static/' + input_image.filename)
            typeOsteo = get_predicted_value(input_image)
            pred = True
    else:
        warning = "Please select an Image"
    img = input_image.filename
    return render_template("homepage.html", img=img, typeOsteo=typeOsteo, pred=pred, warning=warning)


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
