# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import json


def read():
    data = json.load(open('../src/trajectory/measure.json', 'r'))
    return data


def main():
    data = read()
    ans = [0, 0, 0, 0]
    ans2 = [0, 0, 0, 0]
    ans3 = [0, 0, 0, 0]
    for datum in data[1]:
        layout = datum['layout']
        if layout == 'STGIB':
            ans[0] = datum['durAnsRatio']
            ans2[0] = datum['durAns2Ratio']
            ans3[0] = datum['durAns3Ratio']
        elif layout == 'TRGIB':
            ans[1] = datum['durAnsRatio']
            ans2[1] = datum['durAns2Ratio']
            ans3[1] = datum['durAns3Ratio']
        elif layout == 'FDGIB':
            ans[2] = datum['durAnsRatio']
            ans2[2] = datum['durAns2Ratio']
            ans3[2] = datum['durAns3Ratio']
        elif layout == 'Chatu':
            ans[3] = datum['durAnsRatio']
            ans2[3] = datum['durAns2Ratio']
            ans3[3] = datum['durAns3Ratio']

    names = ['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB']

    xx = np.arange(len(names)) + 1
    col1 = '#ffa0a0'  # color of dam height
    col2 = '#a0a0ff'  # color of waterway length
    col3 = '#ABFF7F'
    col4 = '#FFEF85'
    fsz = 8
    fig = plt.figure(figsize=(5, 5), facecolor='w', dpi=150)
    plt.rcParams["font.size"] = fsz

    plt.subplot(111)
    plt.xticks(xx, names)
    plt.ylim(0, 0.3)
    plt.xlim(0, len(xx) + 1)
    plt.xlabel('Layouts')
    plt.ylabel('The ratio of gaze duration')
    plt.grid(color='#999999', linestyle='--')

    # plt.barh([0], [0], color=col1, align='center', label='Dam height (m)')
    plt.bar(xx - 0.2, ans, width=0.20, color=col1, align='center', label='answer')
    plt.bar(xx, ans2, width=0.20, color=col2, align='center', label='candidate 1')
    plt.bar(xx + 0.2, ans3, width=0.20, color=col3, align='center', label='candidate 2')

    plt.legend(shadow=True, loc='upper right')
    # plt.titl e('Total duration of the candidates', loc='center', fontsize=fsz + 4)
    plt.show(fig)

    a = input()

if __name__ == '__main__':
    main()