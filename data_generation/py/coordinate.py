# -*- coding: utf-8 -*-

import os
import sys
import subprocess

argvs = sys.argv
if len(argvs) != 2:
    print('lack of argvs')
    sys.exit()

os.chdir('/Users/Aoyama/Documents/Program/scalable-GIB/data_generation/rust-fd-layout/')

main = []
if argvs[1] == 'all':
    main.append('../../data_generation/data/TRGIB/temp/')
    main.append('../../data_generation/data/FDGIB/temp/')
else:
    main.append('../../data_generation/data/' + argvs[1] + '/temp/')

print(main)

inp = input('Are you really run this program? This can damage your data. (y/n) :')
if inp == 'y':
    for path in main:
        for dir in os.listdir(path):
            try:
                for file in os.listdir(path + dir):
                    if (file[-5:] == '.json'):
                        print(file)
                        cmd = 'cargo run --release --example gib-cli -- -f ' + path + dir + "/" + file + ' > ' + path + dir + "/" + file[:-5] + '-nodes.txt'
                        os.system(cmd)
                        print(dir, file)
            except:
                pass
else:
    pass

os.chdir('/Users/Aoyama/Documents/Program/scalable-GIB/data_generation/py/')
cmds = []
cmds.append('python add_coordinates.py ' + argvs[1])
print('add coordinates to file')

for cmd in cmds:
    os.system(cmd)
