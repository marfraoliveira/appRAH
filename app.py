from sklearn import tree
from flask import Flask,request,jsonify
import numpy as np
import pickle


model = pickle.load(open('modelkNN100Hz.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return "Eficiência de Energia em dispositivos Móveis"


@app.route('/predict',methods=['POST'])
def predict():
    x_axis = float((request.form.get('x_axis')))
    y_axis = float((request.form.get('y_axis')))
    z_axis = float((request.form.get('z_axis')))
    input_query = np.array([[x_axis,y_axis,z_axis]])
    result = model.predict(input_query)[0]
    return jsonify({'Movimento':str(result)})

if __name__ == '__main__':
    app.run(debug=True)

