import json
import math
import matplotlib
from statistics import mean, stdev
from scipy.stats import f_oneway, friedmanchisquare, shapiro, wilcoxon
import matplotlib.pyplot as plt
import seaborn as sns
import os
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
    ax.set_xticklabels(['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB'], fontsize=24)
    # plt.xlabel('layout', fontsize=20)
    # plt.ylabel(title, fontsize=20)
    # font = {'family' : 'normal',
    #     'weight' : 'bold',
    #     'size'   : 64}

    # matplotlib.rc('font', **font)
    # plt.ylabel('completion time [ms]')
    # plt.rcParams["font.sisze"] = 24
    plt.tick_params(labelsize=22)
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


def inner_ratio():
    main_path = '../../data_generation/data/origin/'
    dirs = ['low-mid/', 'high-mid/']

    ratios = []
    for dir in dirs:
        for file in os.listdir(main_path + dir):
            if file[-5:] == '.json':
                data = json.load(open(main_path + dir + file, 'r'))
                inner_links = 0
                inter_links = 0
                links = len(data['links'])
                for link in data['links']:
                    if data['nodes'][link['source']]['group'] == data['nodes'][link['target']]['group']:
                        inner_links += 1
                    else:
                        inter_links += 1
                if inner_links / inter_links < 10:
                    ratios.append(inner_links / inter_links)
    print(mean(ratios), stdev(ratios))


def main():
    data = json.load(open('../flaski/result.json'))
    edgecross = [[] for i in range(4)]
    space = [[] for i in range(4)]
    aspect = [[] for i in range(4)]
    length = [[] for i in range(4)]
    for datum in data:
        layout = verify_layout(datum['type'])
        edgecross[layout].extend(datum['edgeCross'])
        space[layout].extend(datum['meanSpaceWasted'])
        aspect[layout].extend(datum['meanAspect'])
        length[layout].extend(datum['edgeLength'])
    box_graph(edgecross, 'The Number of Edge Crossings')
    box_graph(space, 'Screen Space Efficiency')
    box_graph(aspect, 'Group Box Aspect Ratio')
    box_graph(length, 'Uniform Edge Length')



if __name__ == '__main__':
	# main()
    inner_ratio()