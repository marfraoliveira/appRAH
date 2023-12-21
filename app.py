from flask import Flask,request,jsonify  
import numpy as np
import pandas as pd
import json
from json import JSONEncoder
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
import keras
from keras.models import load_model,model_from_json
import jsonschema
from jsonschema import validate
from sklearn.metrics import accuracy_score
from flask_cors import CORS
from statistics import mode


# =============================================================================

# =============================================================================
# CARREGAR O MODELO DE DL
# =============================================================================
# Model saved with Keras model.save()
MODEL_PATH = 'modelCNN.h5'

#Load your trained model
#model = load_model(MODEL_PATH)

loaded_model = tf.keras.saving.load_model("modelCNN.h5")


# Verifique se o modelo foi carregado com sucesso
if isinstance(loaded_model, keras.models.Model):
    print("O modelo" + MODEL_PATH + " foi carregado com sucesso.")
else:
    print("Ocorreu um erro ao carregar o modelo.")

app = Flask(__name__)
CORS(app)
#%%

@app.route('/api', methods=['POST'])
def receber_dados():
    global classificacoes_list  # Indica que a variável está no escopo global
    try:
        #data = 
        data = request.get_json()
        if "data" in data:
        # Excluindo o último registro se estiver mal formado
            if not all(key in data["data"][-1] for key in ["x", "y", "z", "timestamp"]):
                del data["data"][-1]
# Recompondo o JSON
        recomposed_json = json.dumps(data, indent=4)
# Convertendo a string JSON para uma lista Python
        lista_python = json.loads(recomposed_json)['data']
        #print(lista_python)    
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
        #print(df)
        data = df.to_numpy()
        #data = data[:len(data)//10] # Pego 10% dos dados enviados
        tamanho_data = data.size
        print('Quantidade de registros: '+str(len(lista_python)))
        print('tamanho dos dados numpy: '+str(tamanho_data))
        print('Dados Numpy:' + str(data) )
# =============================================================================
# Pre processamento novo
        if data.shape[1:] != (90, 3):
            # Determine quantos registros devem ser descartados ou ajustados
            ajuste_necessario = data.shape[1] - 90
            
            # Descarte os primeiros registros
            data = data[:, ajuste_necessario:]
# =============================================================================
        
          # Parâmetros da janela deslizante
            tamanho_janela = 90  # Defina o tamanho da janela conforme necessário

          # Crie todas as janelas deslizantes
            janelas_deslizantes = []
# =============================================================================
            for i in range(len(data) - tamanho_janela + 1):
              janela_deslizante = data[i:i + tamanho_janela]
              janelas_deslizantes.append(janela_deslizante)
# =============================================================================
# Converta as janelas para um array numpy
            janelas_deslizantes = np.array(janelas_deslizantes)
    
# Agora você pode usar 'janelas_deslizantes' conforme necessário em seu código
          # por exemplo, imprimir uma janela:
            #print("Primeira janela deslizante:")
            #print(janelas_deslizantes[0])
            
# Inicialize um array para armazenar as previsões
            previsoes = np.array([])
                
# Faça previsões para cada janela deslizante
            category_mapping = {
                  0: 'Walking',
                  1: 'Jogging',
                  2: 'Upstairs',
                  3: 'Downstairs',
                  4: 'Sitting',
                  5: 'Standing'
            }  
        previsoes = []
        #global atividade_predita_final
        # Faça previsões para todas as janelas deslizantes de uma vez
        resultado_previsao = loaded_model.predict(np.array(janelas_deslizantes))
        print(resultado_previsao)
        # Obtenha as categorias preditas para cada janela
        categorias_preditas = np.argmax(resultado_previsao, axis=1)
        # Mapeie as categorias para as atividades usando list comprehension
        previsoes = [category_mapping[categoria] for categoria in categorias_preditas]

        # Calcule a moda das previsões
        atividade_predita_final = mode(previsoes)
        print('>>>>>',atividade_predita_final)
 
        try:
            return jsonify({'Reconhecimento': str('Classificacao da atividade: '+ str(resultado_previsao)), 'O retorno eh bem formado': True})
        except json.JSONDecodeError as json_error:
            return jsonify({'error': f'JSON recomposto mal formado: {json_error}', 'is_well_formed': False})       
        
    except Exception as e:
        return jsonify({'error': str(e)})
   
 # =============================================================================

#@app.route('/recuperar_solicitacoes', methods=['GET'])
#def recuperar_solicitacoes():
    #global atividade_predita_final  # Indica que a variável está no escopo global
    # Calcular a moda da lista
    #if atividade_predita_final:
        #moda = mode(atividade_predita_final)
    #else:
        #moda = None

    #return jsonify({'Classificação:': atividade_predita_final})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
