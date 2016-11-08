#!/usr/bin/env python
# encoding: utf-8
"""
cuckoo2mist.py

Created by Dr. Philipp Trinius on 2013-11-10.
Copyright (c) 2013 pi-one.net . 

This program is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or (at your option) 
any later version.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
more details.

You should have received a copy of the GNU General Public License along with 
this program; if not, see <http://www.gnu.org/licenses/>
"""

__author__ = "philipp trinius"
__version__ = "0.2"



import re
import os, sys
import getopt
import subprocess
import time
import hashlib
import xml.etree.ElementTree as ET
import glob
import argparse

from cuckoo2mist.thread_mist import th_seq2mist
from constants import *

max_threads	= 10
user_interrupt	= False

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def get_log_md5s():
	result = {}
	for f in os.listdir('log'):
		hfile = open(os.path.join('log', f), "r")
		h = hashlib.sha1()
		h.update(hfile.read())
		result[f] = h.hexdigest()
		hfile.close()
	return result

def read_configuration(fconfigdir):
	elements2mist = ET.ElementTree()
	elements2mist.parse(os.path.join(fconfigdir, CONF_ELEM2MIST))

	types2mist = ET.ElementTree()
	types2mist.parse(os.path.join(fconfigdir, CONF_TYPES2MIST))	
	return elements2mist, types2mist

def generate_Mist_Reports(files, e2m, t2m):
	global max_threads
	### Determine the IDs of analysis that yet not have been converted ########################################
	seqReportRows = []
	for ffile in files:
		seqReportRows.append({'analysis_id': None, 'seq_path': ffile})

	### Convert reports to MIST representation (in threads) ####################################
	thlist = []
	try:
		for seqReportRow in seqReportRows:
			while len(thlist) >= max_threads:
				time.sleep(5)
				for t in thlist:
					t.join(2.0)
					if not t.isAlive():
						thlist.remove(t)
			t = th_seq2mist(input_file=seqReportRow["seq_path"], elements2mist=e2m, types2mist=t2m, analysis_id=seqReportRow["analysis_id"])
			thlist.append(t)
			t.start()
	except KeyboardInterrupt:
		pass
	print '\nAborting %s threads...' % len(thlist)
	for t in thlist:
		t.join()
		thlist.remove(t)
		print '  Aborted one thread - %s remaining' % len(thlist)
		sys.stdout.flush()
	print "  --> All threads aborted\n"



def main(argv=None):
	try:
		opt = argparse.ArgumentParser(description="Convert Cuckoo logs into MIST reports")
		opt.add_argument("-i", "--input", action="store", dest="folder", help="Folder path of Cuckoo logs")
		opt.add_argument("-t", "--taskids", action="append", nargs=3, metavar=("run_folder", "start", "end"), help="Convert JSON logs, by task_id and run, into MIST format. specify START and END task ids")
		if len(sys.argv) < 2:
			opt.print_help()
			sys.exit()
		options = opt.parse_args()
		f_configdir = CONF_FOLDER
		if options.folder:
			f_input = options.folder

                        print "Reading configuration files from %s ..." % (f_configdir), 
                        (e2m, t2m) = read_configuration(f_configdir)
                        print " done."
                        
                        log_md5s_before = get_log_md5s()
                        
                        print "Reading %s" % (f_input),
                        files = []
                        if os.path.exists(f_input):
                                for ffile in os.listdir(f_input):
                                        file = os.path.join(f_input, ffile)
                                        if os.path.isfile(file) and file.endswith(".json"):
                                                files.append(file)
                                                print ".",
                        if len(files) == 0:
                                # no reports found
                                print "No reports found."
                                sys.exit(1)
                        else:
                                print " done."
                                
                        generate_Mist_Reports(files, e2m, t2m)
                        
                elif options.taskids:
                        run_folder = options.taskids[-1][0]
                        start = options.taskids[-1][1]
                        end = options.taskids[-1][2]
                        print run_folder, start, end
                        try:
                                from scripts.convert_json import process_tasks

                                process_tasks(ALL_ANALYSES, str(run_folder), int(start), int(end))
                        except Exception as e:
                                print "Script import error\n"
                                print e
                                sys.exit()
		else:
                        opt.print_help()
                        sys.exit()

							
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())

