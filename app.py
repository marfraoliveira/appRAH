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

#%%
@app.route('/api', methods=['POST'])
def receber_dados():
    
    try:
       #data = json.loads(received_json)
        data = request.get_json()
        if "data" in data:
        # Excluindo o último registro se estiver mal formado
            if not all(key in data["data"][-1] for key in ["x", "y", "z", "timestamp"]):
                del data["data"][-1]
        # Recompondo o JSON
        recomposed_json = json.dumps(data, indent=4)
        print(recomposed_json)        
        
                
        return jsonify({'args': str(recomposed_json)})
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
