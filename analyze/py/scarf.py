# -*- coding: utf-8 -*-

import numpy as np
import os
import csv
import sys
import json
import matplotlib.pyplot as plt
from operator import itemgetter


def attach(result):
    data = json.load((open('../flaski/choice.json', 'r')))
    total = 0
    for datum in data:
        person = datum['username']
        task = datum['task']
        que = datum['file'][:-5]
        if person == 'onda+naoto':
            person = 'onda'
        elif person == 'seto+akane':
            person = 'seto'
        elif person == "kawaguchi+shigenobu":
            person = 'kawaguchi'
        elif person == "Wakiko+Ueda":
            person = 'ueda'
        elif person == "kume+nonoka":
            person = 'kume nonoka'
        elif person == "Hara+Momoka":
            person = 'hara'
        elif person == "Toshiki+Watanabe":
            person = 'Toshiki Watanabe'
        elif person == "Sato+Rika":
            person = 'sato'
        elif person == "tomonaga+yota":
            person = 'tomonaga'
        elif person == "ide+wataru":
            person = 'ide'
        elif person == "Kento+Inoue":
            person = 'Kento Inoue'
        elif person == "yoshihara+ikumi":
            person = 'yoshihara ikumi'
        elif person == "fujiwara+takuto":
            person = 'fujiwara takuto'
        elif person == "takada+haruka":
            person = 'takada haruka'
        elif person == "Hiei+Fukuda":
            person = 'Hiei Fukuda'
        elif person == "takasugi+risei":
            person = 'takasugi'

        for i in range(len(result[int(task) - 1][int(que)])):
            if person == result[int(task) - 1][int(que)][i]['participant']:
                if int(datum['answer']) == 1:
                    result[int(task) - 1][int(que)][i]['answer'] = 0
                else:
                    result[int(task) - 1][int(que)][i]['answer'] = 1
                result[int(task) - 1][int(que)][i]['time'] = datum['time']
                total += 1
                break
            # if i == len(result[int(task) - 1][int(que)]) - 1:
            #     print(task, que, person)
    print(total)
    return result


def main():
    data = json.load(open('../src/trajectory/fixation_detail.json', 'r'))
    plot_data = [[[{"data":[]} for person in range(len(data[task][que]))] for que in range(120)] for task in range(4)]
    for task in range(len(data)):
        for que in range(len(data[task])):
            for person in range(len(data[task][que])):
                plot_data[task][que][person]['participant'] = data[task][que][person]['participant']
                duration = float(data[task][que][person]['segmentDur'])
                start = float(data[task][que][person]['segmentStart'])
                if duration != 0.:
                    for fixation in data[task][que][person]['fixations']:
                        dic = {}
                        dic['length'] = float(fixation['gazeDur']) / duration
                        dic['start'] = (float(fixation['recStart']) - start) / duration
                        dic['AOI'] = fixation['AOI']
                        plot_data[task][que][person]['data'].append(dic)

    plot_data = attach(plot_data)

    for task in range(4):
        for que in range(120):
            for person in range(len(plot_data[task][que])):
                if plot_data[task][que][person]['participant'] == 'toyama':
                    del plot_data[task][que][person]
                    break

    for task in range(4):
        for que in range(120):
            plot_data[task][que] = sorted(plot_data[task][que], key=itemgetter('answer'))
            turning = 0
            for people in range(len(plot_data[task][que])):
                if int(plot_data[task][que][people]['answer']) == 1:
                    turning = people
                    break
                elif people == len(plot_data[task][que]) - 1:
                    turning = people
            # print(plot_data[task][que][:turning])
            plot_data[task][que][:turning] = sorted(plot_data[task][que][:turning], key=itemgetter('time'))
            plot_data[task][que][turning:] = sorted(plot_data[task][que][turning:], key=itemgetter('time'))

    outpath = '../src/trajectory/'
    f = open(outpath + 'scarfData.json', 'w')
    json.dump(plot_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))           


if __name__ == '__main__':
    main()
