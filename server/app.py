#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

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

    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "created_at": bakery.created_at,
            "id": bakery.id,
            "name": bakery.name,
            "updated_at": bakery.updated_at  
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )

    return response
    
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        bakery_dict,
        200
    )

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.all()

    baked_goods.sort(key=lambda bg: bg.price, reverse=True)

    baked_goods_dicts = []
    for bg in baked_goods:
        baked_goods_dicts.append(bg.to_dict())

    response = make_response(
        jsonify(baked_goods_dicts),
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    mebg = BakedGood.query.order_by(BakedGood.price.desc()).first()

    response = make_response(
        jsonify(mebg.to_dict()),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
