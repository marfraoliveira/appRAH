import time
from distutils.log import debug
from fileinput import filename
from flask import *  
from flask import Flask,request,jsonify  
import numpy as np
import pandas as pd
import keras.models
from keras.models import model_from_json
import json
from json import JSONEncoder
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)
#%%


#%%
# Carregue o modelo uma vez ao iniciar o servidor Flask
model = load_model('./modelCNN.h5')
import time

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/api', methods=['POST'])
def predict():
    try:
        # Obtém o JSON da solicitação
        data = request.get_json()
        # Pré-processamento dos dados
        columns = ['x', 'y', 'z']
        df = pd.DataFrame(data, columns=columns)
        df['x'] = df['x'].astype('float')
        df['y'] = df['y'].astype('float')
        df['z'] = df['z'].astype('float')
        data = df.to_numpy()
        data = data.reshape(-1, 90, 3)
        
        # Faça uma única previsão com o modelo carregado
        predictions = model.predict(data)
        
        # Mapear as previsões para as categorias
        category_mapping = {
            0: 'Walking',
            1: 'Jogging',
            2: 'Upstairs',
            3: 'Downstairs',
            4: 'Sitting',
            5: 'Standing'
        }
        
        # Faça uma única previsão com o modelo carregado
        class_predict = [category_mapping[np.argmax(pred)] for pred in predictions]
        
        return jsonify({'args': str(class_predict)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
df = pd.read_csv('resultados_1210.csv',sep=';')


