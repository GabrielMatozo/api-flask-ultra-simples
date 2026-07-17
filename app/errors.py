from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(message="Requisição inválida"), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(message="Recurso não encontrado"), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(message="Método não permitido"), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(message="Erro interno do servidor"), 500
