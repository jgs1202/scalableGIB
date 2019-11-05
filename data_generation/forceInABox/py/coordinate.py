# -*- coding: utf-8 -*-

import os
import sys
import subprocess

argvs = sys.argv
if len(argvs) != 2:
    print('lack of argvs')
    sys.exit()

os.chdir('/Users/Aoyama/Documents/Program/brainEx/GIB/rust-fd-layout/src')
levels = ['high/', 'low/']

main = []
if argvs[1] == 'all':
    # main.append('../../forceInABox/data/STGIB/temp/')
    main.append('../../forceInABox/data/Chaturvedi/temp/')
    main.append('../../forceInABox/data/TRGIB/temp/')
    main.append('../../forceInABox/data/FDGIB/temp/')
else:
    main.append('../../forceInABox/data/' + argvs[1] + '/temp/')

inp = input('Are you really run this program? This can damage your data. (y/n) :')
if inp == 'y':
    print('start')
    for level in levels:
        for dir in main:
            for file in os.listdir(dir + level):
                print(file)
                if (file[-5:] == '.json'):
                    cmd = 'cargo run --release --example gib-cli -- -f ' + dir + level + file + ' > ' + dir + level + file[:-5] + '-nodes.txt'
                    # subprocess.call( cmd.strip().split(' ') )
                    os.system(cmd)
                    print(dir + level, file)
else:
    print('stop')
    pass
