import os
import json
import random
import networkx as nx
import sys
import matplotlib.pyplot as plt


# 一つのノードから最短経路のパス（+1）数内でいける全てのノード分の答えのノードの割合を揃える
class Tree(object):
    def __init__(self, id, parent, depth):
        self.children = []
        self.id = id
        self.parent = parent
        self.depth = depth

    def append_child(self, id):
        self.children.append(Tree(id, self, self.depth + 1))


def dupli_check(nodes, depth):
    leaves = []
    for node in nodes:
        if node.depth == depth:
            leaves.append(node)

    for leaf in leaves:
        path = []
        current = leaf
        while current.parent.id != 'header':
            path.append(current.id)
            current = current.parent
        print(path)


def difficulty(data, source, target):
    links = data['links']
    shortest_length = data['shortest_path']['length']
    depth_margin = 2
    nodes = []
    tree = Tree('header', None, -1)

    def append_child_nodelist(parent, id):
        parent.append_child(id)
        nodes.append(parent.children[-1])

    append_child_nodelist(tree, source)

    parent = tree
    print(shortest_length)
    for depth in range(shortest_length - 1 + depth_margin):
        for child_num, child in enumerate(parent.children):
            for link in links:
                if link['source'] == child.id:
                    append_child_nodelist(child, link['target'])
                elif link['target'] == child.id:
                    append_child_nodelist(child, link['source'])
    # dupli_check(nodes, 2)
    for node in nodes:
        print(node.depth)


def pickup2nodes(data):
    graph = nx.readwrite.json_graph.node_link_graph(data)
    length = len(graph.nodes)
    data['shortest_path'] = {}
    data['shortest_path']['path'] = []
    verify = True
    while verify:
        try:
            rand = [random.randint(0, length), random.randint(0, length)]
            while rand[1] == rand[0] or data['nodes'][rand[0]]['group'] == data['nodes'][rand[1]]['group']:
                rand[1] = random.randint(0, length)
            sps = nx.all_shortest_paths(graph, source=rand[0], target=rand[1])
            data['shortest_path']['nodes'] = [rand[0], rand[1]]
            for sp in sps:
                data['shortest_path']['path'].append(sp)
                data['shortest_path']['length'] = len(sp)
            if data['shortest_path']['length'] <= 6 and data['shortest_path']['length'] > 4:
                verify = False
        except:
            pass
    difficulty(data, rand[0], rand[1])
    return data


def routing():
    levels = ['low/', 'high/']
    home = '../../src/data/'

    for level in levels:
        for file in os.listdir(home + level):
            if file != '.DS_Store':
                data = json.load(open(home + level + file))
                data['directed'] = False
                data['multigraph'] = False
                data = pickup2nodes(data)
                f = open(home + level + file, 'w')
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    routing()
