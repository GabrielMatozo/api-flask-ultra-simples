from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Carro(db.Model):
    __tablename__ = "Carros"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
