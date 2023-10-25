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
    # Suponha que você tenha recebido dados JSON
    dados_json = request.get_json()
    try:
       # Tente validar os dados recebidos com o esquema
       validate(instance=dados_json, schema=schema)
       # Os dados são válidos
       return jsonify({"status": "Dados válidos"}), 200
    except Exception as e:
       # Erro de validação
       return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
