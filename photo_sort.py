#!/usr/bin/python

import os, shutil, datetime

PHOTOPATH = '/Users/bonnie/Pictures'
DUPPATH = '/Users/bonnie/Pictures/duplicates'

for item in os.listdir(PHOTOPATH):
	item_fullpath = os.path.join(PHOTOPATH, item)
	if os.path.isfile(item_fullpath) and item[0] != '.':
		file_date_unix = os.path.getmtime(item_fullpath)
		file_date = datetime.datetime.fromtimestamp(file_date_unix)
		year = file_date.strftime('%Y')
		foldername = file_date.strftime('%Y-%m-%d')
		dirname = os.path.join(PHOTOPATH, year,foldername)
		
		if not os.path.exists(dirname): 
			alternate_foldername = file_date.strftime('%Y_%m_%d')
			alternate_dirname = os.path.join(PHOTOPATH, year, alternate_foldername)
			if os.path.exists(alternate_dirname):
				dirname = alternate_dirname
			else:
				os.mkdir(dirname)
				print "*****made directory " + dirname
				
		if os.path.exists(os.path.join(dirname, item)):
			dest = DUPPATH
		else:
			dest = dirname
				
		shutil.move(item_fullpath, dest)
		print "moved " + item_fullpath + " to " + dest 
