from main import run
import os
import json
from STGIB import ST
import datetime

if __name__ == '__main__':
    main = '../data/origin/TRGIB/'
    width = 960
    height = 600

    actualLevels = ['high', 'low']
    refLevels = ['high-mid', 'low-mid']

    dir = False
    # for dir in os.listdir(main):
    #     if not dir == '.DS_Store':

    time = datetime.datetime.now()
    for dir_num, dir in enumerate(refLevels):
        for file in os.listdir(main + dir):
            if file != '.DS_Store':
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

                out = '../data/TRGIB/temp/' + actualLevels[dir_num] + '/'
                try:
                    a = os.listdir(out)
                except:
                    os.mkdir(out)
                print(path)
                run(graph, width, height, out + file)
    print(datetime.datetime.now() - time)

    cmds = ['python TRGIB.py', 'python coordinate.py TRGIB', 'python add_coordinate.py TRGIB', 'python arrangeForTask.py', 'python route.py', 'python metrics.py']
    for i in cmds:
        cmd = i
    os.system(cmd)
