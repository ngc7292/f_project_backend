#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ngc7293'
__mtime__ = '2020/4/28'
"""


def get_node_temp(node_id, name, props, type, flag):
    return {
        'id': str(node_id),
        'name': name,
        'props': props,
        'type': type,
        'flag': flag
    }


def get_edges_temp(type, start_node_id, end_node_id, props):
    return {
        'type':type,
        'source': str(start_node_id),
        'target': str(end_node_id),
        'value': props
    }
