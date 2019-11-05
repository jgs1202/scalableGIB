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
    for dir in os.listdir(main):
        if not dir == '.DS_Store':
            for file in os.listdir(main + dir):
                if dir != '.DS_Store' and dir[:5] == 'mid-l':
                    # if file == '0.json' or file == '1.json' or file== '2.json':
                    path = main + dir + "/" + file
                    graph = json.load(open(path))
                    use = 'TRGIB'
                    groups = [[] for i in range(graph['groupSize'])]
                    # make list 'groups' a list have nodes' index
                    length = len(graph['nodes'])
                    for i in range(length):
                        dic = {}
                        dic['number'] = i
                        groups[graph['nodes'][i]['group']].append(dic)
                    # ST(graph, groups, path, dir, file, width, height, use)
                    # for i in range(graph['groupSize']):
                    #     graph['groups'][i]['name'] = graph['groups'][i]['id']
                    # graph = json.load(open(path))
                    out = '../data/TRGIB/temp/' + dir + '/'
                    try:
                        a = os.listdir(out)
                    except:
                        os.mkdir(out)
                    run(graph, width, height, out + file)
