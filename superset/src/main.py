from flask import Flask, jsonify
from flask_cors import CORS
from superset.src.extensions import cache
from superset.src.routes import products, categories, sales


def build_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object('superset.src.config')
    cache.init_app(app)

    app.register_blueprint(products.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(sales.bp)

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


flask_app = build_app()

if __name__ == '__main__':
    flask_app.run("0.0.0.0", port=5000, debug=True)
