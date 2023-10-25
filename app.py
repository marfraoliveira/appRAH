schema = {
    "type": "object",
    "properties": {
        "x": { "type": "number" },
        "y": { "type": "number" },
        "z": { "type": "number" },
        "timestamp": { "type": "string" }
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
