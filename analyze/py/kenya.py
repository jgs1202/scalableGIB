# -*- coding: utf-8 -*-

import math
import os
import csv
import json
from statistics import mean
import numpy as np


def calcEachQue(data, totalData, queInfo):
    out = [[[] for j in range(120)] for i in range(4)]
    for task in range(len(out)):
        for que in range(len(out[task])):
            answer = json.load(open(srcpath + 'task' + str(int(task) + 1) + '/' + str(que) + '.json'))
            if task == 1:
                if que < 60:
                    ans = answer['nodeMax']
                    ans2 = answer['node2ndMax']
                    ans3 = answer['node3rdMax']
                else:
                    ans = answer['nodeMin']
                    ans2 = answer['node2ndMin']
                    ans3 = answer['node3rdMin']
            if task == 2:
                if que < 60:
                    ans = answer['linkMax']
                    ans2 = answer['link2ndMax']
                    ans3 = answer['link3rdMax']
                else:
                    ans = answer['linkMin']
                    ans2 = answer['link2ndMin']
                    ans3 = answer['link3rdMin']
            if task == 3:
                ans = answer['linkOutMost'][0]
                ans2 = answer['linkOut2nd']
                ans3 = answer['linkOut3rd']
            # from here I must calculate each variable at a person respectively
            dic = {}
            eyePeople = len(data[task][que])
            quePeople = int(queInfo[task][que]['people'])
            dic['layout'] = answer['type']
            dic['meanGazeCount'] = len(totalData[int(task)][que]) / eyePeople
            dic['totalLength'] = 0.
            dic['meanAngle'] = []
            for i in range(len(totalData[task][que])):
                if i != len(totalData[task][que]) - 1:
                    dx = float(totalData[task][que][i]['x']) - float(totalData[task][que][i+1]['x'])
                    dy = float(totalData[task][que][i]['y']) - float(totalData[task][que][i+1]['y'])
                    dic['totalLength'] += math.sqrt(dx * dx + dy * dy)
            for member in data[task][que]:
                angles = []
                for i in range(len(member)):
                    if i < len(member) - 2:
                        x0, y0 = int(member[i]['x']), int(member[i]['y'])
                        x1, y1 = int(member[i+1]['x']), int(member[i+1]['y'])
                        x2, y2 = int(member[i+2]['x']), int(member[i+2]['y'])
                        d0 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                        d1 = math.sqrt((x2 - x0) ** 2 + (y2 - y0) ** 2)
                        d2 = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
                        # print(d0, d2)
                        try:
                            cos = (d0 ** 2 + d2 ** 2 - d1 ** 2) / (2 * d0 * d2)
                            angles.append(np.arccos(cos))
                        except:
                            pass
                if len(angles) != 0:
                    dic['meanAngle'].append(mean(angles))
            if dic['meanAngle'][0] is not None:
                dic['meanAngle'] = mean(dic['meanAngle'])
            else:
                dic['meanAngle'] = None
            if task == 0:
                totalDur = 0
                for i in range(len(totalData[task][que])):
                    totalDur += int(totalData[task][que][i]['duration'])
                dic['totalFixation'] = totalDur
            if task != 0:
                totalDur, ansDur, ansCount = 0, 0, 0
                ans2Dur, ans3Dur, ans2Count, ans3Count = 0., 0., 0, 0
                for i in range(len(totalData[task][que])):
                    totalDur += float(totalData[task][que][i]['duration'])
                    if ans == int(totalData[task][que][i]['AOI']) - 1:
                        ansDur += float(totalData[task][que][i]['duration'])
                        ansCount += 1
                    if ans2 == int(totalData[task][que][i]['AOI']) - 1:
                        ans2Dur += float(totalData[task][que][i]['duration'])
                        ans2Count += 1
                    if ans3 == int(totalData[task][que][i]['AOI']) - 1:
                        ans3Dur += float(totalData[task][que][i]['duration'])
                        ans3Count += 1
                    elif type(ans) == list:
                        # for an in ans:
                        if ans[0] == int(totalData[task][que][i]['AOI']) - 1:
                            ansDur += float(totalData[task][que][i]['duration'])
                            ansCount += 1
                dic['ansDur'] = ansDur
                dic['totalFixation'] = totalDur
                dic['ansCount'] = ansCount
                dic['ans2Dur'] = ans2Dur
                dic['ans3Dur'] = ans3Dur
                dic['ans2Count'] = ans2Count
                dic['ans3Count'] = ans3Count
                dic['relavantDur'] = ansDur + ans2Dur + ans3Dur
                dic['relavantCount'] = (ansCount + ans2Count + ans3Count)
                dic['inrelavantDur'] = (totalDur - dic['relavantDur']) / eyePeople
                dic['inrelavantCount'] = (len(totalData[int(task)][que]) - dic['relavantCount'])
            dic['firstFixation'] = []
            if task != 0:
                dic['distractorsBeforeTarget'] = []
                dic['durOfDistractorsBeforeTarget'] = []
                dic['distractorsAfterTarget'] = []
                dic['durOfDistractorsAfterTarget'] = []
                dic['durOfFirstTarget'] = []
            for member in range(len(data[task][que])):
                dic['firstFixation'].append(int(data[task][que][member][0]['duration']))
                if task != 0:
                    tmpCount = 0
                    tmpDur = []
                    for fix in range(len(data[task][que][member])):
                        if int(data[task][que][member][fix]['AOI']) - 1 != ans and fix != len(data[task][que][member])-1:
                            tmpCount += 1
                            tmpDur.append(int(data[task][que][member][fix]['duration']))
                        elif int(data[task][que][member][fix]['AOI']) - 1 != ans and fix == len(data[task][que][member])-1:
                            tmpCount += 1
                            tmpDur.append(int(data[task][que][member][fix]['duration']))
                            dic['distractorsBeforeTarget'].append(tmpCount)
                            dic['durOfDistractorsBeforeTarget'].append(mean(tmpDur))
                            break
                        elif int(data[task][que][member][fix]['AOI']) - 1 == ans and fix == 0:
                            # tmpDur.append(0)
                            dic['distractorsBeforeTarget'].append(tmpCount)
                            dic['durOfFirstTarget'].append(int(data[task][que][member][fix]['duration']))
                            try:
                                dic['durOfDistractorsBeforeTarget'].append(mean(tmpDur))
                            except:
                                pass
                            break
                        else:
                            dic['distractorsBeforeTarget'].append(tmpCount)
                            dic['durOfDistractorsBeforeTarget'].append(mean(tmpDur))
                            dic['durOfFirstTarget'].append(int(data[task][que][member][fix]['duration']))
                            break
            for member in range(len(data[task][que])):
                if task != 0:
                    tmpCount = 0
                    tmpDur = []
                    after = 0
                    for fix in range(len(data[task][que][member])):
                        if after == 1 and int(data[task][que][member][fix]['AOI']) - 1 != ans and fix != len(data[task][que][member])-1:
                            tmpCount += 1
                            tmpDur.append(int(data[task][que][member][fix]['duration']))
                        elif after == 1 and int(data[task][que][member][fix]['AOI']) - 1 != ans and fix == len(data[task][que][member])-1:
                            tmpCount += 1
                            tmpDur.append(int(data[task][que][member][fix]['duration']))
                            dic['distractorsAfterTarget'].append(tmpCount)
                            dic['durOfDistractorsAfterTarget'].append(mean(tmpDur))
                        elif after == 1 and int(data[task][que][member][fix]['AOI']) - 1 == ans and fix == len(data[task][que][member])-1 and len(tmpDur) != 0:
                            dic['distractorsAfterTarget'].append(tmpCount)
                            dic['durOfDistractorsAfterTarget'].append(mean(tmpDur))
                        elif after == 1 and int(data[task][que][member][fix]['AOI']) - 1 == ans and fix == len(data[task][que][member])-1 and len(tmpDur) == 0:
                            # tmpDur.append(0)
                            dic['distractorsAfterTarget'].append(tmpCount)
                            try:
                                dic['durOfDistractorsAfterTarget'].append(mean(tmpDur))
                            except:
                                pass
                        elif after == 0 and fix == len(data[task][que][member])-1:
                            # tmpDur.append(0)
                            dic['distractorsAfterTarget'].append(tmpCount)
                            try:
                                dic['durOfDistractorsAfterTarget'].append(mean(tmpDur))
                            except:
                                pass
                        if int(data[task][que][member][fix]['AOI']) - 1 == ans:
                            after = 1
            if task != 0:
                dic['distractorsBeforeTarget'] = mean(dic['distractorsBeforeTarget'])
                dic['durOfDistractorsBeforeTarget'] = mean(dic['durOfDistractorsBeforeTarget'])
                dic['distractorsAfterTarget'] = mean(dic['distractorsAfterTarget'])
                dic['durOfDistractorsAfterTarget'] = mean(dic['durOfDistractorsAfterTarget'])
                dic['durOfFirstTarget'] = mean(dic['durOfFirstTarget'])
            dic['firstFixation'] = mean(dic['firstFixation'])
            dic['meanFixation'] = dic['totalFixation'] / len(totalData[task][que])
            dic['corrects'] = queInfo[task][que]['correct']
            dic['meanLength'] = dic['totalLength'] / eyePeople
            dic['meanTime'] = queInfo[task][que]['meanTime']
            dic['devTime'] = queInfo[task][que]['devTime']
            dic['saccadeDur'] = dic['meanTime'] - dic['meanFixation'] * dic['meanGazeCount']
            dic['saccade/fixation'] = dic['meanFixation'] / dic['saccadeDur']
            if dic['saccadeDur'] < 0:
                dic['saccadeDur'], dic['saccade/fixation'] = None, None
            out[task][que] = dic
    return out


def calcMetric(out):
    output = [[[] for j in range(120)] for i in range(4)]
    for task in range(4):
        for datum in range(len(out[task])):
            output[task][datum]['layout'] = out[task][datum]['layout']
            try:
                output[task][layout]['total']
            except:
                output[task][layout]['total'] = 0
                output[task][layout]['length'] = 0
                output[task][layout]['layout'] = datum['layout']
                if task != 0:
                    output[task][layout]['ansDur'] = 0.
                    output[task][layout]['totalDur'] = 0.
                    output[task][layout]['ansCount'] = 0.
                    output[task][layout]['ans2Dur'] = 0.
                    output[task][layout]['ans2Count'] = 0.
                    output[task][layout]['ans3Dur'] = 0.
                    output[task][layout]['ans3Count'] = 0.
            output[task][layout]['total'] += datum['total']
            output[task][layout]['length'] += datum['length']
            if task != 0:
                output[task][layout]['ansDur'] += datum['ansDur']
                output[task][layout]['totalDur'] += datum['totalDur']
                output[task][layout]['ansCount'] += datum['ansCount']
                output[task][layout]['ans2Dur'] += datum['ans2Dur']
                output[task][layout]['ans2Count'] += datum['ans2Count']
                output[task][layout]['ans3Dur'] += datum['ans3Dur']
                output[task][layout]['ans3Count'] += datum['ans3Count']
    for i in range(4):
        for j in range(4):
            output[i][j]['length'] = output[i][j]['length'] / 120 / 20
            if i != 0:
                output[i][j]['durAnsRatio'] = output[i][j]['ansDur'] / output[i][j]['totalDur']
                output[i][j]['ansCountRatio'] = output[i][j]['ansCount'] / output[i][j]['total']
                output[i][j]['durAns2Ratio'] = output[i][j]['ans2Dur'] / output[i][j]['totalDur']
                output[i][j]['ans2CountRatio'] = output[i][j]['ans2Count'] / output[i][j]['total']
                output[i][j]['durAns3Ratio'] = output[i][j]['ans3Dur'] / output[i][j]['totalDur']
                output[i][j]['ans3CountRatio'] = output[i][j]['ans3Count'] / output[i][j]['total']
    return output


def makefile():
    totalData = [[[] for j in range(120)] for i in range(4)]
    queInfo = json.load(open('../src/trajectory/perQuestion.json'))
    global origin, outpath, srcpath
    origin = '../src/Analyze/'
    outpath = '../src/trajectory/'
    srcpath = '../src/data/'

    # for who in os.listdir(origin):
    #     if who != '.DS_Store':
    #         for task in os.listdir(origin + who):
    #             if task != '.DS_Store':
    #                 for file in range(120):
    #                     f = open(origin + who + '/' + task + '/' + str(file) + '.csv', 'r')
    #                     reader = csv.reader(f)
    #                     datum = [i for i in reader]
    #                     f.close()
    #                     for i in range(len(datum) - 1):
    #                         dic = {}
    #                         if type(datum[i][1]) == 'list':
    #                             datum[i][1] = datum[i][1][0]
    #                         dic['AOI'], dic['duration'] = datum[i][1], datum[i][4]
    #                         dic['x'], dic['y'] = datum[i][2], datum[i][3]
    #                         data[int(task[-1]) - 1][file].append(dic)
    data = json.load(open('../src/trajectory/fixations.json'))
    for task in range(4):
        for que in range(120):
            for i in range(len(data[task][que])):
                for j in data[task][que][i]:
                    totalData[task][que].append(j)
    # print(data)
    out = calcEachQue(data, totalData, queInfo)
    # output = calcMetric(out)
    # print(output)
    f = open(outpath + 'metrics.json', 'w')
    json.dump(out, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def main():
    makefile()


if __name__ == '__main__':
    main()