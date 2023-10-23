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
       # Obter os dados JSON da requisição
       data_req = request.get_json()
       
       # Suponha que você já tenha a string JSON em 'data_json'
       data_json = json.dumps(data_req)
       
       # Decodifique a string JSON em uma lista de dicionários
       data_list = json.loads(data_json)
       
       # Crie um DataFrame a partir da lista de dicionários
       #df = pd.DataFrame(data_list)
       
       # Agora você tem um DataFrame criado a partir da lista de dicionários
     
       return jsonify({"status": str(data_list)})
     except Exception as e:
       return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



