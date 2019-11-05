from main import run
import os
import json
from STGIB import ST

if __name__ == '__main__':
    main = '../data/origin/TRGIB/'
    width = 960
    height = 600
    # for dir in os.listdir(main):
    #     if (dir != '.DS_Store'):
    dir = False
    for file in os.listdir(main):
        if (file != '.DS_Store'):
        # if dir == '15-0.001-0.1':
            # if file == '0.json' or file == '1.json' or file== '2.json':
            path = main + file
            graph = json.load(open(path))
            use = 'TRGIB'
            groups = [ [] for i in range(graph['groupSize'])]
            # make list 'groups' a list have nodes' index
            length = len(graph['nodes'])
            for i in range(length):
                dic = {}
                dic['number'] = i
                groups[graph['nodes'][i]['group']].append(dic)
            ST(graph, groups, path, dir, file, width, height, use)
            path2 = '../data/TRGIB/temp/' + file
            graph = json.load(open(path2))
            for i in range(graph['groupSize']):
                graph['groups'][i]['id'] = graph['groups'][i]['name']
                # graph['groups'][i]['name'] = graph['groups'][i]['id']
            graph = json.load(open(path))
            out = '../data/TRGIB/temp/'
            try:
                a = os.listdir(out)
            except:
                os.mkdir(out)
            run(graph, width, height, out + file)
