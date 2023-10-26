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
        dados = request.get_json()  # Obter dados JSON da requisição
        print(dados)
        columns = ['x', 'y', 'z','timestamp']
        #df = pd.DataFrame(dados)
        #data = np.array(df)
        # Converta o array NumPy em uma lista Python
        #data_list = data.tolist()
        # Serialize a lista em formato JSON
        json_data = json.dumps(data_list)
        # Converter o JSON de volta para uma lista de dicionários
        data_list = json.loads(json_data)
        # Remover o último registro
        if data_list:
            data_list.pop()
            print(data_list)
        return jsonify({"status dos dados recebidos": str(json_data)})
    except Exception as e:
        return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
