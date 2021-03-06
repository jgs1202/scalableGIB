# -*- coding: utf-8 -*-

import os
import json
import sys


def delete_comp(outputs):
    levels = ['low/', 'high/']
    for output in outputs:
        for level in levels:
            for file in os.listdir(output + level):
                os.system('rm ' + output + level + file)


def calculation(data, txt, layout, dir, file):
    minus = False
    length = len(data['nodes'])
    list = [i for i in range(length)]
    sentence = ''
    num = 0
    name = 0
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
            data['nodes'][i]['cx'] = list[data['nodes'][i]['id']]['cx']
            data['nodes'][i]['cy'] = list[data['nodes'][i]['id']]['cy']
        data['layout'] = layout
        if dir is not None:
            try:
                current = os.listdir(dir)
            except:
                os.mkdir(dir)
        f = open(file, 'w')
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def add(layout):
    mains = []
    outputs = []
    layouts = []
    if layout == 'all':
        mains.append('../data/FDGIB/temp/')
        outputs.append('../data/FDGIB/comp/')
        layouts.append('FDGIB')
        mains.append('../data/TRGIB/temp/')
        outputs.append('../data/TRGIB/comp/')
        layouts.append('TRGIB')
    else:
        mains.append('../data/' + layout + '/temp/')
        outputs.append('../data/' + layout + '/comp/')
        layouts.append(layout)

    delete_comp(outputs)
    for pathNumber, path in enumerate(mains):
        for dir in os.listdir(path):
            if dir != '.DS_Store':
                for file in os.listdir(path + dir):
                    if file[-5:] == '.json':
                        f = open(path + dir + '/' + file[:-5] + '-nodes.txt')
                        txt = f.read()
                        reader = open(path + dir + '/' + file)
                        data = json.load(reader)
                        output_dir = outputs[pathNumber] + dir + '/'
                        output_file = output_dir + file
                        calculation(outputs, layouts, data, txt, layouts[pathNumber], output_dir, output_file)
    else:
        pass


if __name__ == '__main__':
    argvs = sys.argv
    add(argvs[1])
