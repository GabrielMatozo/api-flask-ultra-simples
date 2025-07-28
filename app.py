
"""
API Flask simples.
"""
import mysql.connector
from flask import Flask, make_response, jsonify, request

mydb = mysql.connector.connect(
    host="localhost",
    user="RootUser",
    password="MainPassword",
    database="CarrosDB"
)
app = Flask(__name__)


@app.route('/carros', methods=['GET'])
def get_carros():
    """Endpoint para retornar a lista de carros que está no banco de dados."""
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Carros")
        meus_carros = cursor.fetchall()
        carros = list()
        for carro in meus_carros:
            carros.append({
                'id': carro['id'],
                'marca': carro['marca'],
                'modelo': carro['modelo'],
                'ano': carro['ano']
            })
        return make_response(
            jsonify(
                message='Lista de carros',
                carros=carros)
        )
    except mysql.connector.Error as e:
        print('Erro no endpoint GET /carros:', e)
        return make_response(jsonify(message='Erro interno', erro=str(e)), 500)


@app.route('/carros', methods=['POST'])
def create_carro():
    """
    Cria um novo carro a partir do payload JSON enviado na requisição e salva no banco de dados.
    """
    try:
        carro = request.json
        cursor = mydb.cursor()
        sql = "INSERT INTO Carros (marca, modelo, ano) VALUES (%s, %s, %s)"
        valores = (carro['marca'], carro['modelo'], carro['ano'])
        cursor.execute(sql, valores)
        mydb.commit()
        carro['id'] = cursor.lastrowid
        return make_response(
            jsonify(
                message='Carro criado com sucesso',
                carro=carro
            )
        )
    except mysql.connector.Error as e:
        print('Erro no endpoint POST /carros:', e)
        return make_response(jsonify(message='Erro interno', erro=str(e)), 500)


# Atualizar carro existente
@app.route('/carros/<int:carro_id>', methods=['PUT'])
def update_carro(carro_id):
    """
    Atualiza um carro existente pelo ID usando os dados enviados no JSON.
    """
    try:
        dados = request.json
        cursor = mydb.cursor()
        sql = "UPDATE Carros SET marca=%s, modelo=%s, ano=%s WHERE id=%s"
        valores = (dados['marca'], dados['modelo'], dados['ano'], carro_id)
        cursor.execute(sql, valores)
        mydb.commit()
        if cursor.rowcount == 0:
            return make_response(jsonify(message='Carro não encontrado'), 404)
        return make_response(jsonify(message='Carro atualizado com sucesso'))
    except mysql.connector.Error as e:
        print('Erro no endpoint PUT /carros/<id>:', e)
        return make_response(jsonify(message='Erro interno', erro=str(e)), 500)


# Remover carro existente
@app.route('/carros/<int:carro_id>', methods=['DELETE'])
def delete_carro(carro_id):
    """
    Remove um carro existente pelo ID.
    """
    try:
        cursor = mydb.cursor()
        sql = "DELETE FROM Carros WHERE id=%s"
        cursor.execute(sql, (carro_id,))
        mydb.commit()
        if cursor.rowcount == 0:
            return make_response(jsonify(message='Carro não encontrado'), 404)
        return make_response(jsonify(message='Carro removido com sucesso'))
    except mysql.connector.Error as e:
        print('Erro no endpoint DELETE /carros/<id>:', e)
        return make_response(jsonify(message='Erro interno', erro=str(e)), 500)


app.run()
