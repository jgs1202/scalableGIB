import os
from randData import *
from main import run
import json
from STGIB import ST
from add_coordinates import add


def main():
    print('Generating origin data...')
    makeData()

    print('Applying TRGIB layout...')
    mainDir = '../data/origin/TRGIB/'
    width = 960
    height = 600
    for file in os.listdir(mainDir):
        if (file != '.DS_Store'):
            path = mainDir + file
            graph = json.load(open(path))
            use = 'TRGIB'
            groups = [[] for i in range(graph['groupSize'])]
            length = len(graph['nodes'])
            for i in range(length):
                dic = {}
                dic['number'] = i
                groups[graph['nodes'][i]['group']].append(dic)
            ST(graph, groups, path, dir, file, width, height, use)
            path2 = '../data/origin/TRGIB/' + file
            graph = json.load(open(path2))
            for i in range(graph['groupSize']):
                graph['groups'][i]['id'] = graph['groups'][i]['name']
            graph = json.load(open(path))
            out = '../data/origin/TRGIB/'
            try:
                a = os.listdir(out)
            except:
                os.mkdir(out)
            run(graph, width, height, out + file)

    print('Defining coordinates of nodes within a box...')
    os.chdir('../rust-fd-layout')
    path = '../data/origin/TRGIB/'
    for file in os.listdir(path):
        if (file[-5:] == '.json'):
            cmd = 'cargo run --release --example gib-cli -- -f ' + path + file + ' > ' + path + file[:-5] + '-nodes.txt'
            os.system(cmd)

    os.chdir('../py')
    add('TRGIB')


if __name__ == '__main__':
    main()
