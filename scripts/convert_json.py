#!/usr/bin/env python
# encoding: utf-8
"""
convert_json.py

script called by cuckoo2mist.py. Processes task ids
"""

__author__ = "joa suico"
__version__ = "0.1"  

import os, sys
import glob

ALL = "all_analyses"

def process_tasks():
    run_folder = raw_input("CBAQ run folder: ")
    start = int(raw_input("start task id: "))
    end = int(raw_input("end task id: "))

    myfolder = os.path.join(ALL, run_folder)

    if os.path.exists(myfolder):
        from cuckoo2mist import class_mist
    else:
        print "Folder does not exist.\n"
        print sys.exit()


if __name__ == '__main__':
    process_tasks()
