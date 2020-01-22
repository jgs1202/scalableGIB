# -*- coding: utf-8 -*-

import numpy as np
import os
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import copy


def preprocess(data):
    files = [[], []]
    layouts = [[], []]
    answers = [[], []]
    segs = [[], []]
    AOIs = [[], []]
    AOIKinds = [[], []]
    groupSizes = [[], []]

    for que in data:
        for datum in que:
            layout = datum['layout']
            answer = datum['answer']
            file = datum['file']
            if layout == "FDGIB":
                for seg in range(len(datum['segments'])):
                    seg_data = datum['segments'][seg]
                    files[0].append(file)
                    layouts[0].append(layout)
                    groupSizes[0].append(datum['groupSize'])
                    answers[0].append(answer)
                    segs[0].append(seg)
                    AOIs[0].append(len(seg_data['AOIs']))
                    AOIKinds[0].append(len(seg_data['AOIKinds']))
            elif layout == "TRGIB":
                for seg in range(len(datum['segments'])):
                    seg_data = datum['segments'][seg]
                    files[1].append(file)
                    layouts[1].append(layout)
                    groupSizes[1].append(datum['groupSize'])
                    answers[1].append(answer)
                    segs[1].append(seg)
                    AOIs[1].append(len(seg_data['AOIs']))
                    AOIKinds[1].append(len(seg_data['AOIKinds']))

    # AOIs = [np.array(AOIs[0]), np.array(AOIs[1])]
    # AOIs[0] = AOIs[0] / AOIs[0].max()
    # AOIs[1] = AOIs[1] / AOIs[1].max()
    # AOIKinds = [np.array(AOIKinds[0]), np.array(AOIKinds[1])]
    # AOIKinds[0] = AOIKinds[0] / AOIKinds[0].max()
    # AOIKinds[1] = AOIKinds[1] / AOIKinds[1].max()

    df_fd = pd.DataFrame({"file": files[0],
                        "answer": answers[0],
                        "layout": layouts[0],
                        "groupSize": groupSizes[0],
                        "segment": segs[0],
                        "AOIs": AOIs[0],
                        "AOIKinds": AOIKinds[0]})
    df_tr = pd.DataFrame({"file": files[1],
                        "answer": answers[1],
                        "layout": layouts[1],
                        "groupSize": groupSizes[1],
                        "segment": segs[1],
                        "AOIs": AOIs[1],
                        "AOIKinds": AOIKinds[1]})

    return df_fd, df_tr


def make_data():
    data = json.load(open('../data/fixation_detail.json', 'r'))
    total_que = 120
    total_step = 15
    outputs = [[] for que in range(total_que)]

    for que in range(total_que):
        src_data = json.load(open('../../src/data/random/' + str(que) + '.json', 'r'))

        for datum in data[que]:
            dic = copy.deepcopy(datum)
            dic['segments'] = [{"AOIs": [], "AOIKinds": []} for i in range(total_step)]
            segStart = int(datum['segmentStart'])
            segEnd = int(datum['segmentEnd'])
            duration = segEnd - segStart

            for fixation in datum['fixations']:
                recStart = float(fixation['recStart'])
                recEnd = recStart + float(fixation['gazeDur'])
                startUnit = int((recStart - segStart) / duration * total_step)
                endUnit = int((recEnd - segStart) / duration * total_step) + 1
                if endUnit > total_step:
                    endUnit = total_step
                for step in range(startUnit, endUnit):
                    AOI = fixation['AOI']
                    dic['segments'][step]['AOIs'].append(AOI)
                    if AOI not in dic['segments'][step]['AOIKinds']:
                        dic['segments'][step]['AOIKinds'].append(AOI)
            del dic['fixations']
            dic['layout'] = src_data['layout']
            dic['groupSize'] = src_data['groupSize']
            outputs[que].append(dic)
    return outputs


def vis(df):
    aois = df['AOIs'].max()
    kinds = df['AOIKinds'].max()
    AOI_index = [i % aois for i in range(aois * kinds)]
    kind_index = [int(i / aois) for i in range(aois * kinds)]
    numbers = [len(df[(df['AOIs'] == (i % aois)) & (df['AOIKinds'] == int(i / aois))]) for i in range(aois * kinds)]
    _df = pd.DataFrame({"AOIKinds": kind_index, "numberOfAOI": AOI_index, "value": numbers})
    _df = _df.pivot('AOIKinds', 'numberOfAOI', 'value')
    heatmap = sns.heatmap(_df, cmap='hot_r')
    # plt.savefig('../data/AOI-kind-fd.png')

    aois = df['AOIs'].max()
    segs = df['segment'].max()
    AOI_index = [i % aois for i in range(aois * segs)]
    segment_index = [int(i / aois) for i in range(aois * segs)]
    numbers = [len(df[(df['AOIs'] == (i % aois)) & (df['segment'] == int(i / aois))]) for i in range(aois * segs)]
    _df = pd.DataFrame({"segment": segment_index, "numberOfAOI": AOI_index, "value": numbers})
    _df = _df.pivot('segment', 'numberOfAOI', 'value')
    heatmap = sns.heatmap(_df, cmap='hot_r')
    # plt.savefig('../data/time-AOI-fd.png')

    aois = df['AOIKinds'].max()
    segs = df['segment'].max()
    AOI_index = [i % aois for i in range(aois * segs)]
    segment_index = [int(i / aois) for i in range(aois * segs)]
    numbers = [len(df[(df['AOIKinds'] == (i % aois)) & (df['segment'] == int(i / aois))]) for i in range(aois * segs)]
    _df = pd.DataFrame({"segment": segment_index, "numberOfAOI": AOI_index, "value": numbers})
    _df = _df.pivot('segment', 'numberOfAOI', 'value')
    heatmap = sns.heatmap(_df, cmap='hot_r')
    # plt.savefig('../data/time-Kind-fd.png')


def verify_level(group):
    if group == 10:
        return 0
    elif group == 40:
        return 1


def verify_tax1(segment, AOI):
    if AOI == 0:
        return 0
    elif AOI > 0 and AOI < 6 and segment < 7:
        return 1
    elif AOI > 5 and segment < 7:
        return 2
    elif AOI > 0 and AOI < 6 and segment > 6:
        return 3
    elif AOI > 5 and segment > 6:
        return 4


def verify_tax2(kind):
    if kind == 0:
        return 0
    elif kind < 3:
        return 1
    else:
        return 2


def verify_tax3(AOI, kind):
    if AOI == 0:
        return 0
    elif AOI < 6 and kind < 3:
        return 1
    elif AOI > 5 and kind < 3:
        return 2
    elif kind > 2:
        return 3


def taxonomy_comp(tax1, tax2, tax3):
    if tax1 == 0:
        return 0
    elif tax1 == 1 and tax2 == 1:
        return 1
    elif tax1 == 1 and tax2 == 2:
        return 2
    elif tax1 == 2 and tax2 == 1:
        return 3
    elif tax1 == 2 and tax2 == 2:
        return 4
    elif tax1 == 3 and tax2 == 1:
        return 5
    elif tax1 == 3 and tax2 == 2:
        return 6
    elif tax1 == 4 and tax2 == 1:
        return 7
    elif tax1 == 4 and tax2 == 2:
        return 8


def compare(tr, fd):
    _level = 2
    _answer = 2
    _tax1 = 5
    _tax2 = 3
    _tax3 = 4

    ans_fd0 = 534
    ans_tr0 = 586
    ans_fd1 = 473
    ans_tr1 = 600
    num_answers = [[ans_fd0, ans_fd1], [ans_tr0, ans_tr1]]

    result = [[[[0 for l in range(9)] for k in range(_answer)] for j in range(2)] for i in range(_level)]

    for level in range(_level):
        for answer in range(_answer):
            for tax1 in range(_tax1):
                for tax2 in range(_tax2):
                    for tax3 in range(_tax3):
                        if tr[level][answer][tax1][tax2][tax3] != 0 or fd[level][answer][tax1][tax2][tax3] != 0:
                            taxonomy = taxonomy_comp(tax1, tax2, tax3)
                            result[level][0][answer][taxonomy] = fd[level][answer][tax1][tax2][tax3] / abs(num_answers[0][level] - 14 * 60 * (1 - answer))
                            result[level][1][answer][taxonomy] = tr[level][answer][tax1][tax2][tax3] / abs(num_answers[1][level] - 14 * 60 * (1 - answer))

    for level in range(2):
        for answer in range(2):
            sns.set()
            # sns.set_style("whitegrid", {'grid.linestyle': '--'})
            # sns.set_context("paper", 1.5, {"lines.linewidth": 4})
            # sns.set_palette("winter_r", 8, 1)
            # sns.set('talk', 'whitegrid', 'dark', font_scale=1.5,
            #         rc={"lines.linewidth": 2, 'grid.linestyle': '--'})

            x = np.arange(9)
            y1 = [result[level][0][answer][tax] for tax in range(9)]
            y2 = [result[level][1][answer][tax] for tax in range(9)]

            plt.figure()
            plt.plot(x, y1, label='FD-GIB')
            plt.plot(x, y2, label='TR-GIB')
            plt.legend(loc='upper left')
            plt.savefig('../data/segment-taxonomy-level' + str(level) + '-ans-' + str(answer) + '.png')


def classify(df):
    # 1試行をセグメント分けし、各セグメントがどの分類に入るか検証
    # その試行をレイアウト、レベル、解答の成否に分けさらに分類する
    _level = 2
    _answer = 2
    _tax1 = 5
    _tax2 = 3
    _tax3 = 4
    result = [[[[[0 for i5 in range(_tax3)] for i4 in range(_tax2)] for i3 in range(_tax1)] for i2 in range(_answer)] for i1 in range(_level)]

    for segment in range(len(df)):
        level = verify_level(df['groupSize'][segment])
        answer = int(df['answer'][segment])
        tax1 = verify_tax1(df['segment'][segment], df['AOIs'][segment])
        tax2 = verify_tax2(df['AOIKinds'][segment])
        tax3 = verify_tax3(df['AOIs'][segment], df['AOIKinds'][segment])
        result[level][answer][tax1][tax2][tax3] += 1
    return result


def main():
    data = make_data()
    df_fd, df_tr = preprocess(data)
    # vis(df_fd)
    fd_result = classify(df_fd)
    tr_result = classify(df_tr)
    compare(fd_result, tr_result)



if __name__ == '__main__':
    main()
