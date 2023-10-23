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
@app.route('/api', methods=['POST'])
def receber_dados():
    try:
        data = request.get_json()  # Obter dados JSON da requisição
        data = json.dumps(data)

        ############################
        # Pré-processamento dos dados
        columns = ['x', 'y', 'z']
        df = pd.DataFrame(data, columns=columns)
        df['x'] = df['x'].astype('float')
        df['y'] = df['y'].astype('float')
        df['z'] = df['z'].astype('float')
        data = df.to_numpy()
        data = data.reshape(-1, 90, 3)
       # print("Número de registros recebidos:", numero_de_registros)
        print("Dados recebidos:", data)

        return jsonify({"status": str(data)})
    except Exception as e:
        return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



