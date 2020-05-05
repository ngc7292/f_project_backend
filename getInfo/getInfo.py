#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'getInfo'
__author__ = 'ngc7293'
__mtime__ = '2020/4/22'
"""
from py2neo import Graph, NodeMatcher, RelationshipMatcher
from py2neo.data import walk
from nodeTemp.nodeTemp import *
from Help.RemoteTime import *
import json
from threading import Thread


class getInfo():
    """
    this class is from name to info every func is return node or nodelist or none
    """

    def __init__(self):
        self.graph = Graph('http://121.196.223.97:7474', username='neo4j', password='feizhaoye001')
        self.NodeMatcher = NodeMatcher(self.graph)
        self.RelationshipMather = RelationshipMatcher(self.graph)

    def getPerson(self, p_name):
        """
        get person node
        :param p_name: person's name
        :return: None or Node's list
        """
        # print(self.graph.run("match (n:Person) WHERE n.p_name=~'卢迈?' return n.p_name"))
        return list(self.NodeMatcher.match("Person").where("_.p_name=~ '.*" + p_name + ".*'"))

    def getCompany(self, c_name):
        return list(self.NodeMatcher.match("Company").where("_.c_name=~ '.*" + c_name + ".*'"))

    def getSharHolder(self, s_name):
        return list(self.NodeMatcher.match("ShareHolder").where("_.s_name=~ '.*" + s_name + ".*'"))

    def getServeFromCompany(self, c_node):
        relation_res = self.RelationshipMather.match({c_node}, r_type="serve")
        return [list(walk(i)) for i in list(relation_res)]

    def getServeFromPerson(self, p_node):
        relation_res = self.RelationshipMather.match({p_node}, r_type="serve")
        return [list(walk(i)) for i in list(relation_res)]

    def getHoldFromSH(self, sh_node):
        relation_res = self.RelationshipMather.match({sh_node}, r_type="hold")
        return [list(walk(i)) for i in list(relation_res)]

    def getHoldFromCompany(self, c_node):
        relation_res = self.RelationshipMather.match({c_node}, r_type="hold")
        return [list(walk(i)) for i in list(relation_res)]

    def getRelationFromCompany(self, c_name):
        res_data = {
            'nodes': [],
            'remain_nodes': [],
            'edges': [],
            'status': ''
        }
        node_list = []

        c_nodes = self.getCompany(c_name)
        if not c_nodes:
            res_data['status'] = 'company error'
            return res_data

        c_node_first = c_nodes[0]
        res_data['nodes'].append(get_node_temp(c_node_first.identity, c_node_first['c_name'], dict(c_node_first), 1, 1))
        node_list.append(c_node_first.identity)

        for node in c_nodes[1:]:
            res_data['remain_nodes'].append(get_node_temp(node.identity, node['c_name'], dict(node), 1, 3))
            node_list.append(node.identity)

        c_serves = self.getServeFromCompany(c_node_first)

        for serve in c_serves:
            time_s = dict(serve[1])['s_end_time'] if dict(serve[1]).get('s_end_time') else FuTime()
            if checkTime(time_s):
                res_data['edges'].append(get_edges_temp(1, serve[0].identity, serve[2].identity, dict(serve[1])))
                res_data['nodes'].append(get_node_temp(serve[0].identity, serve[0]['p_name'], {}, 2, 2))
            else:
                res_data['remain_nodes'].append(get_node_temp(serve[0].identity, serve[0]['p_name'], {}, 2, 3))

        c_holds = self.getHoldFromCompany(c_node_first)

        for hold in c_holds:
            res_data['edges'].append(get_edges_temp(2, hold[0].identity, hold[2].identity, dict(hold[1])))
            res_data['nodes'].append(get_node_temp(hold[0].identity, hold[0]['s_name'], {}, 3, 2))

        res_data['status'] = 'success'
        return res_data

    def getRelationFromPerson(self, p_name):
        res_data = {
            'nodes': [],
            'remain_nodes': [],
            'edges': [],
            'status': ''
        }
        node_list = []

        p_nodes = self.getPerson(p_name)

        if not p_nodes:
            res_data['status'] = "Person error"
            return res_data

        p_node_first = p_nodes[0]
        res_data['nodes'].append(get_node_temp(p_node_first.identity, p_node_first['p_name'], dict(p_node_first), 2, 1))

        for node in p_nodes[1:]:
            res_data['remain_nodes'].append(get_node_temp(node.identity, node['p_name'], dict(node), 1, 3))

        p_serves = self.getServeFromPerson(p_node_first)

        for serve in p_serves:
            time_s = dict(serve[1])['s_end_time'] if dict(serve[1]).get('s_end_time') else FuTime()
            if checkTime(time_s):
                res_data['edges'].append(get_edges_temp(1, serve[0].identity, serve[2].identity, dict(serve[1])))
                res_data['nodes'].append(get_node_temp(serve[2].identity, serve[2]['c_name'], dict(serve[2]), 1, 2))
            else:
                res_data['remain_nodes'].append(
                    get_node_temp(serve[2].identity, serve[2]['name'], dict(serve[2]), 1, 3))

        res_data['status'] = 'success'
        return res_data

    def getRelationFromHolder(self, sh_name):
        res_data = {
            'nodes': [],
            'remain_nodes': [],
            'edges': [],
            'status': ''
        }

        sh_nodes = self.getSharHolder(sh_name)

        if not sh_nodes:
            res_data['status'] = 'shareholder error'
            return res_data

        sh_node_first = sh_nodes[0]
        res_data['nodes'].append(
            get_node_temp(sh_node_first.identity, sh_node_first['s_name'], dict(sh_node_first), 3, 1))

        for sh_node in sh_nodes[1:]:
            res_data['remain_nodes'].append(get_node_temp(sh_node.identity, sh_node['s_name'], dict(sh_node), 3, 3))

        sh_serves = self.getHoldFromSH(sh_node_first)

        sh_holds = self.getHoldFromSH(sh_node_first)

        for hold in sh_holds:
            res_data['edge'].append(get_edges_temp(2, hold[0].identity, hold[2].identity, dict(hold[1])))
            res_data['nodes'].append(get_node_temp(hold[2].identity, hold[2]['c_name'], dict(hold[2]), 1, 2))

        res_data['status'] = 'success'
        return res_data

    def getDataFromCompany(self, c_name):
        res_data = {
            'c_p': {
                'nodes': [],
                'edges': [],
            },
            'c_s': {
                'nodes': [],
                'edges': [],
            },
            'remain_node': [],
            'status': ''
        }

        node_list_1 = []
        node_list_2 = []
        c_nodes = self.getCompany(c_name)
        if c_nodes is None:
            res_data['status'] = 'error'
            return res_data

        c_node_f = c_nodes[0]
        res_data['c_p']['nodes'].append(get_node_temp(c_node_f.identity, c_node_f['c_name'], dict(c_node_f), 1, 1))
        res_data['c_s']['nodes'].append(get_node_temp(c_node_f.identity, c_node_f['c_name'], dict(c_node_f), 1, 1))
        node_list_1.append(c_node_f.identity)
        node_list_2.append(c_node_f.identity)
        for c_node in c_nodes[1:]:
            res_data['remain_node'].append(get_node_temp(c_node.identity, c_node['c_name'], dict(c_node), 1, 1))

        c_serves = self.getServeFromCompany(c_node_f)
        for serve in c_serves:
            time_s = dict(serve[1])['s_end_time'] if dict(serve[1]).get('s_end_time') else FuTime()
            if checkTime(time_s):
                res_data['c_p']['edges'].append(get_edges_temp(1, serve[0].identity, serve[2].identity, dict(serve[1])))
                res_data['c_p']['nodes'].append(
                    get_node_temp(serve[0].identity, serve[0]['c_name'], dict(serve[0]), 2, 2))
                node_list_1.append(serve[0].identity)

                p_node = serve[0]
                p_serves = self.getServeFromPerson(p_node)
                for s in p_serves:
                    time_s = dict(s[1])['s_end_time'] if dict(s[1]).get('s_end_time') else FuTime()
                    if checkTime(time_s):
                        res_data['c_p']['edges'].append(get_edges_temp(1, s[0].identity, s[2].identity, dict(s[1])))
                        if s[2].identity not in node_list_1:
                            res_data['c_p']['nodes'].append(
                                get_node_temp(s[2].identity, s[2]['c_name'], dict(s[2]), 1, 3))
                            node_list_1.append(s[2].identity)
                    else:
                        res_data['c_p']['edges'].append(get_edges_temp(2, s[0].identity, s[2].identity, dict(s[1])))
                        if s[2].identity not in node_list_1:
                            res_data['c_p']['nodes'].append(
                                get_node_temp(s[2].identity, s[2]['c_name'], dict(s[2]), 1, 3))
                            node_list_1.append(s[2].identity)

        c_holds = self.getHoldFromCompany(c_node_f)
        for hold in c_holds:
            res_data['c_s']['nodes'].append(get_node_temp(hold[0].identity, hold[0]['s_name'], dict(hold[0]), 3, 2))
            res_data['c_s']['edges'].append(get_edges_temp(2, hold[0].identity, hold[2].identity, dict(hold[1])))
        res_data['status'] = 'success'
        return res_data

    def getDataFromCompany_mul(self, c_name):
        res_data = {
            'c_p': {
                'nodes': [],
                'edges': [],
            },
            'c_s': {
                'nodes': [],
                'edges': [],
            },
            'remain_node': [],
            'status': ''
        }

        c_nodes = self.getCompany(c_name)
        if c_nodes is None:
            res_data['status'] = 'error'
            return res_data

        c_node_f = c_nodes[0]
        for c_node in c_nodes[1:]:
            res_data['remain_node'].append(get_node_temp(c_node.identity, c_node['c_name'], dict(c_node), 1, 1))

        cp = None
        def get_serve_data(c_node):
            data = {
                'nodes': [],
                'edges': [],
            }
            node_list = [c_node.identity]
            c_serves = self.getServeFromCompany(c_node)
            for serve in c_serves:
                time_s = dict(serve[1])['s_end_time'] if dict(serve[1]).get('s_end_time') else FuTime()
                if checkTime(time_s):
                    data['edges'].append(get_edges_temp(1, serve[0].identity, serve[2].identity, dict(serve[1])))
                    data['nodes'].append(get_node_temp(serve[0].identity, serve[0]['p_name'], dict(serve[0]), 2, 2))
                    node_list.append(serve[0].identity)

                    p_node = serve[0]
                    p_serves = self.getServeFromPerson(p_node)
                    for s in p_serves:
                        time_s = dict(s[1])['s_end_time'] if dict(s[1]).get('s_end_time') else FuTime()
                        if checkTime(time_s):
                            data['edges'].append(get_edges_temp(1, s[0].identity, s[2].identity, dict(s[1])))
                            if s[2].identity not in node_list:
                                data['nodes'].append(get_node_temp(s[2].identity, s[2]['c_name'], dict(s[2]), 1, 3))
                                node_list.append(s[2].identity)
                        else:
                            data['edges'].append(get_edges_temp(2, s[0].identity, s[2].identity, dict(s[1])))
                            if s[2].identity not in node_list:
                                data['nodes'].append(get_node_temp(s[2].identity, s[2]['c_name'], dict(s[2]), 1, 3))
                                node_list.append(s[2].identity)
            res_data['c_p'] = data

        cs = None
        def get_hold_data(c_node):
            data = {
                'nodes': [],
                'edges': [],
            }
            node_list = [c_node.identity]
            c_holds = self.getHoldFromCompany(c_node)
            for hold in c_holds:
                data['nodes'].append(get_node_temp(hold[0].identity, hold[0]['s_name'], dict(hold[0]), 3, 2))
                data['edges'].append(get_edges_temp(2, hold[0].identity, hold[2].identity, dict(hold[1])))
            res_data['c_s'] = data

        t1 = Thread(target=get_serve_data, args=(c_node_f, ))
        t2 = Thread(target=get_hold_data, args=(c_node_f, ))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        res_data['c_p']['nodes'].append(get_node_temp(c_node_f.identity, c_node_f['c_name'], dict(c_node_f), 1, 1))
        res_data['c_s']['nodes'].append(get_node_temp(c_node_f.identity, c_node_f['c_name'], dict(c_node_f), 1, 1))

        res_data['status'] = 'success'
        return res_data


if __name__ == '__main__':
    a = getInfo()
    # print(a.getPerson("asd") is None)
    c = a.getCompany("银行")
    # for node in c:
    #     print(dict(node))

    # print(a.getHoldFromCompany(c[0])[0][0]['s_name'])
    # print(a.getRelationFromCompany("平安银行"))
    # print(a.getRelationFromPerson("袁成第"))
    # print(a.getRelationFromHolder("中国证券"))
    print(a.getDataFromCompany("平安"))
