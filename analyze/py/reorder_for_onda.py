# -*- coding: utf-8 -*-

import numpy as np
import os
import csv
import sys


def main():
    participants = ['onda', 'yoshida']
    ref_path = '../src/Analyze/'
    main_path = '../src/evalGIBresult/'
    file_list = [i for i in range(120)]

    for person in participants:
        for task in os.listdir(ref_path + person):
            corrects = []
            if os.path.isdir(ref_path + person):
                for num in range(120):
                    count = 0
                    f = open(ref_path + person + '/' + task + '/' + str(num) + '.csv', 'r')
                    readerf = csv.reader(f)
                    ref_data = [i for i in readerf]

                    for file_num in range(len(file_list)):
                        g = open(main_path + person + '/' + task + '/' + person + '_' + task + '_' + str(file_num) + '.csv', 'r')
                        readerg = csv.reader(g)
                        main_data = [i for i in readerg]
                        if len(ref_data) == len(main_data) - 1:
                            for i in range(1, len(main_data)):
                                if ref_data[i-1][4] != main_data[i][15]:
                                    break
                                if len(ref_data) == i:
                                    count += 1
                                    if count > 1:
                                        print('error')
                                    corrects.append(file_num)
                                    try:
                                        os.mkdir(main_path + person + '_new')
                                    except:
                                        pass
                                    try:
                                        os.mkdir(main_path + person + '_new' + '/' + task)
                                    except:
                                        pass
                                    h = open(main_path + person + '_new' + '/' + task + '/' + person + '_' + task + '_' + str(num) + '.csv', 'w')
                                    writer = csv.writer(h, lineterminator='\n')
                                    for row in main_data:
                                        writer.writerow(row)
                                    h.close()

if __name__ == '__main__':
    main()
