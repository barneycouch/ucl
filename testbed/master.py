import re, sys, os
from collections import Counter
from itertools import islice

if len(sys.argv) != 5:
	print 'Please Provide 4 Valid Command Line Inputs:'
	print '<sliding window length> <sliding window step> <decreasing increment> <minimum window length>'
	exit(1)

windl = int(sys.argv[1]) #sliding window length
windinc = int(sys.argv[2]) #sliding window step
decreaseinc = int(sys.argv[3]) #amount to decrease window size every time
windmin = int(sys.argv[4]) #minimum window length

	
txtfolder = raw_input('Which folder would you like to scan for scaffolds? ')
print 'The Following folder selected: '
print txtfolder

files = os.listdir(txtfolder)

print '\n'
print 'The Following files will be processed: '
print files
print '\n'

fullist = []
slash = '/'
for i in files:
	path = txtfolder
	filename = i
	full = path + slash + filename
	fullist.append(full)

for el in fullist:
	targfile = open(el, 'r')
	execfile("scr14.py")