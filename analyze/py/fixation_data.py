# -*- coding: utf-8 -*-

import os
import csv
import sys
import json
import copy


def main():
    main_path = '../src/evalGIBresult/'
    ref_path = '../src/Analyze/'
    outpath = '../src/trajectory/'
    outputs = [[[] for que in range(120)] for task in range(4)]
    tasknum = 0
    for person in os.listdir(main_path):
        # if person == 'kawaguchi':
        # print(person)
        if os.path.isdir(main_path + person):
            for task in os.listdir(main_path + person):
                if os.path.isdir(main_path + person + '/' + task): # and task == 'task1':
                    tasknum = int(task[-1]) - 1
                    for num in range(120):
                        # print(person, task, num)
                        f = open(ref_path + person + '/' + task + '/' + str(num) + '.csv', 'r')
                        readerf = csv.reader(f)
                        ref_data = [i for i in readerf]
                        g = open(main_path + person + '/' + task + '/' + person + '_' + task + '_' + str(num) + '.csv', 'r')
                        readerg = csv.reader(g)
                        main_data = [i for i in readerg]
                        index = copy.deepcopy(main_data[0])
                        name_list = ['ParticipantName', 'SegmentStart', 'SegmentEnd', 'SegmentDuration', 'RecordingTimestamp', 'GazeEventDuration', 'FixationPointX (MCSpx)', 'FixationPointY (MCSpx)']
                        id_list = []
                        for name in name_list:
                            for index_num in range(len(index)):
                                if name == index[index_num]:
                                    id_list.append(index_num)
                                    continue
                        del main_data[0]
                        dic = {}
                        segmentStart = 0
                        segmentEnd = 0
                        segmentDur = 0
                        if len(main_data) == 0:
                            print('no data found')
                            print(person, task, num)
                            if person == 'kume':
                                participant = 'kume nonoka'
                            if person == 'ide':
                                participant = 'ide'
                            print(participant)
                            segmentStart = 0
                            segmentEnd = 100
                            segmentDur = 100
                            dic['participant'] = participant
                            dic['segmentStart'] = segmentStart
                            dic['segmentEnd'] = segmentEnd
                            dic['segmentDur'] = segmentDur
                            dic['fixations'] = []
                        else:
                            participant = main_data[0][id_list[0]]
                            segmentStart = main_data[0][id_list[1]]
                            segmentEnd = main_data[0][id_list[2]]
                            segmentDur = main_data[0][id_list[3]]
                            dic['participant'] = participant
                            dic['segmentStart'] = segmentStart
                            dic['segmentEnd'] = segmentEnd
                            dic['segmentDur'] = segmentDur
                            dic['fixations'] = []
                            for step in range(len(main_data)):
                                if int(ref_data[step][1]) != 0:
                                    recStart = main_data[step][id_list[4]]
                                    gazeDur = main_data[step][id_list[5]]
                                    gazeX = main_data[step][id_list[6]]
                                    gazeY = main_data[step][id_list[7]]
                                    AOI = int(ref_data[step][1]) - 1
                                    tmp = {}
                                    tmp['recStart'] = recStart
                                    tmp['gazeDur'] = gazeDur
                                    tmp['gazeX'] = gazeX
                                    tmp['gazeY'] = gazeY
                                    tmp['AOI'] = AOI
                                    dic['fixations'].append(tmp)
                        # print(tasknum, num)
                        outputs[tasknum][num].append(dic)
                        # print(person)
                        # print(dic)
                        # print(outputs)
                        # print(tasknum, num)
                        # sys.exit()
                # print('task ' + str(tasknum) + ' complete.')
                # sys.exit()

    f = open(outpath + 'fixation_detail.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
