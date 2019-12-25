# -*- coding: utf-8 -*-

import os
import csv
import json
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np


def execute():
    data = json.load(open('../src/trajectory/metrics.json'))
    output = [[] for i in range(4)]

    for task in range(4):
        figure = plt.figure()
        tmpData = data[task]
        # if task == 0:
        index = 'corrects'
        tmpData.sort(key=itemgetter(index))
        keys = tmpData[0].keys()
        keylist = [i for i in keys]
        for i in range(len(keylist)):
            if keylist[i] == 'layout':
                del keylist[i]
                break
        pltData = [[] for i in range(len(keylist))]
        xx = np.arange(120)
        old = 0
        for i in range(len(keylist)):
            name = keylist[i]
            # print(keylist)
            for datum in tmpData:
                try:
                    pltData[i].append(float(datum[name]))
                    old = float(datum[name])
                except:
                    pltData[i].append(old)
            tmpMax = max(pltData[i])
            tmpMin = min(pltData[i])
            for j in range(len(pltData[i])):
                pltData[i][j] -= tmpMin
                pltData[i][j] /= (tmpMax - tmpMin)
            if name == 'inrelavantCount' or name == 'inrelavantDur' or name == 'relavantCount' or name == 'relavantDur':
                plt.plot(xx, pltData[i], label=name)
                plt.legend()
        plt.show()
        pltData = np.asarray(pltData)
        num = 0
        for i in range(len(keylist)):
            if keylist[i] == index:
                num = i
        coef = np.corrcoef(pltData)[num]
        for i in range(len(coef)):
            # if abs(coef[i]) > 0.3:
            if keylist[i] == 'ansCount': # 'inrelavantCount' or keylist[i] == 'inrelavantDur' or keylist[i] == 'relavantCount' or keylist[i] == 'relavantDur':
                print(task, keylist[i], coef[i])
            output[task].append([task + 1, keylist[i], coef[i]])

        f = open('../src/trajectory/correlation_' + index + '.json', 'w')
        json.dump(output, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def main():
    execute()


if __name__ == '__main__':
    main()