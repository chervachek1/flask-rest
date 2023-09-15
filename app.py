from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
product_categories = db.Table('product_categories',
                              db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                              db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                              )


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    categories = db.relationship("Category", backref="categories", secondary=product_categories)


# Category Class/Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    products = db.relationship("Product", backref="products", secondary=product_categories)


# Product Schema
class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    qty = fields.Int(required=True)


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ProductSchema(PlainProductSchema):
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)


class CategorySchema(PlainCategorySchema):
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
