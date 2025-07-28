
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


app.run()
