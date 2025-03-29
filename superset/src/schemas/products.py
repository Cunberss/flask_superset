from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    category_id = fields.Int(required=True)


class ProductCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    category_id = fields.Int(required=True)


class ProductWithSalesSchema(ProductSchema):
    sales = fields.Nested('SaleSchema', many=True, exclude=('product',))