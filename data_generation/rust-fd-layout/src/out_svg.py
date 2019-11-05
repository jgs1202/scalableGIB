# -*- coding: utf-8 -*-

import os
import sys
import subprocess

argvs = sys.argv
if len(argvs) != 2:
    print('lack of argvs')
    sys.exit()

main = '../../forceInABox/data/' + argvs[1]

inp = input('Are you really run this program? This can damage your data. (y/n) :')
if inp == 'y':
    for dir in os.listdir(main):
        if (dir != '.DS_Store'):
        # if dir == '15-0.0001-0.05':
            try:
                for file in os.listdir(main + '/' + dir):
                        # if (file[-5:] == '.json'):
                        if ( file == '1.json' or file[0] == str(3) ) and file[-5:] == '.json':
                            cmd = 'cargo run --release --example gib -- -f ' + main + '/' + dir + '/' + file + ' > ' + main + '/' + dir + '/' + file[:-5] + '.svg'
                            # subprocess.call( cmd.strip().split(' ') )
                            os.system(cmd)
                            print(dir, file)
            except:
                pass
else:
    pass
