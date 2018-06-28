# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request
import pandas as pd

app = Flask(__name__)


x = pd.read_csv('./tspmod2015.csv')

@app.route('/api/v1.0/exhibits', methods=['GET'])
def get_exhibits():
  args = request.args
  country = args['country']
  exhibit = x.loc[(x['EXHIBITION_COUNTRY'].isin([country])) &
                  (x['svd'] > 0.5)].fillna('null').to_dict('records')
  if not exhibit:
    abort(404)
  return jsonify({'exhibits': exhibit})

#@app.route('/api/v1.0/exhibits', methods=['GET'])
#def get_exhibits():
#  return jsonify({'exhibits': exhibits})

@app.route('/api/v1.0/exhibits/<int:exhibit_id>', methods=['GET'])
def get_site(exhibit_id):
  exhibit = filter(lambda d: d['id'] == exhibit_id, exhibits)
  exhibit = list(exhibit)
  if not exhibit:
    abort(404)
  return jsonify({'exhibit': exhibit[0]})

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/exhibits', methods=['POST'])
def create_exhibit():
  if not request.json or not 'exhibit' in request.json:
    abort(400)
  exhibit = {
    'id': exhibits[-1]['id'] + 1,
    'exhibit': request.json['exhibit'],
    'list': request.json.get('list', [])
  }
  exhibits.append(exhibit)
  return jsonify({'exhibit': exhibit}), 201

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)

