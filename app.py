
"""
API Flask simples.
"""
from flask import Flask, make_response, jsonify, request
from db import Carros


app = Flask(__name__)

@app.route('/carros', methods=['GET'])
def get_carros():
    """Endpoint para retornar a lista de carros."""
    return make_response(
        jsonify(
                message='Lista de carros',
                carros=Carros)
    )

@app.route('/carros', methods=['POST'])
def create_carro():
    """
    Cria um novo carro a partir do payload JSON enviado na requisição.
    """
    carro = request.json
    Carros.append(carro)
    return make_response(
        jsonify(
            message='Carro criado com sucesso',
            carro=carro
        )
    )

app.run()
