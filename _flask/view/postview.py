# -*- coding: utf-8 -*-
# @Time    : 2018/12/24 上午11:06
from flask import render_template, request, make_response
from _flask import app
from flask import jsonify
import json
from _flask.lib import lzstring
x = lzstring.LZString()

@app.route('/post/', methods=['POST'])
def postTest():
    username = request.values['username']  # json['username']
    content = request.values['content']  # .json['']
    print("username " + username)
    print("content " + content)
    loader = {}
    loader['dd'] = 5
    return json.dumps(loader), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/mydict', methods=['GET', 'POST'])
def mydict():
    id =  request.values['id']
    ff = request.values['ff']
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)


@app.route('/postSaveTxt/', methods=['POST'])
def postSaveTxt():
    username = request.values['username']
    #content = x.decompress(request.values['content'])
    content =request.values['content']
    print('username  ' + username)
    with open("static/txt/" + username, 'w') as f:
        f.write(content)
    loader = {}
    loader['dd'] = 'success'
    return json.dumps(loader), 200, {'Content-Type': 'application/json; charset=utf-8'}

basedir = '/Users/admin/Documents/ljworkspace/local/python/pythonTool/_flask'

@app.route('/postSaveImg', methods=['POST'])#,strict_slashes=False
def postSaveImg():
    img = request.files.get('photo')
    username = request.form.get("name")
    path = basedir + "/static/photo/"
    file_path = path + img.filename
    img.save(file_path)
    print('上传头像成功，上传的用户是：' + username)
    return render_template('index.html')

