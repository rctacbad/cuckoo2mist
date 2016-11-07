Cuckoo2mist
===========

About
-----
This aims to convert Cuckoo JSON logs into MIST format.

This repository is a fork of http://sourceforge.net/p/cuckoo2mist/
Its original author is Philipp Trinius.

Usage
--------------------------
Specify folder containing Cuckoo JSON logs.

	$ python cuckoo2mist.py -i [Folder of Cuckoo logs]
	
Package Installation
---------------------
Python dependencies needed (install via `pip`)

	setuptools
	
From repository run

	$ python setup.py build
	$ python setup.py install
	
If successful, package can then be imported in Python

	>> import cuckoo2mist
	>> from cuckoo2mist import class_mist
	

MIST description 
--------------------
The Malware Instruction Set (MIST) is a representation for monitored behavior
of malicious software. The representation is optimized for effective and
efficient analysis of behavior using data mining and machine learning
techniques. It can be obtained automatically during analysis of malware with a
behavior monitoring tool or by converting existing behavior reports. The
representation is not restricted to a particular monitoring tool and thus can
also be used as a meta language to unify behavior reports of different sources.

