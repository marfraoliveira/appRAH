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
# Model saved with Keras model.save()
MODEL_PATH = 'modelCNN.h5'

#Load your trained model
model = load_model(MODEL_PATH)
print('Modelo carregado com sucesso...')


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
        print(df)
        data = df.to_numpy()
        data = data[:len(data)//1]
        tamanho_data = data.size
        print('tamanho dos dados numpy: '+str(tamanho_data))
        print('Dados Numpy:' + str(data) )
# =============================================================================
# Pre processamento
# Tamanho da janela (90, 3)
        janela = (90, 3)

# Inicialize uma lista para armazenar as previsões das janelas deslizantes
        previsoes = []

# Defina um critério de parada
        critério_de_parada = 0.9  # Exemplo: interromper quando a previsão for maior ou igual a 0.9
        janela_deslizante = np.array([])  # Inicialize a janela deslizante como uma matriz vazia

# Percorra os dados com uma janela deslizante
        for i in range(len(data) - janela[0] + 1):
            janela_deslizante = data[i:i + janela[0]]
            # Faça previsões com a janela deslizante
            #previsao = model.predict(janela_deslizante)
            previsao = model.predict(np.array([janela_deslizante]))
            previsoes.append(previsao)

# Calcule a previsão geral como a média das previsões individuais
        #previsao_geral = np.mean(previsoes)
        # 'previsao_geral' agora contém a previsão geral baseada na média das previsões
        
        # Suponha que 'category_mapping' seja o seu mapeamento de classes
        # Mapeie a previsão geral para a classe correspondente usando o category_mapping
# Mapear as previsões para as categorias
        category_mapping = {
            0: 'Walking',
            1: 'Jogging',
            2: 'Upstairs',
            3: 'Downstairs',
            4: 'Sitting',
            5: 'Standing'
        }
        #classificacao_geral = category_mapping[np.argmax(previsao_geral)]
        
        # 'classificacao_geral' agora contém a classe correspondente à previsão geral

        # Exiba a classificação geral
        #print("Classificação Geral:", classificacao_geral)

# =============================================================================
# Faça uma única previsão com o modelo carregado
        #predictions = model.predict(data)

# =============================================================================
# Previsão do modelo carregado
        # Faça previsões com as janelas deslizantes
        #previsoes = model.predict(janelas_deslizantes_numpy)
# =============================================================================
# Faça uma única previsão com o modelo carregado
        #class_predict = [category_mapping[np.argmax(pred)] for pred in predictions]
# =============================================================================
        try:
           loaded_data = json.loads(recomposed_json)
           return jsonify({'args': str(category_mapping), 'is_well_formed': True})
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
