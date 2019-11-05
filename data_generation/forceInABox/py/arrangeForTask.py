import os
import math
import json
from setAnswer import calc
import random


def arrange():
    inputPath = []
    # inputPath.append('../data/Chaturvedi/comp/')
    inputPath.append('../data/FDGIB/comp/')
    inputPath.append('../data/TRGIB/comp/')

    levels = ['low/', 'high/']
    levelNums = [30, 20]
    outputPath = []
    outputPath.append('../data/experiment/low/')
    outputPath.append('../data/experiment/high/')

    for output in outputPath:
        if not os.path.exists(output):
            os.mkdir(output)

    order = 0
    num = 0
    outData = [[] for i in range(4)]

    for level in range(len(levels)):
        num = 0
        for i in inputPath:
            for file in os.listdir(i + levels[level]):
                if file != '.DS_Store':
                    order = order % 4
                    data = json.load(open(i + levels[level] + file, 'r'))
                    data = calc(data)
                    data['type'] = i[8:13]
                    data['level'] = levels[level][:-1]
                    data['set'] = math.floor(num / levelNums[level])
                    outData[order].append(data)
                    if not os.path.exists(outputPath[level] + str(math.floor(num / levelNums[level]))):
                        os.mkdir(outputPath[level] + str(math.floor(num / levelNums[level])))
                    f = open(outputPath[level] + str(math.floor(num / levelNums[level])) + '/' + str(num%levelNums[level]) + '.json',  'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                    num += 1
                if num % 60 == 0:
                    print(num)
                    break


def main():
    arrange()
    cmds = []
    cmds.append('rm -r ../../../src/data/low')
    cmds.append('rm -r ../../../src/data/high')
    cmds.append('mv ../data/experiment/low ../../../src/data/')
    cmds.append('mv ../data/experiment/high ../../../src/data/')
    for cmd in cmds:
        os.system(cmd)

if __name__ == '__main__':
    main()
