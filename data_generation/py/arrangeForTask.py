import os
import json
import random


def arrange():
    inputPath = []
    inputPath.append('../data/FDGIB/comp/')
    inputPath.append('../data/TRGIB/comp/')

    outputPath = ('../../src/data/')
    levels = ['low', 'high']

    if os.path.exists(outputPath) is not True:
        os.mkdir(outputPath)

    order = 0
    total = 0
    outData = [[] for i in range(4)]

    for level in levels:
        num = 0
        for input in inputPath:
            for file in os.listdir(input + level + '/'):
                if file != '.DS_Store':
                    data = json.load(open(input + level + '/' + file))
                    f = open(outputPath + level + '/' + str(num) + '.json', 'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                    num += 1

def main():
    arrange()

if __name__ == '__main__':
    main()
