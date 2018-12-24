# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 下午3:39
# -*- coding: utf-8 -*-
from flask import render_template, request,make_response
from _flask import app
from flask import jsonify
import json


# string
@app.route('/')
def hello_world():
    return "hello world"

@app.route('/users=<id>')   #直接绑定 接口 好像是比ruby rails 简单一点 http://127.0.0.1:5000/users=55
def hello_users(id):
    return "users: " + id


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/indexTest/', methods=['GET'])
def index_Iframe():
    return render_template('index.html')


