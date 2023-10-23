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
        dados = request.get_json()  # Obter dados JSON da requisição
        # tratar json
        # Verificar se cada registro contém todas as chaves necessárias
        dados_filtrados = [registro for registro in dados if all(chave in registro for chave in ('x', 'y', 'z', 'timestamp'))]
        
        # Converter os dados filtrados de volta para uma carga JSON
        json_filtrado = json.dumps(dados_filtrados)

        
        # Contar o número de registros recebidos
        numero_de_registros = len(dados)

        print("Número de registros recebidos:", numero_de_registros)
        print("Dados recebidos:", dados)

        return jsonify({"status": "Dados recebidos com sucesso"})
    except Exception as e:
        return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



