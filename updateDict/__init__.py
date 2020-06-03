import py2neo

def updateData():
    graph = py2neo.Graph(uri="http://121.196.223.97:7474",username="neo4j",password="feizhaoye001")

    nodes = list(graph.nodes.match("Company"))

    with open("../dict/dict.txt","a+",encoding="utf-8") as fd:
        for node in nodes:
            fd.write(node['c_name']+" nt\n")

if __name__ == '__main__':
    updateData()