# -*- coding: utf-8 -*-
"""
このモジュールの説明
"""

import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import numpy as np


class metrics():
    def __init__(self, data):
        self.data = data
        self.graph = nx.Graph()
        self.nodes = data['nodes']
        self.links = data['links']
        self.num_n = None
        self.num_l = None
        self.to_nxgraph()

    def to_nxgraph(self):
        node_list = []
        link_list = []
        for node in self.nodes:
            node_list.append(node["name"])
        for link in self.links:
            l = (link["source"], link["target"])
            link_list.append(l)

        self.graph.add_nodes_from(node_list)
        self.graph.add_edges_from(link_list)
        self.num_n = int(nx.number_of_nodes(self.graph))
        self.num_l = int(nx.number_of_edges(self.graph))

    def visualize(self):
        nx.draw(self.graph, node_size=50, node_color="b", pos=nx.spring_layout(self.graph, k=1/self.num_n))
        plt.show()

    def average_shortest_path_length(self):
        try:
            return nx.average_shortest_path_length(self.graph)
        except:
            print("the graph is not fully connected")
            return 0

    def degree(self):
        deg_list = []
        degrees = sorted(self.graph.degree())
        for _degree in degrees:
            deg_list.append(_degree[1])
        ave_dig = np.average(deg_list)
        return ave_dig

    def density(self):
        # return 2 * self.num_l / (self.num_n * (self.num_n - 1))
        return self.num_l / self.num_n

    def cluster_coef(self):
        return nx.average_clustering(self.graph)

    def writejson(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            data["averageDegree"] = self.degree()
            data["clusteringCoef"] = self.cluster_coef()
            data["density"] = self.density()
            data['average_shortest_path_length'] = self.average_shortest_path_length()
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == "__main__":
    levels = ['low/', 'high/']
    home = '../../src/data/'

    for level in levels:
        for file in os.listdir(home + level):
            if file != '.DS_Store':
                path = home + level + file
                print(path)
                data = json.load(open(path))
                metric = metrics(data)
                metric.writejson(path)
