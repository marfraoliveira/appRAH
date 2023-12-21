from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import json
import tensorflow as tf
from keras.models import load_model
from flask_cors import CORS
from statistics import mode

# Carregar o modelo de DL
MODEL_PATH = './modelCNN.h5'
loaded_model = tf.keras.models.load_model(MODEL_PATH)

# Verificar se o modelo foi carregado com sucesso
if isinstance(loaded_model, tf.keras.models.Model):
    print("O modelo " + MODEL_PATH + " foi carregado com sucesso.")
else:
    print("Ocorreu um erro ao carregar o modelo.")

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def receber_dados():
    try:
        data = request.get_json()
        if "data" in data:
            # Excluindo o último registro se estiver mal formado
            if not all(key in data["data"][-1] for key in ["x", "y", "z", "timestamp"]):
                del data["data"][-1]

            # Pré-processamento
            parsed_data = json.loads(json.dumps(data, indent=4))
            data = np.array([[item["x"], item["y"], item["z"]] for item in parsed_data["data"]])
            columns = ['x', 'y', 'z']
            df = pd.DataFrame(data, columns=columns)
            df['x'] = df['x'].astype('float')
            df['y'] = df['y'].astype('float')
            df['z'] = df['z'].astype('float')
            data = df.to_numpy()

            # Remova a parte do código relacionada ao janelamento
            if data.size > 0:
                print('Dados em data OK')
            else:
                print('Dados em data não OK')
            # Redimensionar os dados de entrada para ter tamanho 90
            data = data[-90:]
            # Se o tamanho da sequência não for 90, faça os ajustes necessários
            if data.shape[1] != 90:
                ajuste_necessario = data.shape[1] - 90
                data = data[:, ajuste_necessario:]

        
            # Faça a previsão diretamente a partir de 'data'
            resultado_previsao = loaded_model.predict(np.array([data]))
            print("Resultado da previsão:", resultado_previsao)

            # Obtenha as categorias preditas
            categorias_preditas = np.argmax(resultado_previsao, axis=1)
            category_mapping = {
                0: 'Walking',
                1: 'Jogging',
                2: 'Upstairs',
                3: 'Downstairs',
                4: 'Sitting',
                5: 'Standing'
            }
            previsao = category_mapping[categorias_preditas[0]]

            return jsonify({'Reconhecimento': f'Classificação da atividade: {previsao}', 'O retorno é bem formado': True})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
