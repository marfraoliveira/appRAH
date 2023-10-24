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
import jsonschema
from jsonschema import validate

app = Flask(__name__)
#%%
# Defina o esquema JSON
schema = {
    "type": "object",
    "properties": {
        "x": {"type": "number"},
        "y": {"type": "number"},
        "z": {"type": "number"},
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["x", "y", "z", "timestamp"]
}
#%%
@app.route('/api', methods=['POST'])
def receber_dados():
     try:
       # Obter os dados JSON da requisição
       data = request.get_json()
       data = json.loads(data_json)
       validate(data, schema)  # Validação
       # Suponha que você já tenha a string JSON em 'data_json'
       #data_json = json.dumps(data_req)
       # Decodifique a string JSON em uma lista de dicionários
       #data_list = json.loads(data_json)
       print(data)      
# =============================================================================
#        #Cria um dataframe numpy
#        data_array = np.array(data_list)
#       
#        # Verifique se 'data_array' tem pelo menos uma linha (é 1D)
#        if data_array.ndim == 1:
#             # Adicione uma dimensão extra para torná-lo 2D
#             data_array = data_array.reshape(1, -1)
#         
#         # Agora você pode criar um DataFrame Pandas a partir de 'data_array'
#        df = pd.DataFrame(data_array)
# =============================================================================
       # Agora você tem um DataFrame criado a partir da lista de dicionários

       return jsonify({"status": str(data)})
     except json.JSONDecodeError:
          # Tratar erro de decodificação JSON
     except jsonschema.exceptions.ValidationError:
    # Tratar erro de validação em relação ao esquema
       return jsonify({"status": "Erro ao processar os dados", "erro": str(e)})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



