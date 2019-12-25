import json
import math
import matplotlib
from statistics import mean, stdev
from scipy.stats import f_oneway, friedmanchisquare, shapiro, wilcoxon
import matplotlib.pyplot as plt
import seaborn as sns


def verify_layout(layout):
    if layout == 'STGIB':
        return 0
    elif layout == 'Chaturvedi':
        return 1
    elif layout == 'FDGIB':
        return 2
    elif layout == 'TRGIB':
        return 3


def box_graph(data, title):
    # data = (data[0], data[1], data[2], data[3])
    # print(data)
    sns.set()
    sns.set_style("whitegrid", {'grid.linestyle': '--'})
    sns.set_context("paper", 1.5, {"lines.linewidth": 4})
    sns.set_palette("winter_r", 8)
    sns.set('talk', 'whitegrid', 'dark',
        rc={"lines.linewidth": 2, 'grid.linestyle': '--'})
    fig, ax = plt.subplots()
    bp = ax.boxplot(data, vert=True, patch_artist=True)
    # bp = ax.boxplot(time[i], vert=True, patch_artist=True)
    for box in bp['boxes']:
        box.set(color="black", linewidth=1.5)
    for box in bp['medians']:
        plt.setp(box, color="black", linewidth=1.5)
    for box in bp['caps']:
        plt.setp(box, color="black", linewidth=1.5)
    for box in bp['whiskers']:
        plt.setp(box, ls="solid", color="black", linewidth=1.5)
    for box, color in zip(bp["boxes"], sns.color_palette("Set3",6)):
        box.set_facecolor(color)
    ax.set_xticklabels(['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB'])
    # plt.xlabel('layout', fontsize=20)
    # plt.ylabel(title, fontsize=20)
    # font = {'family' : 'normal',
    #     'weight' : 'bold',
    #     'size'   : 64}

    # matplotlib.rc('font', **font)
    # plt.ylabel('completion time [ms]')
    if title == 'Screen Space Efficiency':
        plt.ylim(0, 110)
    if title == 'Group Box Aspect Ratio':
        plt.ylim(0.5, 3.5)
    # plt.ylim(0, 110)
    # ax.legend(bp["boxes"], ['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB'], loc='upper right')
    plt.legend()
    plt.grid()
    plt.savefig('../src/trajectory/' + title + '.png')
    # plt.savefig('../src/trajectory/time' + str(i+1) + '.png')
    plt.close()


def main():
    angle = json.load(open('../flaski/angle.json'))
    data = []
    for i in angle:
        data.append(i['data'])
    box_graph(data, 'Crossing Angle')



if __name__ == '__main__':
	main()