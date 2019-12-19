import os
import json
import random


def make_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except:
        pass


def delete_file():
    path = '../../src/data/'
    for dir in os.listdir(path):
        if dir != '.DS_Store':
            dir += '/'
            for file in os.listdir(path + dir):
                os.system('rm ' + path + dir + file)


def delete_random():
    path = '../../src/data/random/'
    for file in os.listdir(path):
        os.system('rm ' + path + file)


def rename_FDGIB(max):
    paths = ['../data/FDGIB/comp/high/', '../data/FDGIB/comp/low/']

    for path in paths:
        number = 0
        ref = 0
        while(number < max):
            try:
                data = json.load(open(path + str(ref) + '.json', 'r'))
                f = open(path + str(number) + '.json', 'w')
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                number += 1
            except:
                ref += 1


def arrange():
    delete_file()

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


def random_arrange(each_num):
    delete_random()
    rename_FDGIB(30)

    out = '../../src/data/random/'
    input_paths = ['../data/FDGIB/comp/', '../data/TRGIB/comp/']
    level_names = ['high/', 'low/']

    index = [i for i in range(each_num * 4)]
    _levels = [0 for i in range(each_num * 2)]
    _levels.extend([1 for i in range(each_num * 2)])
    _layouts = [0 for i in range(each_num)]
    _layouts.extend([1 for i in range(each_num)])
    _layouts.extend([0 for i in range(each_num)])
    _layouts.extend([1 for i in range(each_num)])
    _questions = [i for i in range(each_num)]
    _questions.extend([i for i in range(each_num)])
    _questions.extend([i for i in range(each_num)])
    _questions.extend([i for i in range(each_num)])

    random.shuffle(index)
    levels = [_levels[index[i]] for i in range(each_num * 4)]
    questions = [_questions[index[i]] for i in range(each_num * 4)]
    layouts = [_layouts[index[i]] for i in range(each_num * 4)]

    make_dir(out)
    for i in range(each_num * 4):
        data = json.load(open(input_paths[layouts[i]] + level_names[levels[i]] + str(questions[i]) + '.json', 'r'))
        f = open(out + str(i) + '.json', 'w')
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def main():
    # arrange()
    random_arrange(30)

if __name__ == '__main__':
    main()
