from flask import Flask,request,jsonify
import numpy as np
import pickle
import json

model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world"


@app.route('/predict',methods=['POST'])
def predict():
    cgpa = float(request.form.get('cgpa'))
    iq = float(request.form.get('iq'))
    profile_score = float(request.form.get('profile_score'))
    #input_query = np.array([[float(cgpa),float(iq),float(profile_score)]])
    input_query = np.array([[(cgpa),(iq),(profile_score)]])
    teste = dict({"cgpa":0.1,"iq":12,"profile_score":90})
    result = model.predict(input_query)[0]
    return jsonify({'Movimento':str(result),
                    'teste':teste
                    })



if __name__ == '__main__':
    app.run(debug=True)
