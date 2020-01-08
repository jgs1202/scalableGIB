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
        self.ratio = 2.15
        self.x_offset = 247
        self.y_offset = 138
        self.gaze_data = gaze_data

    def inpolygon(self, x, y, xs, ys):
        if x >= xs[0] and x <= xs[1]:
            if y >= ys[0] and y <= ys[3]:
                return True
            else:
                return False
        else:
            return False

    def delete_data(self):
        rmList = ['StudioVersionRec', 'StudioProjectName', 'RecordingResolution', 'MediaPosX (ADCSpx)', 'MediaPosY (ADCSpx)', 'LocalTimeStamp', 'EyeTrackerTimestamp', 'SaccadicAmplitude', 'AbsoluteSaccadicDirection', 'RelativeSaccadicDirection', 'GazePointIndex', 'GazePointLeftX (ADCSpx)', 'GazePointLeftY (ADCSpx)', 'GazePointRightX (ADCSpx)', 'GazePointRightY (ADCSpx)', 'GazePointLeftX (ADCSmm)', 'GazePointLeftY (ADCSmm)', 'GazePointRightX (ADCSmm)', 'GazePointRightY (ADCSmm)', 'StrictAverageGazePointX (ADCSmm)', 'StrictAverageGazePointY (ADCSmm)', 'EyePosLeftX (ADCSmm)', 'EyePosLeftY (ADCSmm)', 'EyePosLeftZ (ADCSmm)', 'EyePosRightX (ADCSmm)', 'EyePosRightY (ADCSmm)', 'EyePosRightZ (ADCSmm)', 'DistanceLeft', 'DistanceRight', 'PupilLeft', 'PupilRight', 'ValidityLeft', 'ValidityRight']
        for word in rmList:
            self.gaze_data = self.gaze_data.drop(columns=word)

    def process(self):
        print('processing...')
        file_number = 0
        self.delete_data()
        self.gaze_data['AOI'] = 0
        self.gaze_data['AOIsBeforeFixation'] = 0
        self.gaze_data['AOIsAfterFixation'] = 0

        calc_margin = 100
        graph = load_graph(file_number)
        self.set_group_data(graph)
        for i in range(len(self.gaze_data) - calc_margin):
            if len(self.gaze_data) > 100:
                if i != 0 and i % int(len(self.gaze_data) / 10) == 0:
                    print(str(int(i / int(len(self.gaze_data) / 100))) + "% done...")
            block = int(self.gaze_data['RecordingName'][i][-1]) - 1
            try:
                segment = int(self.gaze_data['SegmentName'][i][-2:]) - 1
            except:
                segment = int(self.gaze_data['SegmentName'][i][-1]) - 1
            file_tmp = block * self.each_block + segment

            # print(file_tmp, file_number, block, segment, self.gaze_data['SegmentName'][i][-2:])
            if file_number != file_tmp:
                graph = load_graph(file_tmp)
                self.set_group_data(graph)
                file_number = file_tmp

            if graph['layout'] == 'FDGIB':
                layout_num = 0
            elif graph['layout'] == 'TRGIB':
                layout_num = 1

            self.set_AOI(graph, i)
        for i in range(len(self.gaze_data) - calc_margin):
            if i != 0 and i % int(len(self.gaze_data) / 10) == 0:
                print(str(int(i / int(len(self.gaze_data) / 100))) + "% done...")
            self.set_move(i)
        self.gaze_data.to_csv('../data/data_with_AOI.csv')

    def set_group_data(self, graph):
        self.xvs, self.yvs, self.circles = [], [], []
        for num, group in enumerate(graph['groups']):
            if group != graph['groups'][-1]:
                x = group['x'] * self.ratio + self.x_offset
                y = group['y'] * self.ratio + self.y_offset
                dx = group['dx'] * self.ratio
                dy = group['dy'] * self.ratio
                self.xvs.append([x, x + dx, x + dx, x])
                self.yvs.append([y, y, y + dy, y + dy])
                center = [x + dx / 2, y + dy / 2]
                nodes = [node for node in graph['nodes'] if node['group'] == num]
                coordinates = [[node['cx'] * self.ratio + self.x_offset, node['cy'] * self.ratio + self.y_offset] for node in nodes]
                ds = [distance(coordinates[i], center) for i in range(len(coordinates))]
                max_distance = max(ds)
                self.circles.append([center[0], center[1], max_distance])

    def set_AOI(self, graph, index):
        x = self.gaze_data['FixationPointX (MCSpx)'][index]
        y = self.gaze_data['FixationPointY (MCSpx)'][index]
        for group in range(graph['groupSize']):
            if self.inpolygon(x, y, self.xvs[group], self.yvs[group]):
                if graph['groupSize'] < group + 1:
                    print(graph['groupSize'], group + 1)
                self.gaze_data['AOI'][index] = group + 1

    def count_AOIs_in_a_time_window(self, index, direction, start, time_window):
        # direction is 1 or -1
        count = 0
        step = 1
        span = 0
        old_AOI = self.gaze_data['AOI'][index]
        while span < time_window:
            try:
                ref_start = self.gaze_data['RecordingTimestamp'][index + step * direction]
                ref_end = ref_start + self.gaze_data['GazeEventDuration'][index + step * direction]

                if direction == -1:
                    span = abs(start - ref_start)
                    if old_AOI != self.gaze_data['AOI'][index + step * direction]:
                        old_AOI = self.gaze_data['AOI'][index + step * direction]
                        if abs(start - ref_end) < time_window:
                            count += 1

                if direction == 1:
                    span = abs(start - ref_end)
                    if old_AOI != self.gaze_data['AOI'][index + step * direction]:
                        old_AOI = self.gaze_data['AOI'][index + step * direction]
                        if abs(start - ref_start) < time_window:
                            count += 1
                step += 1
            except:
                break
        return count

    def set_move(self, index):
        time_window = 1000 * 2
        start = self.gaze_data['RecordingTimestamp'][index]
        duration = self.gaze_data['GazeEventDuration'][index]
        end = start + duration
        mid = int(start + duration / 2)

        self.gaze_data['AOIsBeforeFixation'][index] = self.count_AOIs_in_a_time_window(index, -1, mid, time_window)
        self.gaze_data['AOIsAfterFixation'][index] = self.count_AOIs_in_a_time_window(index, 1, mid, time_window)


if __name__ == '__main__':
    # path = '../data/scalable-gib-data-only-first.tsv'
    # dropnull_data(path)
    path = '../data/data_dropona.csv'
    # path = '../data/analyze-gib-sample-data.csv'
    data = read_csv(path)
    session = AOIPreprocess(data)
    session.process()
