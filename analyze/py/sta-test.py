import json
import math
from statistics import mean, stdev
from scipy import stats
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
            datum = data[layout][level]
            means[layout][level].extend(datum['answer'])
            for time in datum['all_time']:
                times[layout][level].append(int(time))
            for time in datum['correct_time']:
                correct_times[layout][level].append(int(time))
    return means, times, correct_times


def box_graph(means, times, correct_times, data):
    mean = []
    time = []
    correct_time = []
    for i in range(layouts_number):
        mean.append((means[0][i], means[1][i]))
        time.append((times[0][i], times[1][i]))
        correct_time.append((correct_times[0][i], correct_times[1][i]))
    for i in range(layouts_number):
        sns.set()
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        sns.set_context("paper", 1.5, {"lines.linewidth": layouts_number})
        sns.set_palette("winter_r", 8)
        sns.set('talk', 'whitegrid', 'dark', rc={"lines.linewidth": 2, 'grid.linestyle': '--'})
        fig, ax = plt.subplots()
        # bp = ax.boxplot(mean[i], vert=True, patch_artist=True)
        bp = ax.boxplot(time[i], vert=True, patch_artist=True)
        # bp = ax.boxplot(correct_time[i], vert=True, patch_artist=True)
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
        fig.subplots_adjust(top=0.95, bottom=0.2, left=0.17, right=0.97)
        ax.set_xticklabels(['FD-GIB', 'TR-GIB'], fontsize=20)
        plt.tick_params(labelsize=22)
        plt.xlabel('layout', fontsize=24)

        # plt.ylim(0, 110)
        # ax.legend(bp["boxes"], ['FD-GIB', 'TR-GIB'], loc='upper right')
        # plt.legend()
        plt.grid()

        # plt.ylabel('accuracy [%]', fontsize=28)
        # plt.savefig('../data/mean' + str(i + 1) + '.png')

        plt.ylabel('completion time [ms]', fontsize=28)
        plt.savefig('../data/time' + str(i+1) + '.png')

        # plt.ylabel('completion time [ms]', fontsize=28)
        # plt.savefig('../data/correct-time' + str(i+1) + '.png')

        plt.close()


def main():
    data = json.load(open('../data/perQuestion.json'))
    all_data = json.load(open('../data/answers.json'))

    # means, times, correct_times = get_stalist(data)
    means, times, correct_times = get_stalist(all_data)

    # print(means)
    # print(stats.ttest_rel(means[0][1], means[1][1]))
    # print(mean(means[0][1]), mean(means[1][1]))

    for layout in range(len(all_data)):
        for level in range(len(all_data[layout])):
            for answer in range(len(all_data[layout][level]['answer'])):
                all_data[layout][level]['answer'][answer] = int(all_data[layout][level]['answer'][answer])
            for time in range(len(all_data[layout][level]['all_time'])):
                all_data[layout][level]['all_time'][time] = int(all_data[layout][level]['all_time'][time])
            for time in range(len(all_data[layout][level]['correct_time'])):
                all_data[layout][level]['correct_time'][time] = int(all_data[layout][level]['correct_time'][time])

    print('answer')
    print(mean(all_data[0][0]['answer']), mean(all_data[1][0]['answer']))
    print(stats.wilcoxon(all_data[0][0]['answer'], all_data[1][0]['answer']))
    print(mean(all_data[0][1]['answer']), mean(all_data[1][1]['answer']))
    print(stats.wilcoxon(all_data[0][1]['answer'], all_data[1][1]['answer']))

    print('correct time')
    print(mean(all_data[0][0]['correct_time']), mean(all_data[1][0]['correct_time']))
    print(stats.mannwhitneyu(all_data[0][0]['correct_time'], all_data[1][0]['correct_time']))
    print(mean(all_data[0][1]['correct_time']), mean(all_data[1][1]['correct_time']))
    print(stats.mannwhitneyu(all_data[0][1]['correct_time'], all_data[1][1]['correct_time']))

    print('all time')
    print(mean(all_data[0][0]['all_time']), mean(all_data[1][0]['all_time']))
    print(stats.wilcoxon(all_data[0][0]['all_time'], all_data[1][0]['all_time']))
    print(mean(all_data[0][1]['all_time']), mean(all_data[1][1]['all_time']))
    print(stats.wilcoxon(all_data[0][1]['all_time'], all_data[1][1]['all_time']))

    # for layout in range(len(all_data)):
    #     for level in range(len(all_data[layout])):
    #         for que in range(len(all_data[layout][level])):
    #             print(len(all_data[layout][level][que]))
    # print('time')
    # print(stats.wilcoxon(all_data[0][0]['all_time'], all_data[1][0]['all_time']))
    # print(stats.wilcoxon(all_data[0][1]['all_time'], all_data[1][1]['all_time']))

    # print('accuracy')
    # print(stats.wilcoxon(all_data[0][0]['answer'], all_data[1][0]['answer']))
    # print(stats.wilcoxon(all_data[0][1]['answer'], all_data[1][1]['answer']))

    box_graph(means, times, correct_times, all_data)

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
