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

#execção ansiosa
tf.config.run_functions_eagerly(True)
# Carregue o modelo uma vez ao iniciar o servidor Flask
model = load_model('./modelCNN.h5')
# Defina a opção para executar em modo eager
#tf.config.run_functions_eagerly(True)

#%%
@app.route('/api', methods=['POST'])
def receber_dados():
    try:
        dados = request.get_json()  # Obter dados JSON da requisição
        # Pré-processamento dos dados
        columns = ['x', 'y', 'z']
        df = pd.DataFrame(dados, columns=columns)
        df['x'] = df['x'].astype('float')
        df['y'] = df['y'].astype('float')
        df['z'] = df['z'].astype('float')
        dados = df.to_numpy()
        dados = dados.reshape(-1, 90, 3)

        # Faça uma única previsão com o modelo carregado
        class_predict = np.argmax(model.predict(dados), axis=1)
        
        # Contar o número de registros recebidos
        numero_de_registros = len(dados)
        
        # Mapear as previsões para as categorias
        category_mapping = {
            0: 'Walking',
            1: 'Jogging',
            2: 'Upstairs',
            3: 'Downstairs',
            4: 'Sitting',
            5: 'Standing'
        }
        class_labels = [category_mapping[pred] for pred in class_predict]
        print("Número de registros recebidos:", numero_de_registros)
        print("Dados recebidos:", dados)

        return jsonify(str(category_mapping))
    except Exception as e:
        return jsonify(str({"status": "Erro ao processar os dados", "erro": str(e)}))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



