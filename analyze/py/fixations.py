# -*- coding: utf-8 -*-

import os
import csv
import json


def makefile():
    data = [[[] for j in range(120)] for i in range(4)]
    origin = '../src/eyeGIBresult/'
    outpath = '../src/trajectory/'

    for who in os.listdir(origin):
        if who != '.DS_Store':
            for task in os.listdir(origin + who):
                if task != '.DS_Store':
                    for file in range(120):
                        list = []
                        f = open(origin + who + '/' + task + '/' + str(file) + '.csv', 'r')
                        reader = csv.reader(f)
                        datum = [i for i in reader]
                        f.close()
                        for i in range(len(datum)):
                            dic = {}
                            dic['AOI'], dic['duration'] = datum[i][1], datum[i][4]
                            dic['x'], dic['y'] = datum[i][2], datum[i][3]

                            list.append(dic)
                        data[int(task[-1]) - 1][file].append(list)
    # print(len(data[0]), len(data[0][0]), len(data[1][0][1]))
    f = open(outpath + 'gazeData.json', 'w')
    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def main():
    makefile()


if __name__ == '__main__':
    main()