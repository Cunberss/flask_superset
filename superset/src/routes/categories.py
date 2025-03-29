from flask import Blueprint, request, jsonify
from superset.src.services import CategoryService
from superset.src.db.base import get_session

bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@bp.route('/', methods=['GET'])
def get_all():
    try:
        with get_session() as session:
            service = CategoryService(session)
            categories = service.get_all()
            return jsonify(categories)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    try:
        with get_session() as session:
            service = CategoryService(session)
            category = service.create(data)
            return jsonify(category), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<int:category_id>', methods=['DELETE'])
def delete(category_id):
    try:
        with get_session() as session:
            service = CategoryService(session)
            success = service.delete(category_id)
            if not success:
                return jsonify({"error": "Category not found"}), 404
            return jsonify({"message": "Category deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500