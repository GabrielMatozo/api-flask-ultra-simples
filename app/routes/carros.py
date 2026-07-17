from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models import db, Carro
from app.schemas import carro_schema, carros_schema

carros_bp = Blueprint("carros", __name__)


@carros_bp.route("/carros", methods=["GET"])
def get_carros():
    carros = Carro.query.all()
    return jsonify(message="Lista de carros", carros=carros_schema.dump(carros))


@carros_bp.route("/carros", methods=["POST"])
def create_carro():
    try:
        dados = carro_schema.load(request.json)
    except ValidationError as e:
        return jsonify(message="Dados inválidos", erros=e.messages), 400

    carro = Carro(**dados)
    db.session.add(carro)
    db.session.commit()

    return (
        jsonify(message="Carro criado com sucesso", carro=carro_schema.dump(carro)),
        201,
    )


@carros_bp.route("/carros/<int:carro_id>", methods=["PUT"])
def update_carro(carro_id):
    carro = db.session.get(Carro, carro_id)
    if not carro:
        return jsonify(message="Carro não encontrado"), 404

    try:
        dados = carro_schema.load(request.json)
    except ValidationError as e:
        return jsonify(message="Dados inválidos", erros=e.messages), 400

    for key, value in dados.items():
        setattr(carro, key, value)
    db.session.commit()

    return jsonify(
        message="Carro atualizado com sucesso", carro=carro_schema.dump(carro)
    )


@carros_bp.route("/carros/<int:carro_id>", methods=["DELETE"])
def delete_carro(carro_id):
    carro = db.session.get(Carro, carro_id)
    if not carro:
        return jsonify(message="Carro não encontrado"), 404

    db.session.delete(carro)
    db.session.commit()

    return jsonify(message="Carro removido com sucesso")
