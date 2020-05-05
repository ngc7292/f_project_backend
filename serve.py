#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ngc7293'
__mtime__ = '2020/4/28'
"""
from flask import Flask, request
import json
from getInfo.getInfo import *
from nodeTemp.nodeTemp import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    pass


@app.route('/api/getInfo')
def get_info():
    pass


@app.route('/api/company/<name>', methods=['GET'])
def show_type(name):
    Help = getInfo()
    res_data = Help.getDataFromCompany_mul(name)
    return json.dumps(res_data)


if __name__ == '__main__':
    app.run('0.0.0.0', '23333')
