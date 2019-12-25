# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import json
import numpy as np
from scipy import stats
from scipy.stats import pearsonr


def mkframe():
    eye = json.load(open('../src/trajectory/measure.json'))
    result = json.load(open('../flaski/statistics.json'))
    xs, ys = [0 for i in range(16)], [0 for i in range(16)]
    for i in range(len(eye)):
        for j in eye[i]:
            if j['layout'] == 'STGIB':
                layout = 0
            if j['layout'] == 'Chaturvedi' or j['layout'] == 'Chatu':
                layout = 1
            if j['layout'] == 'FDGIB':
                layout = 2
            if j['layout'] == 'TRGIB':
                layout = 3
            ys[4 * i + layout] = j['total']

    for i in range(len(result)):
        for j in result[i]:
            if j['layout'] == 'STGIB':
                layout = 0
            if j['layout'] == 'Chaturvedi' or j['layout'] == 'Chatu':
                layout = 1
            if j['layout'] == 'FDGIB':
                layout = 2
            if j['layout'] == 'TRGIB':
                layout = 3
            xs[4 * i + layout] = j['time']
    return [xs, ys]


def main():
    data = mkframe()
    print(data)
    xs, ys = data[0], data[1]
    print(xs)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(xs[0], ys[0], c='#E22C4A', label='task1')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[1], ys[1], c='#353FBC')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[2], ys[2], c='#00A45D')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[3], ys[3], c='#F9CD04')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[4], ys[4], c='#E22C4A', marker='^', label='task2')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[5], ys[5], c='#353FBC', marker='^')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[6], ys[6], c='#00A45D', marker='^')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[7], ys[7], c='#F9CD04', marker='^')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[8], ys[8], c='#E22C4A', marker='s', label='task3')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[9], ys[8], c='#353FBC', marker='s')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[10], ys[10], c='#00A45D', marker='s')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[11], ys[11], c='#F9CD04', marker='s')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[12], ys[12], c='#E22C4A', marker='*', label='task4')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[13], ys[13], c='#353FBC', marker='*')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[14], ys[14], c='#00A45D', marker='*')  #, edgecolor='black', linewidth='1')
    ax.scatter(xs[15], ys[15], c='#F9CD04', marker='*')  #, edgecolor='black', linewidth='1')

    # ax.set_title('The relationshops beteen task completion time and total count of visit')
    ax.set_xlabel('Task completion time')
    ax.set_ylabel('Total count of visits')
    ax.legend()
    fig.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(xs, ys)
    print('y = ' + str(slope) + 'x + ' + str(intercept) + ', r_value = ' + str(r_value))
    print(r_value*r_value, p_value)
    print(pearsonr(xs, ys))

if __name__ == '__main__':
    main()
