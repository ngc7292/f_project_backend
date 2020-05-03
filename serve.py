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

app = Flask(__name__)


@app.route('/')
def index():
    pass


@app.route('/api/getInfo')
def get_info():
    pass


@app.route('/api/<type>', methods=['POST'])
def show_type(type):
    name = request.form['name']
    res_data = {
        'nodes': [],
        'eage': [],
        'remains_nodes':[],
        'status': ''
    }
    Help = getInfo()
    if type == "company":
        res_data = Help.getRelationFromCompany(name)
    elif type == "person":
        res_data = Help.getRelationFromPerson(name)
    elif type == "shareholder":
        res_data = Help.getRelationFromHolder(name)
    else:
        res_data['status'] = 'type is error'

    return json.dumps(res_data)


if __name__ == '__main__':
    app.run('0.0.0.0', '23333')
