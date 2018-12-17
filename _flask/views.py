# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 下午3:39
# -*- coding: utf-8 -*-
from flask import render_template, request
from _flask import app
@app.route('/')
def hello_world():
    return "hello world"


@app.route('/users=<id>')   #直接绑定 接口 好像是比ruby rails 简单一点 http://127.0.0.1:5000/users=55
def hello_users(id):
    return "users: " + id


@app.route('/test=<id>')   #http://127.0.0.1:5000/test=55
def hello_test(id):
    return "test: " + id


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/indexTest/', methods=['GET'])
def index_Iframe():
    return render_template('index.html')

@app.route('/battle/<int:battle_id>', methods=['GET'])
def get_battle_script(battle_id):
    #loader = BattleResourceLoader()
    return '' #loader.load_script(battle_id), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/res/battle/', methods=['POST'])
def get_battle_resource():
    loader = {}
    forms0 = request.json['forms0']
    forms1 = request.json['forms1']
    skills = request.json['skills']
    if len(skills) is 0:
        skills = False
    return '' #loader.load_form_res(forms0, forms1,skills), 200, {'Content-Type': 'application/json; charset=utf-8'}

