from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/exportar', methods=['POST'])
def exportar():
    dados = request.get_json()
    if not dados:
        return jsonify({"status": "erro", "mensagem": "Nenhum dado recebido"}), 400

    with open("dados_instagram.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "sucesso", "mensagem": "Dados recebidos e salvos!"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
