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
    for index, node in enumerate(nodes):
        if node.depth == depth:
            path = []
            current = node
            while current.id != 'header':
                path.append(current.id)
                current = current.parent
            for point in path:
                if path.count(point) > 1:
                    del nodes[index]
                    break


def set_answer(nodes, data, target):
    data['shortest_path']['answers'] = []
    for node in nodes:
        if node.id == int(target):
            path = []
            current = node
            while current.id != 'header':
                path.append(current.id)
                current = current.parent
            data['shortest_path']['answers'].append(path)


def vis_tree(nodes, depth):
    print("tree visualization")
    for d in range(depth):
        for node in nodes:
            if node.depth == d:
                print(str(node.id) + " ", end="")
        print(" ")


def difficulty(data, source, target):
    print('calculating difficulty...')
    links = data['links']
    shortest_length = data['shortest_path']['length']
    depth_margin = 1
    nodes = []
    tree = Tree('header', None, -1)

    def append_child_nodelist(parent, id):
        parent.append_child(id)
        nodes.append(parent.children[-1])

    append_child_nodelist(tree, source)

    for depth in range(shortest_length + depth_margin):
        parents = [node for node in nodes if node.depth == depth]
        for parent in parents:
            for link in links:
                if link['source'] == parent.id:
                    append_child_nodelist(parent, int(link['target']))
                elif link['target'] == parent.id:
                    append_child_nodelist(parent, int(link['source']))
        print(len(nodes))
        before = [node.id for node in nodes if node.depth == depth + 1]
        dupli_check(nodes, depth + 1)
        after = [node.id for node in nodes if node.depth == depth + 1]
        # print("depth" + str(depth + 1) + ": " + "the number of leaf nodes decrease " + str(len(after)) + " from " + str(len(before)))

    set_answer(nodes, data, target)

    leaves = []
    for d in range(depth_margin + 1):
        leaves.append([node.id for node in nodes if node.depth == shortest_length - 1 + d])
    nums_answer = [leaf.count(target) for leaf in leaves]
    num = sum([len(leaf) for leaf in leaves])

    # print(num, nums_answer, len(data['shortest_path']['path']))
    return sum(nums_answer) / num


def pickup2nodes(data):
    print('choosing 2 nodes...')
    graph = nx.readwrite.json_graph.node_link_graph(data)
    length = len(graph.nodes)
    verify = True
    count = 0
    total_path_length = 0
    while verify:
        try:
            data['shortest_path'] = {}
            data['shortest_path']['path'] = []
            rand = [random.randint(0, length - 1), random.randint(0, length - 1)]
            while rand[1] == rand[0] or data['nodes'][rand[0]]['group'] == data['nodes'][rand[1]]['group']:
                rand[1] = random.randint(0, length - 1)
            sps = nx.all_shortest_paths(graph, source=rand[0], target=rand[1])
            data['shortest_path']['nodes'] = [rand[0], rand[1]]
            for sp in sps:
                data['shortest_path']['path'].append(sp)
                data['shortest_path']['length'] = len(sp)
            count += 1
            total_path_length += data['shortest_path']['length']
            if data['shortest_path']['length'] <= 6 and data['shortest_path']['length'] >= 5:
                data['shortest_path']['difficulty'] = difficulty(data, rand[0], rand[1])
                verify = False
                # if data['shortest_path']['difficulty'] > 0.001 and data['shortest_path']['difficulty'] < 0.003:
                #     print(data['shortest_path']['difficulty'])
                #     verify = False
            if count % 100 == 0 and count != 0:
                print(data['shortest_path']['path'])
            if count > 100000:
                print('cannot find appropriate pair of nodes')
                print('the average path length is ' + str(total_path_length / count))

        except:
            pass
    return data


def routing():
    levels = ['low/', 'high/']
    home = '../../src/data/'

    for level in levels:
        for file in os.listdir(home + level):
            if file != '.DS_Store':
                data = json.load(open(home + level + file))
                print(home + level + file)
                data['directed'] = False
                data['multigraph'] = False
                data = pickup2nodes(data)
                f = open(home + level + file, 'w')
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    routing()
