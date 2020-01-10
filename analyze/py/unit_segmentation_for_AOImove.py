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
    count = 0
    old_AOI = data[index]['AOI']
    for step in range(time_window):
        position = index + step * direction
        if position >= 0 and position < len(data):
            try:
                if old_AOI != data[position]['AOI']:
                    old_AOI = data[position]['AOI']
                    count += 1
            except:
                if old_AOI is not None:
                    old_AOI = None
                    count += 1
        else:
            break
    return count


def calc_move(data):
    time_window_step = int(1000 / 20)
    for que in data:
        for participant in que:
            for segment in range(len(participant['segments'])):
                if participant['segments'][segment]['fixation']:
                    count_before = count_AOIs_in_a_time_window(participant['segments'], segment, -1, time_window_step)
                    count_after = count_AOIs_in_a_time_window(participant['segments'], segment, 1, time_window_step)
                    participant['segments'][segment]['AOIsBefore'] = count_before
                    participant['segments'][segment]['AOIsAfter'] = count_after
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
            outputs[que].append(dic)

    outputs = calc_move(outputs)

    f = open('../data/segmentedFixation.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f = open('../../src/data/eye-tracking/segmentedFixation.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
