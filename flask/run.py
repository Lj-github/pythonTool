# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 下午3:16
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"


@app.route('/users=<id>')   #直接绑定 接口 好像是比ruby rails 简单一点
def hello_users(id):
    return "users: " + id


if __name__ == '__main__':
    app.run()

