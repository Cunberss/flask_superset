from flask import Blueprint, request, jsonify
from superset.src.services import SalesService
from superset.src.db.base import get_session
from superset.src.schemas.sales import SalesAnalyticsSchema

bp = Blueprint('sales', __name__, url_prefix='/api/sales')


@bp.route('/total', methods=['GET'])
def total_sales():
    schema = SalesAnalyticsSchema()
    errors = schema.validate(request.args)
    if errors:
        return jsonify({"error": errors}), 400

    validated_data = schema.load(request.args)  # Валидация запроса

    try:
        with get_session() as session:
            service = SalesService(session)
            result = service.get_total_sales(validated_data["start_date"], validated_data["end_date"])
            return jsonify(result)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/top-products', methods=['GET'])
def top_products():
    schema = SalesAnalyticsSchema()
    errors = schema.validate(request.args)
    if errors:
        return jsonify({"error": errors}), 400

    validated_data = schema.load(request.args)

    try:
        with get_session() as session:
            service = SalesService(session)
            result = service.get_top_products(validated_data["start_date"], validated_data["end_date"], validated_data.get("limit", 5))
            return jsonify({"products": result})

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
