# -*- coding: utf-8 -*-

import json
import math
import pandas as pd


def dropnull_data(path):
    data = pd.read_csv(path, delimiter='\t')
    data = data.dropna(how='all', axis=1)
    data.to_csv('../data/data_dropona.csv')


def read_csv(path):
    return pd.read_csv(path)


def load_graph(file_number):
    graph = json.load(open('../../src/data/random/' + str(file_number) + '.json', 'r'))
    return graph


def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0]) * (p0[0] - p1[0]) + (p0[1] - p1[1]) * (p0[1] - p1[1]))


class AOIPreprocess():
    def __init__(self, gaze_data):
        self.each_block = 20
        self.xvs, self.yvs, self.circles = [], [], []
        self.ratio = 1
        self.x_offset = 0
        self.y_offset = 0
        self.gaze_data = gaze_data

    def inpolygon(self, x, y, xs, ys):
        if x >= xs[0] and x <= xs[1]:
            if y >= ys[0] and y <= ys[3]:
                return True
            else:
                return False
        else:
            return False

    def process(self):
        for i in range(len(self.gaze_data)):
            block = int(data['RecordingName'][i][-1]) - 1
            segment = int(data['SegmentName'][i][-1]) - 1
            file_number = block * self.each_block + segment
            graph = load_graph(file_number)

            if graph['layout'] == 'FDGIB':
                layout_num = 0
            elif graph['layout'] == 'TRGIB':
                layout_num = 1

            self.set_group_data(graph)
            self.set_AOI(graph)
            print(self.gaze_data['AOI'])

    def set_group_data(self, graph):
        for group in graph['groups']:
            if group != graph['groups'][-1]:
                x = group['x'] * self.ratio + self.x_offset
                y = group['y'] * self.ratio + self.y_offset
                dx = group['dx'] * self.ratio
                dy = group['dy'] * self.ratio
                self.xvs.append([x, x + dx, x + dx, x])
                self.yvs.append([y, y, y + dy, y + dy])
                center = [x + dx / 2, y + dy / 2]
                nodes = [node for node in graph['nodes'] if node['group'] == group['id']]
                coordinates = [[node['cx'] * self.ratio + self.x_offset, node['cy'] * self.ratio + self.y_offset] for node in nodes]
                ds = [distance(coordinates[i], center) for i in range(len(coordinates))]
                max_distance = max(ds)
                self.circles.append([center[0], center[1], max_distance])

    def set_AOI(self, graph):
        self.gaze_data['AOI'] = 0
        for fixation in range(0, len(self.gaze_data)):
            x = self.gaze_data['FixationPointX (MCSpx)'][fixation]
            y = self.gaze_data['FixationPointY (MCSpx)'][fixation]
            for group in range(graph['groupSize']):
                if pow(x - self.circles[group][0], 2) + pow(y - self.circles[group][1], 2) <= pow(self.circles[group][2], 2):
                    self.gaze_data['AOI'][fixation] = - group
                elif self.inpolygon(x, y, self.xvs[group], self.yvs[group]) and (pow(x - self.circles[group][0], 2) + pow(y - self.circles[group][1], 2) > pow(self.circles[group][2], 2)):
                    self.gaze_data['AOI'][fixation] = group


if __name__ == '__main__':
    path = '../data/data_dropona.csv'
    path = '../data/analyze-gib-sample-data.csv'
    data = read_csv(path)
    session = AOIPreprocess(data)
    session.process()
