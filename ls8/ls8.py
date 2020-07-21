#!/usr/bin/env python3

"""Main."""

import sys
from os.path import join
from cpu import *
# filename = sys.argv[1]
filename = open(join('./examples/', sys.argv[1]), 'r')
code = filename.readlines()
filename.close()
cpu = CPU()
cpu.load(code)

# try:
#     cpu.load(filename)
# except:
#     sys.exit('Error')
# cpu.load()
# cpu.run()
