#!/usr/bin/env python
# encoding: utf-8
"""
convert_json.py

script called by cuckoo2mist.py. Processes task ids
arguments, start and end task id number, are given in main script
"""

__author__ = "joa suico"
__version__ = "0.1"  

import os, sys
import glob
import fnmatch

def process_tasks(ALL_ANALYSES, run_folder, start, end):
    from cuckoo2mist import class_mist

    json_files = []
    for root, dirname, filenames in os.walk(os.path.join(ALL_ANALYSES, run_folder)):
        for filename in fnmatch.filter(filenames, "report.json"):
            json_files.append(os.path.join(root, filename))

    task_ids = range(start, end+1)
    needed_files = [path for path in json_files for i in task_ids if "/{}/".format(i) in path]
    
    for i in needed_files:
        try:
            cm = class_mist.mistit(i)
            if cm.parse() and cm.convert():
                temp_path = i.replace("report.json", "report.mist")
                cm.write(os.path.join("reports", temp_path.replace("/", "-")))
        except Exception as e:
            print "Cannot convert {}".format(i)
            print e
            continue
