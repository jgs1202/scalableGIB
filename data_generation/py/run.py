import os
from randData import *
from main import run
import json
from STGIB import ST
from FDGIB import force
from resize import sizing
from add_coordinates import add


def tr():
    print('Applying TRGIB layout...')
    mainDir = '../data/origin/TRGIB/'
    width = 960
    height = 600
    for file in os.listdir(mainDir):
        if (file[-5:] == '.json'):
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


def fd():
    print('applying TRGIB layout...')
    mainDir = '../data/origin/FDGIB/'
    width = 960
    height = 600
    for file in os.listdir(mainDir):
        if (file[-5:] == '.json'):
            path = mainDir + file
            graph = json.load(open(path))
            use = 'FDGIB'
            groups = [[] for i in range(graph['groupSize'])]

            graph = make_index_group(graph, width, height)
            # get length of group
            maxGroup = 0
            length = len(graph['nodes'])
            for i in range(length):
                current = graph['nodes'][i]['group']
                if current > maxGroup:
                    maxGroup = current
            groups = [[] for i in range(maxGroup+1)]
            # make list 'groups' a list have nodes' index
            for i in range(length):
                dic = {}
                dic['number'] = i
                groups[graph['nodes'][i]['group']].append(dic)
            for i in range(length):
                dic = {}
                dic['number'] = i
                groups[graph['nodes'][i]['group']].append(dic)

            # path2 = '../data/origin/TRGIB/' + file
            # graph = json.load(open(path2))
            # for i in range(graph['groupSize']):
            #     graph['groups'][i]['id'] = graph['groups'][i]['name']
            # graph = json.load(open(path))
            with_box = sizing(force(graph, width, height, groups))
            out = '../data/origin/FDGIB/'
            try:
                a = os.listdir(out)
            except:
                os.mkdir(out)
            f = open(out + file, 'w')
            json.dump(with_box, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            f.close()

    print('Defining coordinates of nodes within a box...')
    os.chdir('../rust-fd-layout')
    path = '../data/origin/FDGIB/'
    for file in os.listdir(path):
        if (file[-5:] == '.json'):
            cmd = 'cargo run --release --example gib-cli -- -f ' + path + file + ' > ' + path + file[:-5] + '-nodes.txt'
            os.system(cmd)
            cmd = 'cargo run --release --example gib -- -f ' + path + file + ' > ' + path + file[:-5] + '.svg'
            os.system(cmd)

    os.chdir('../py')
    add('FDGIB')


def make_index_group(graph, width, height):
    graph['groups'] = [{"id": i} for i in range(int(graph['groupSize']) + 1)]
    graph['groups'][-1]['dx'] = width
    graph['groups'][-1]['dy'] = height
    graph['groups'][-1]['x'] = 0.
    graph['groups'][-1]['y'] = 0.
    return graph


def main():
    print('Generating origin data...')
    makeData()
    tr()
    fd()


if __name__ == '__main__':
    main()
