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
# =============================================================================
#     try:
#         dados = request.get_json()  # Obter dados JSON da requisição
#         if 'data' in dados and isinstance(dados['data'], list) and len(dados['data']) > 0:
#             # Remova o último registro da lista
#             dados = dados['data'].pop()
#         return jsonify({"status": str(dados)})
#     except Exception as e:
#         return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})
# =============================================================================
   try:
        dados = [
            {"data": [{"x": -1.8440361022949219, "y": 6.280742645263672, "z": 7.210247039794922, "timestamp": "2023-10-25 09:37:40.917324"}, {"x": -1.8440361022949219, "y": 6.280742645263672, "z": 7.210247039794922, "timestamp": "2023-10-25 09:37:40.917402"}, {"x": -1.5227222442626953, "y": 6.109155654907227, "z": 7.767829895019531, "timestamp": "2023-10-25 09:37:40.980064"}, {"x": -1.5227222442626953, "y": 6.109155654907227, "z": 7.767829895019531, "timestamp": "2023-10-25 09:37:40.980143"}, {"x": -1.5538654327392578, "y": 6.10975456237793, "z": 7.692966461181641, "timestamp": "2023-10-25 09:37:41.060983"}]}
        ]

        # Remover o último registro da lista 'dados'
        if dados and 'data' in dados[0] and isinstance(dados[0]['data'], list) and len(dados[0]['data']) > 0:
            dados[0]['data'].pop()

        print(dados)
        return jsonify({"status dos dados recebidos": str(dados)})
   except Exception as e:
        return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
