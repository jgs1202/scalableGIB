# -*- coding: utf-8 -*-

import numpy as np
import os
import csv
import sys
import json
import matplotlib.pyplot as plt
import copy


def count_AOIs_in_a_time_window(data, index, direction, time_window):
    # direction is 1 or -1
    # saccadeはAOIととらえない　AOIの変化のみ記録
    count = 0
    try:
        old_AOI = data[index]['AOI']
    except:
        old_AOI = None
    for step in range(time_window):
        position = index + step * direction
        if position >= 0 and position < len(data):
            try:
                if old_AOI != data[position]['AOI']:
                    old_AOI = data[position]['AOI']
                    count += 1
            except:
                pass
        else:
            break
    return count


def count_AOIs_kind_in_a_time_window(data, index, direction, time_window):
    # direction is 1 or -1
    # saccadeはAOIととらえない　AOIの変化のみ記録
    AOIs = []
    try:
        AOIs.append(data[index]['AOI'])
    except:
        pass
    for step in range(time_window):
        position = index + step * direction
        if position >= 0 and position < len(data):
            try:
                if data[position]['AOI'] not in AOIs:
                    AOIs.append(data[position]['AOI'])
            except:
                pass
        else:
            break
    return len(AOIs)


def calc_move(data, total_step):
    time_window_step = int(total_step / 100)
    for que in data:
        for participant in que:
            for segment in range(len(participant['segments'])):
                count_before = count_AOIs_in_a_time_window(participant['segments'], segment, -1, time_window_step)
                count_after = count_AOIs_in_a_time_window(participant['segments'], segment, 1, time_window_step)
                kind_before = count_AOIs_kind_in_a_time_window(participant['segments'], segment, -1, time_window_step)
                kind_after = count_AOIs_kind_in_a_time_window(participant['segments'], segment, 1, time_window_step)

                participant['segments'][segment]['AOIsBefore'] = count_before
                participant['segments'][segment]['AOIsAfter'] = count_after
                participant['segments'][segment]['AOIKindsBefore'] = kind_before
                participant['segments'][segment]['AOIKindsAfter'] = kind_after
    return data


def main():
    data = json.load(open('../data/fixation_detail.json', 'r'))
    total_que = 120
    total_step = 1000
    outputs = [[] for que in range(total_que)]

    for que in range(total_que):
        src_data = json.load(open('../../src/data/random/' + str(que) + '.json', 'r'))

        for datum in data[que]:
            dic = copy.deepcopy(datum)
            dic['segments'] = [{"fixation": False} for i in range(total_step)]
            segStart = int(datum['segmentStart'])
            segEnd = int(datum['segmentEnd'])
            duration = segEnd - segStart

            for fixation in datum['fixations']:
                recStart = float(fixation['recStart'])
                recEnd = recStart + float(fixation['gazeDur'])
                startUnit = round((recStart - segStart) / duration * total_step)
                endUnit = round((recEnd - segStart) / duration * total_step)
                if endUnit > total_step:
                    endUnit = total_step
                for step in range(startUnit, endUnit):
                    dic['segments'][step]['fixation'] = True
                    dic['segments'][step]['AOI'] = fixation['AOI']
            del dic['fixations']
            dic['layout'] = src_data['layout']
            dic['groupSize'] = src_data['groupSize']
            outputs[que].append(dic)

    outputs = calc_move(outputs, total_step)

    f = open('../data/segmentedFixation.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f = open('../../src/data/eye-tracking/segmentedFixation.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
