from marshmallow import Schema, fields, validate


class CarroSchema(Schema):
    id = fields.Integer(dump_only=True)
    marca = fields.String(required=True, validate=validate.Length(min=1, max=50))
    modelo = fields.String(required=True, validate=validate.Length(min=1, max=50))
    ano = fields.Integer(
        required=True,
        validate=validate.Range(min=1886, max=2030),
    )


carro_schema = CarroSchema()
carros_schema = CarroSchema(many=True)
