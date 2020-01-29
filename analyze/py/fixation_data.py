# -*- coding: utf-8 -*-

import os
import csv
import sys
import json
import copy
import pandas as pd
from operator import itemgetter


def fixation_info(data, fixation_num):
    each_block = 20
    # print(data['ParticipantName'][fixation_num])
    participant = data['ParticipantName'][fixation_num]
    recName = data['RecordingName'][fixation_num]
    segmentName = data['SegmentName'][fixation_num]
    block = int(recName[-1]) - 1
    try:
        segment = int(segmentName[-2:]) - 1
    except:
        segment = int(segmentName[-1]) - 1
    que_number = block * each_block + segment
    return participant, que_number


def check_question(data, participant, que_number, fixation_num):
    _participant, _que_number = fixation_info(data, fixation_num)
    flag = False
    if que_number != _que_number:
        flag = True
    if participant != _participant:
        flag = True
    return flag


def init_data(participant, data, fixation_num):
    dic = {}
    dic['participant'] = participant
    dic['segmentStart'] = int(data['SegmentStart'][fixation_num])
    dic['segmentEnd'] = int(data['SegmentEnd'][fixation_num])
    dic['segmentDur'] = int(data['SegmentDuration'][fixation_num])
    dic['fixations'] = []
    return dic


def get_task_result(task_result, que_number, participant, dic):
    choices = [result for result in task_result if result['file'] == str(que_number) + '.json']
    names = [choice['username'] for choice in choices]
    choice = [choices[i] for i in range(len(choices)) if str(names[i]).upper() == str(participant).upper()]

    # print(str(names[0]).upper(), str(participant).upper())

    if len(choice) == 0:
        print(participant)
        for choice in choices:
            print(choice['username'])
        sys.exit()
    elif len(choice) > 1:
        print(choice[0]['username'], choice[1]['username'])
        sys.exit()

    keys = ['answer', 'file', 'path_length_difference', 'time']
    for key in keys:
        dic[key] = choice[0][key]
    dic['time_left'] = 30 * 1000 - int(dic['time'])


def write_down(outputs, dic, que_number):
    outputs[que_number].append(dic)


def sort_by_score(data):
    for que in data:
        sorted(que, key=itemgetter('answer', 'time_left'), reverse=True)


def main():
    data = pd.read_csv('../data/data_with_AOI.csv')
    task_result = json.load(open('../data/choice.json', 'r'))
    total = 120
    outputs = [[] for i in range(total)]

    participant, que_number = fixation_info(data[0:1], 0)
    dic = init_data(participant, data[0:1], 0)
    get_task_result(task_result, que_number, participant, dic)
    for fixation_num in range(len(data)):
        datum = data[fixation_num:fixation_num + 1]

        if check_question(datum, participant, que_number, fixation_num):
            write_down(outputs, dic, que_number)
            participant, que_number = fixation_info(datum, fixation_num)
            dic = init_data(participant, datum, fixation_num)
            get_task_result(task_result, que_number, participant, dic)

        recStart = datum['RecordingTimestamp'][fixation_num]
        gazeDur = datum['GazeEventDuration'][fixation_num]
        gazeX = datum['FixationPointX (MCSpx)'][fixation_num]
        gazeY = datum['FixationPointY (MCSpx)'][fixation_num]
        AOI = int(datum['AOI'][fixation_num]) - 1
        tmp = {}
        tmp['recStart'] = int(recStart)
        tmp['gazeDur'] = int(gazeDur)
        try:
            tmp['gazeX'] = int(gazeX)
            tmp['gazeY'] = int(gazeY)
            tmp['AOI'] = AOI
            dic['fixations'].append(tmp)
        except:
            print(participant, que_number)
            print(gazeX)

    sort_by_score(outputs)

    f = open('../data/fixation_detail.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
