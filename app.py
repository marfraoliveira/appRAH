import time
from distutils.log import debug
from fileinput import filename
from flask import *  
from flask import Flask,request,jsonify  
import numpy as np
import pandas as pd
from keras.models import model_from_json
import json
from json import JSONEncoder
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
import keras
from keras.models import load_model
import jsonschema
from jsonschema import validate
from sklearn.metrics import accuracy_score
from threading import Timer
from flask_socketio import SocketIO, emit
import asyncio
#from aioflask import Flask, request, Response



app = Flask(__name__)

MODEL_PATH = 'modelExit.h5'
model = load_model(MODEL_PATH)

# Verifique se o modelo foi carregado com sucesso
if isinstance(model, keras.models.Model):
    print(f"O modelo {MODEL_PATH} foi carregado com sucesso.")
else:
    print("Ocorreu um erro ao carregar o modelo.")

async def fazer_previsoes_assincrono(model, janelas_deslizantes, n_janelas_por_predicao, category_mapping):
    previsoes_totais = np.array([])

    for i in range(0, len(janelas_deslizantes), n_janelas_por_predicao):
        grupo_janelas = janelas_deslizantes[i:i + n_janelas_por_predicao]
        previsao_grupo = model.predict(np.array(grupo_janelas))
        previsoes_totais = np.append(previsoes_totais, previsao_grupo)

    # Converta as previsões para classes previstas
    previsoes_totais = previsoes_totais.reshape(-1, len(category_mapping))
    classes_previstas = np.argmax(previsoes_totais, axis=1)
    classificacoes = [category_mapping[class_index] for class_index in classes_previstas]

    return classificacoes

@app.route('/api', methods=['POST'])
async def receber_dados():
    try:
        
        data = request.get_json()

        if "data" in data:
            if not all(key in data["data"][-1] for key in ["x", "y", "z", "timestamp"]):
                del data["data"][-1]

        recomposed_json = json.dumps(data, indent=4)
        lista_python = json.loads(recomposed_json)['data']

        parsed_data = json.loads(recomposed_json)
        data = np.array([[item["x"], item["y"], item["z"]] for item in parsed_data["data"]])

        columns = ['x', 'y', 'z']
        df = pd.DataFrame(data, columns=columns)
        df['x'] = df['x'].astype('float')
        df['y'] = df['y'].astype('float')
        df['z'] = df['z'].astype('float')
        data = df.to_numpy()

        if data.shape[1:] != (90, 3):
            ajuste_necessario = data.shape[1] - 90
            data = data[:, ajuste_necessario:]

        tamanho_janela = 90
        janelas_deslizantes = []

        for i in range(len(data) - tamanho_janela + 1):
            janela_deslizante = data[i:i + tamanho_janela]
            janelas_deslizantes.append(janela_deslizante)

        janelas_deslizantes = np.array(janelas_deslizantes)

        print("Primeira janela deslizante:")
        print(janelas_deslizantes[0])

        previsoes = np.array([])
        category_mapping = {0: 'Walking', 1: 'Jogging', 2: 'Upstairs', 3: 'Downstairs', 4: 'Sitting', 5: 'Standing'}
        previsoes = np.array([])
        classificacoes_list = []
        n_janelas_por_predicao = 100

        classificacoes_list = await fazer_previsoes_assincrono(model, janelas_deslizantes, n_janelas_por_predicao, category_mapping)

        return jsonify({'Reconhecimento': f'Classificacao da atividade: {classificacoes_list}', 'O retorno eh bem formado': True})

    except json.JSONDecodeError as json_error:
        return jsonify({'error': f'JSON recomposto mal formado: {json_error}', 'is_well_formed': False})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    import asyncio
    from aiohttp import web

    loop = asyncio.get_event_loop()
    app.config['loop'] = loop
    app.run(debug=False, host='0.0.0.0', port=5001)
