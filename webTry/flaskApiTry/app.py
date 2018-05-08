# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

departs = [{
    'id': 1,
    'depart': '行銷專案處',
    'list': [{'name': '清真推廣中心',
            'url': 'https://thpc.taiwantrade.com/',
            'description': '此網站可以幫國內廠商的產品做清真(國際)認證，以利銷往木斯林市場'},
           {'name': '台灣精品網站',
           'url': 'https://www.taiwanexcellence.org/tw',
            'description': '此網站提供廠商台灣精品選拔的資訊'},
           {'name': '全球政府採購商機網',
           'url': 'http://gpa.taiwantrade.com.tw/web/index.aspx#&panel1-2',
            'description': '主要將國外政府的標案商機與商情提供會員廠商，次要為說明會與電子報'}]
},
{
    'id': 2,
    'depart': '展覽業務處',
    'list': [{'name': '台灣國際專業展網站管理系統(TTS)',
            'description': ''},
            {'name': '臺灣國際專業展行動應用程式(Mobile App)',
            'description': '各種展的入口網站'},
            {'name': '台北專業展覽會後端管理系統',
            'description': ''},
            {'name': '參展廠商線上申請系統',
            'description': '如其名'},
            {'name': '國內廠商申請國外買主補助系統',
            'description': '如其名'}]
},
{
    'id': 3,
    'depart': '資訊及數據中心',
    'list': [{'name': '活動匯',
            'description': '貿協同仁可透過此網站舉辦講座、研討會、課程等活動；會員可透過此網站了解貿協舉辦的活動甚至報名'},
            {'name': '採洽易',
            'url': 'https://isourcing.taiwantrade.com.tw/internet/index.aspx',
            'description': '國內廠商可透過此網站在國內參加採購洽談會，也就是與國外買主洽談'},
            {'name': '展團行銷網站',
            'description': '國內廠商可透過此網站在國外參加採購洽談會，也就是與國外買主洽談'},
            {'name': '全球貿易大數據平台',
            'description': '國內廠商可透過此網站了解全球貿易商情'}]
}]

@app.route('/api/v1.0/departs', methods=['GET'])
def get_departs():
  return jsonify({'departs': departs})

@app.route('/api/v1.0/departs/<int:depart_id>', methods=['GET'])
def get_site(depart_id):
  depart = filter(lambda d: d['id'] == depart_id, departs)
  depart = list(depart)
  if not depart:
    abort(404)
  return jsonify({'depart': depart[0]})

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/departs', methods=['POST'])
def create_depart():
  if not request.json or not 'depart' in request.json:
    abort(400)
  depart = {
    'id': departs[-1]['id'] + 1,
    'depart': request.json['depart'],
    'list': request.json.get('list', [])
  }
  departs.append(depart)
  return jsonify({'depart': depart}), 201

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)

