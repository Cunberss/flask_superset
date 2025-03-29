from marshmallow import Schema, fields, validate


class SaleSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    date = fields.Date(required=True)
    discount = fields.Float(validate=validate.Range(min=0, max=1))
    total_price = fields.Method("calculate_total_price", dump_only=True)

    def calculate_total_price(self, obj):
        return round((obj.product.price * obj.quantity) * (1 - obj.discount), 2)


class SalesAnalyticsSchema(Schema):
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    limit = fields.Int(validate=validate.Range(min=1, max=100))

