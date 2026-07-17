import math
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models import db, Carro
from app.schemas import carro_schema, carros_schema

carros_bp = Blueprint("carros", __name__)


@carros_bp.route("/carros", methods=["GET"])
def get_carros():
    """Lista carros com paginação e filtros.
    ---
    tags:
      - Carros
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: marca
        in: query
        type: string
      - name: modelo
        in: query
        type: string
      - name: ano
        in: query
        type: integer
    responses:
      200:
        description: Lista de carros
    """
    query = Carro.query

    marca = request.args.get("marca")
    if marca:
        query = query.filter(Carro.marca.ilike(f"%{marca}%"))

    modelo = request.args.get("modelo")
    if modelo:
        query = query.filter(Carro.modelo.ilike(f"%{modelo}%"))

    ano = request.args.get("ano")
    if ano:
        query = query.filter(Carro.ano == int(ano))

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = min(per_page, 100)

    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 0
    carros = query.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify(
        message="Lista de carros",
        carros=carros_schema.dump(carros),
        pagina={"page": page, "per_page": per_page, "total": total, "pages": pages},
    )


@carros_bp.route("/carros", methods=["POST"])
def create_carro():
    """Cria um novo carro.
    ---
    tags:
      - Carros
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            marca:
              type: string
            modelo:
              type: string
            ano:
              type: integer
    responses:
      201:
        description: Carro criado
      400:
        description: Dados inválidos
    """
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
    """Atualiza um carro existente.
    ---
    tags:
      - Carros
    parameters:
      - name: carro_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            marca:
              type: string
            modelo:
              type: string
            ano:
              type: integer
    responses:
      200:
        description: Carro atualizado
      404:
        description: Carro não encontrado
    """
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
    """Remove um carro.
    ---
    tags:
      - Carros
    parameters:
      - name: carro_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Carro removido
      404:
        description: Carro não encontrado
    """
    carro = db.session.get(Carro, carro_id)
    if not carro:
        return jsonify(message="Carro não encontrado"), 404

    db.session.delete(carro)
    db.session.commit()

    return jsonify(message="Carro removido com sucesso")
