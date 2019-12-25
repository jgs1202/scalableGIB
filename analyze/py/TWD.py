# -*- coding: utf-8 -*-

import os
import csv
import json


def makefile():
    data = [[[[] for j in range(120)] for i in range(4)] for k in range(20) ]
    origin = './src/Analyze/'
    outpath = './src/trajectory/'
    people = 0

    for who in os.listdir(origin):
        if who != '.DS_Store':
            for task in os.listdir(origin + who):
                if task != '.DS_Store':
                    for file in range(120):
                        f = open(origin + who + '/' + task + '/' + str(file) + '.csv', 'r')
                        reader = csv.reader(f)
                        datum = [i for i in reader]
                        f.close()
                        for i in range(len(datum) - 1):
                            dic = {}
                            dic['source'], dic['target'] = {}, {}
                            dic['source']['AOI'], dic['source']['duration'] = datum[i][1], datum[i][4]
                            dic['source']['x'], dic['source']['y'] = datum[i][2], datum[i][3]
                            dic['target']['AOI'], dic['target']['duration'] = datum[i+1][1], datum[i+1][4]
                            dic['target']['x'], dic['target']['y'] = datum[i+1][2], datum[i+1][3]
                            data[people][int(task[-1]) - 1][file].append(dic)
            people += 1

    out = [[[[] for j in range(120)] for i in range(4)] for k in range(20) ]

    for who in data:
        for task in who:
            for datum in task:
                for traje 
    print(data)


def main():
    makefile()


if __name__ == '__main__':
    main()