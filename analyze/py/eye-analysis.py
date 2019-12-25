import json
import math
from statistics import mean, stdev
from scipy.stats import f_oneway, friedmanchisquare, shapiro, wilcoxon
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mean, stdev


def verify_layout(layout):
    if layout == 'STGIB':
        return 0
    elif layout == 'Chatu':
        return 1
    elif layout == 'FDGIB':
        return 2
    elif layout == 'TRGIB':
        return 3


def main():
    data = json.load(open('../flaski/answers.json'))
    rowdata = json.load(open('../src/trajectory/row_metrics.json'))
    data = [[[] for j in range(4)] for i in range(4)]
    for i in range(len(rowdata)):
        for j in rowdata[i]:
            data[i][verify_layout(j['layout'])].append(j)
    print(len(data[0][1]))

    gazecounts = [[[] for j in range(4)] for i in range(4)]
    for task in range(4):
        for layout in range(4):
            for que in range(30):

                # if task != 0:
                #     gazecounts[task][layout].append(data[task][layout][que]['saccade/fixation'])
                try:
                    gazecounts[task][layout].extend(data[task][layout][que]['distractorsBeforeTarget'])
                    # gazecounts[task][layout].extend(mean(data[task][layout][que]['totalFixation']) - data[task][layout][que]['ansDur'] / 20)
                except:
                    pass
    task = 3
    print(len(gazecounts[task][0]), len(gazecounts[task][1]), len(gazecounts[task][2]), len(gazecounts[task][3]))
    print(friedmanchisquare(gazecounts[task][0], gazecounts[task][1], gazecounts[task][2], gazecounts[task][3]))
    print(mean(gazecounts[task][0]), mean(gazecounts[task][1]), mean(gazecounts[task][2]), mean(gazecounts[task][3]))
    print(stdev(gazecounts[task][0]), stdev(gazecounts[task][1]), stdev(gazecounts[task][2]), stdev(gazecounts[task][3]))
    # print(friedmanchisquare(gazecounts[1][0], gazecounts[1][1], gazecounts[1][2], gazecounts[1][3]))
    # print(friedmanchisquare(gazecounts[2][0], gazecounts[2][1], gazecounts[2][2], gazecounts[2][3]))
    # print(friedmanchisquare(gazecounts[3][0], gazecounts[3][1], gazecounts[3][2], gazecounts[3][3]))
    print(wilcoxon(gazecounts[task][0], gazecounts[task][1]))
    print(wilcoxon(gazecounts[task][0], gazecounts[task][2]))
    print(wilcoxon(gazecounts[task][0], gazecounts[task][3]))
    print(wilcoxon(gazecounts[task][1], gazecounts[task][2]))
    print(wilcoxon(gazecounts[task][1], gazecounts[task][3]))
    print(wilcoxon(gazecounts[task][2], gazecounts[task][3]))


if __name__ == '__main__':
	main()