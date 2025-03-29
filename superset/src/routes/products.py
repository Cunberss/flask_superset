from flask import Blueprint, request, jsonify
from superset.src.services import ProductService
from superset.src.db.base import get_session

bp = Blueprint('products', __name__, url_prefix='/api/products')


@bp.route('/', methods=['GET'])
def get_all():
    try:
        with get_session() as session:
            service = ProductService(session)
            products = service.get_all()
            return jsonify(products)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    try:
        with get_session() as session:
            service = ProductService(session)
            product = service.create(data)
            return jsonify(product), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<int:product_id>', methods=['PUT'])
def update(product_id):
    data = request.get_json()
    try:
        with get_session() as session:
            service = ProductService(session)
            product = service.update(product_id, data)
            if not product:
                return jsonify({"error": "Product not found"}), 404
            return jsonify(product)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    try:
        with get_session() as session:
            service = ProductService(session)
            success = service.delete(product_id)
            if not success:
                return jsonify({"error": "Product not found"}), 404
            return jsonify({"message": "Product deleted"}), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
