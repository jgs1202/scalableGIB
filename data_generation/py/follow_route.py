import os
import json
from random import randint
import networkx as nx
import sys
import matplotlib.pyplot as plt


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
                print(str(node.id) + " ", end="" )
        print(" ")


def difficulty(data, source, target):
    print('calculating difficulty...')
    links = data['links']
    shortest_length = data['shortest_path']['length']
    depth_margin = 2
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


def set_shortest_path(data, source, target):
    graph = nx.readwrite.json_graph.node_link_graph(data)
    length = len(graph.nodes)
    verify = True
    count = 0
    total_path_length = 0

    data['shortest_path'] = {}
    data['shortest_path']['path'] = []
    sps = nx.all_shortest_paths(graph, source=source, target=target)
    data['shortest_path']['nodes'] = [source, target]

    for sp in sps:
        data['shortest_path']['path'].append(sp)
        data['shortest_path']['length'] = len(sp)
    total_path_length += data['shortest_path']['length']
    return data


def route_upto_depth(data, shortest_length):
    print('searching 2 nodes...')
    links = data['links']
    depth_margin = 2
    flag = False
    calc_num = 0

    def append_child_nodelist(parent, id):
        parent.append_child(id)
        nodes.append(parent.children[-1])

    # choose one node randomly
    while flag is False:
        nodes = []
        tree = Tree('header', None, -1)
        source = randint(0, len(data['nodes']) - 1)
        append_child_nodelist(tree, source)

        print('constructing tree')
        for depth in range(shortest_length + depth_margin):
            parents = [node for node in nodes if node.depth == depth]
            for parent in parents:
                for link in links:
                    if link['source'] == parent.id:
                        append_child_nodelist(parent, int(link['target']))
                    elif link['target'] == parent.id:
                        append_child_nodelist(parent, int(link['source']))
            dupli_check(nodes, depth + 1)
            print(len(nodes))
        print('tree end')

        leaves = []
        for d in range(depth_margin + 1):
            leaves.append([node.id for node in nodes if node.depth == shortest_length - 1 + d])
        total_leaves = sum([len(leaf) for leaf in leaves])

        # keyを並べて、各々に対し出現確率（＝難しさ）を計算　適当なものをtaretとして選ぶ
        keys = []
        for leaf in leaves:
            keys.extend(list(set(leaf)))
        keys = list(set(keys))

        difficulties = []
        for key in keys:
            count = 0
            for leaf in leaves:
                count += leaf.count(key)
            difficulties.append(count / total_leaves)

        for num, diff in enumerate(difficulties):
            if diff > 0.05 and diff <= 0.1:
                target = keys[num]
                data = set_shortest_path(data, source, target)
                set_answer(nodes, data, target)
                print(diff, difficulties[num])
                data['shortest_path']['difficulty'] = difficulties[num]
                flag = True
                break

        if calc_num % 100 == 0 and calc_num != 0:
            print('calclation step: ' + str(calc_num))
            print(difficulties)
        calc_num += 1


def routing():
    levels = ['low/', 'high/']
    home = '../../src/data/'
    depth = 5

    for level in levels:
        for file in os.listdir(home + level):
            if file != '.DS_Store':
                data = json.load(open(home + level + file))
                print(home + level + file)
                data['directed'] = False
                data['multigraph'] = False
                route_upto_depth(data, depth)
                f = open(home + level + file, 'w')
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    routing()
