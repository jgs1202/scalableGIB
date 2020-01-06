import json
import math
from statistics import mean, stdev
from scipy.stats import f_oneway, friedmanchisquare, shapiro, wilcoxon
import matplotlib.pyplot as plt
import seaborn as sns

layouts_number = 2
levels_number = 2


def layout_num(layout):
    if layout == 'FDGIB':
        return 0
    elif layout == 'TRGIB':
        return 1


def level_num(groupSize):
    groupSize = int(groupSize)
    if groupSize == 10:
        return 0
    elif groupSize == 40:
        return 1


def get_stalist(data):
    means = [[[] for j in range(levels_number)] for i in range(layouts_number)]
    correct_times = [[[] for j in range(levels_number)] for i in range(layouts_number)]
    times = [[[] for j in range(levels_number)] for i in range(layouts_number)]
    for layout in range(layouts_number):
        for level in range(levels_number):
            for datum in data[layout][level]:
                means[layout][level].append(datum['correct'] / datum['people'] * 100)
                times[layout][level].append(datum['totalMeanTime'])
                correct_times[layout][level].append(datum['meanCorrectTime'])
    return means, times, correct_times


def box_graph(means, times, data):
    mean = []
    time = []
    for i in range(layout_number):
        mean.append((means[i][0], means[i][1]))
        time.append((times[i][0], times[i][1]))
    for i in range(layout_number):
        sns.set()
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        sns.set_context("paper", 1.5, {"lines.linewidth": layout_number})
        sns.set_palette("winter_r", 8)
        sns.set('talk', 'whitegrid', 'dark', rc={"lines.linewidth": 2, 'grid.linestyle': '--'})
        fig, ax = plt.subplots()
        bp = ax.boxplot(mean[i], vert=True, patch_artist=True)
        # bp = ax.boxplot(time[i], vert=True, patch_artist=True)
        for box in bp['boxes']:
            box.set(color="black", linewidth=1.5)
        for box in bp['medians']:
            plt.setp(box, color="black", linewidth=1.5)
        for box in bp['caps']:
            plt.setp(box, color="black", linewidth=1.5)
        for box in bp['whiskers']:
            plt.setp(box, ls="solid", color="black", linewidth=1.5)
        for box, color in zip(bp["boxes"], sns.color_palette("Set3", 6)):
            box.set_facecolor(color)
        fig.subplots_adjust(top=0.95, bottom=0.15, left=0.10, right=0.97)
        ax.set_xticklabels(['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB'], fontsize=24)
        plt.tick_params(labelsize=22)
        plt.xlabel('layout', fontsize=28)
        # plt.ylabel('accuracy [%]', fontsize=28)
        # plt.ylabel('completion time [ms]', fontsize=28)
        # plt.ylim(1000, 10000)
        plt.ylim(0, 110)
        # ax.legend(bp["boxes"], ['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB'], loc='upper right')
        plt.legend()
        plt.grid()
        plt.savefig('../src/trajectory/mean' + str(i + 1) + '.png')
        # plt.savefig('../src/trajectory/time' + str(i+1) + '.png')
        plt.close()


def main():
    data = json.load(open('../data/perQuestion.json'))
    means, times, correct_times = get_stalist(data)

    all_data = json.load(open('../data/answers.json'))
    print(friedmanchisquare(all_data[0][0]['answer'], all_data[1][0]['answer']))
    print(friedmanchisquare(all_data[0][1]['answer'], all_data[1][1]['answer']))

    print(friedmanchisquare(all_data[0][0]['time'], all_data[1][0]['time']))
    print(friedmanchisquare(all_data[0][1]['time'], all_data[1][1]['time']))

    # for layout in range(len(all_data)):
    #     for level in range(len(all_data[layout])):
    #         for que in range(len(all_data[layout][level])):
    #             print(len(all_data[layout][level][que]))
    box_graph(means, times, all_data)
    # print('time')
    # print(wilcoxon(all_data[3][0]['time'], all_data[3][1]['time']))
    # print(wilcoxon(all_data[3][0]['time'], all_data[3][2]['time']))
    # print(wilcoxon(all_data[3][0]['time'], all_data[3][3]['time']))
    # print(wilcoxon(all_data[3][1]['time'], all_data[3][2]['time']))
    # print(wilcoxon(all_data[3][1]['time'], all_data[3][3]['time']))
    # print(wilcoxon(all_data[3][2]['time'], all_data[3][3]['time']))

    # print('accuracy')
    # print(wilcoxon(all_data[3][0]['answer'], all_data[3][1]['answer']))
    # print(wilcoxon(all_data[3][0]['answer'], all_data[3][2]['answer']))
    # print(wilcoxon(all_data[3][0]['answer'], all_data[3][3]['answer']))
    # print(wilcoxon(all_data[3][1]['answer'], all_data[3][2]['answer']))
    # print(wilcoxon(all_data[3][1]['answer'], all_data[3][3]['answer']))
    # print(wilcoxon(all_data[3][2]['answer'], all_data[3][3]['answer']))

    # for i in range(len(all_data)):
    #     for j in range(len(all_data[i])):
    #         for k in range(len(all_data[i][j]['time'])):
    #             all_data[i][j]['time'][k] = math.log(all_data[i][j]['time'][k])

    # print(shapiro(all_data[0][0]['time']), shapiro(all_data[0][1]['time']), shapiro(all_data[0][2]['time']), shapiro(all_data[0][3]['time']))
    # print(shapiro(all_data[1][0]['time']), shapiro(all_data[1][1]['time']), shapiro(all_data[1][2]['time']), shapiro(all_data[1][3]['time']))
    # print(shapiro(all_data[2][0]['time']), shapiro(all_data[2][1]['time']), shapiro(all_data[2][2]['time']), shapiro(all_data[2][3]['time']))
    # print(shapiro(all_data[3][0]['time']), shapiro(all_data[3][1]['time']), shapiro(all_data[3][2]['time']), shapiro(all_data[3][3]['time']))

    # result1 = f_oneway(all_data[0][0]['time'], all_data[0][1]['time'], all_data[0][2]['time'], all_data[0][3]['time'])
    # result2 = f_oneway(all_data[1][0]['time'], all_data[1][1]['time'], all_data[1][2]['time'], all_data[1][3]['time'])
    # result3 = f_oneway(all_data[2][0]['time'], all_data[2][1]['time'], all_data[2][2]['time'], all_data[2][3]['time'])
    # result4 = f_oneway(all_data[3][0]['time'], all_data[3][1]['time'], all_data[3][2]['time'], all_data[3][3]['time'])
    # print(result1.pvalue, result2.pvalue, result3.pvalue, result4.pvalue)


if __name__ == '__main__':
    main()
