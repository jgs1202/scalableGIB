# -*- coding: utf-8 -*-

from pandas.tools.plotting import parallel_coordinates
import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import json
import sys
import copy


def read():
    dataTime = json.load(open('../src/trajectory/correlation_meanTime.json'))
    dataAccuracy = json.load(open('../src/trajectory/correlation_corrects.json'))
    return dataTime, dataAccuracy


def extract(data, use):
    keys = ['devTime', 'totalFixation', 'ans2Count', 'ans2Dur', 'ans3Count', 'totalLength', 'ans3Dur', 'meanAngle']
    keys.append(use)
    print(keys)
    for i in range(len(data)):
        delList = []
        for j in range(len(data[i])):
                if data[i][j][1] in keys:
                    delList.append(j)
        for j in range(len(delList)):
            del data[i][delList[len(delList) - 1 - j]]
    return data


def mkframe(data):
    keylist = []
    for i in data[1]:
        keylist.append(i[1])
    print(keylist)
    df = [[] for i in range(len(keylist))]
    names = ['measure', 'task2_correlation', 'task3_correlation', 'task4_correlation']
    for task in range(len(data)):
        for key in range(len(keylist)):
            if task == 0:
                # df[key].append(keylist[key])
                df[key].append(key)
            var = 0
            if task != 0:
                    for datum in data[task]:
                        if datum[1] == keylist[key]:
                            df[key].append(datum[2])
                            var = 1
                    if var == 0:
                        df[key].append(None)
    df = pd.DataFrame(df, columns=names)
    df.head()
    return df


def main():
    dataTime, dataAccuracy = read()
    dataTime = extract(dataTime, 'meanTime')
    dataAccuracy = extract(dataAccuracy, 'corrects')
    df = mkframe(dataAccuracy)
    col = []
    length = 18
    cm = plt.get_cmap('gist_rainbow')
    for i in range(length):
        col.append(cm(1. * i / length)[:-1])
    color = []
    for i in col:
        hexes = []
        for j in i:
            tmp = format(int(str(int(round(j*255))), 10), 'x')
            if len(tmp) != 2:
                tmp = '0' + tmp
            hexes.append(copy.deepcopy(tmp))
        hex = '#' + hexes[0]
        hex += hexes[1]
        hex += hexes[2]
        color.append([1.0, hex])
    print((color))
    print(df)
    data = [
        go.Parcoords(
            line=dict(color=df['measure'],
                colorscale=color
            ),
            dimensions=list([
                dict(range=[-1, 1],
                    # name=df['The number of groups'],
                    label='Task 2', values=df['task2_correlation']),
                dict(range=[-1, 1],
                    # name=df['The number of groups'],
                    label='Task 3', values=df['task3_correlation']),
                dict(range=[-1, 1],
                    # name=df['The number of groups'],
                    label='Task 4', values=df['task4_correlation'])
            ])
        )
    ]

    layout = go.Layout(
        showlegend=True
        # plot_bgcolor='#E5E5E5',
        # paper_bgcolor='#E5E5E5'
    )
    # plt.figure()
    # parallel_coordinates(data, 'The number of groups')
    # plt.show()

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)


if __name__ == '__main__':
    main()
