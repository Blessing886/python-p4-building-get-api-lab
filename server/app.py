#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return make_response(jsonify(bakery.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()
    if most_expensive:
        return make_response(jsonify(most_expensive.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "No baked goods found"}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
