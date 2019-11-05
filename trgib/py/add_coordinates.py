# -*- coding: utf-8 -*-

import os
import json
import sys


def add(layout):
    mains = []
    outputs = []
    layouts = []
    if layout == 'all':
        mains.append('../data/origin/TRGIB/')
        outputs.append('../data/comp/TRGIB/')
        layouts.append('TRGIB')
    else:
        mains.append('../data/origin/' + layout + '/')
        outputs.append('../data/comp/' + layout + '/')
        layouts.append(layout)

    # inp = input('Are you really run this program? This can damage your data. (y/n) :')
    inp = 'y'
    if inp == 'y':
        for dir in range(len(mains)):
            for file in os.listdir(mains[dir]):
            # for dataNum in range(10):
                if file[-5:] == '.json':
                    minus = False
                    f = open(mains[dir] + file[:-5] + '-nodes.txt')
                    txt = f.read()
                    reader = open(mains[dir] + file)
                    global data
                    data = json.load(reader)

                    length = len(data['nodes'])
                    list = [i for i in range(length)]
                    sentence = ''
                    num = 0
                    name = 0
                    # print(main[dir], num)
                    for i in txt:
                        try:
                            i = int(i)
                        except:
                            pass
                        if type(i) == int:
                            sentence += (str(int(i)))
                        else:
                            if i == '.':
                                sentence = sentence + '.'
                            elif i == '-':
                                minus = True
                                break
                            else:
                                if num == 0:
                                    global dic
                                    dic = {}
                                    dic['cx'] = float(sentence)
                                    sentence = ''
                                    num += 1
                                elif num == 1:
                                    dic['cy'] = float(sentence)
                                    # dic['name'] = name
                                    sentence = ''
                                    num = 0
                                    list[name] = dic
                                    name += 1
                                else:
                                    print('error')
                    if minus:
                        print('break')

                    else:
                        for i in range(length):
                            # print(i, list[data['nodes'][int(i)]['name']])
                            data['nodes'][i]['cx'] = list[data['nodes'][i]['name']]['cx']
                            data['nodes'][i]['cy'] = list[data['nodes'][i]['name']]['cy']
                        data['layout'] = layouts[dir]

                        try:
                            current = os.listdir(outputs[dir])
                        except:
                            os.mkdir(outputs[dir])
                        f = open(outputs[dir] + file, 'w')
                        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    else:
        pass


if __name__ == '__main__':
    add()
