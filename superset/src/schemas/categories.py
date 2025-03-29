from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))


class CategoryWithProductsSchema(CategorySchema):
    products = fields.Nested('ProductSchema', many=True, exclude=('category',))
