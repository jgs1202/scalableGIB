from main import run
import os
import json
from STGIB import ST
import datetime
import sys
from add_coordinates import calculation


def delte_temp():
    path = '../data/TRGIB/temp/'
    levels = ['low/', 'high/']

    for level in levels:
        for file in os.listdir(path + level):
            os.system('rm ' + path + level + file)


if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 3:
        print('argvs is lack')
        sys.exit()
    path = argvs[1]
    layout = argvs[2]

    main = '../data/origin/'
    width = 960
    height = 600
    graph = json.load(open(path))
    file_name = ''

    if layout == 'TRGIB':
        use = 'TRGIB'
        groups = [[] for i in range(graph['groupSize'])]
        # make list 'groups' a list have nodes' index
        length = len(graph['nodes'])
        for i in range(length):
            dic = {}
            dic['number'] = i
            groups[graph['nodes'][i]['group']].append(dic)
        file_name = path[:-5] + '-TRGIB.json'
        run(graph, width, height, file_name)

    os.chdir('/Users/Aoyama/Documents/Program/scalable-GIB/data_generation/rust-fd-layout/')
    cmd = 'cargo run --release --example gib-cli -- -f ' + file_name + ' > ' + file_name[:-5] + '-nodes.txt'
    os.system(cmd)
    os.chdir('/Users/Aoyama/Documents/Program/scalable-GIB/data_generation/py/')
    data = json.load(open(file_name, 'r'))
    f = open(file_name[:-5] + '-nodes.txt')
    txt = f.read()
    calculation(data, txt, layout, None, file_name)
    cmd = 'rm ' + file_name[:-5] + '-nodes.txt'
    os.system(cmd)
