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
# =============================================================================

# =============================================================================
# CARREGAR O MODELO DE DL
# =============================================================================
model = load_model('./modelCNN.h5')

app = Flask(__name__)
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
# =============================================================================
# pré-processamento
# =============================================================================
        parsed_data = json.loads(recomposed_json)
        data = np.array([[item["x"], item["y"], item["z"]] for item in parsed_data["data"]])
        columns = ['x', 'y', 'z']
        df = pd.DataFrame(data,columns=columns)
        df['x'] = df['x'].astype('float')
        df['y'] = df['y'].astype('float')
        df['z'] = df['z'].astype('float')
        data = df.to_numpy()
        data = data.reshape(-1, 90, 3)
# =============================================================================
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
# =============================================================================
# Previsão do modelo carregado
# =============================================================================
# Faça uma única previsão com o modelo carregado
        class_predict = [category_mapping[np.argmax(pred)] for pred in predictions]
# =============================================================================
        try:
            loaded_data = json.loads(class_predict)
            return jsonify({'args': str(data), 'is_well_formed': True})
        except json.JSONDecodeError as json_error:
            return jsonify({'error': f'JSON recomposto mal formado: {json_error}', 'is_well_formed': False})        
        #return jsonify({'args': str(recomposed_json)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

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


