from itertools import cycle
import time, sys

start = time.time()

if len(sys.argv) != 2:
	print 'PLEASE PROVIDE ADEQUATE COMMAND-LINE ARGUMENTS!'

fileopen = sys.argv[1]

matchlist = []

######
scafflist = []
poslist = []
catlist = []
for l in open(fileopen, 'r'): 
	scaff, pos, cat = l.split()
	scafflist.append(scaff)
	poslist.append(pos)
	catlist.append(cat)
######


running = True
scafflistcycle = cycle(scafflist)
#prime the pump
nextelem = scafflistcycle.next()

cnt = 0
cntmax = len(scafflist)

while cnt <= cntmax:
	thiselem, nextelem = nextelem, scafflistcycle.next()
	if thiselem != nextelem:
		matchlist.append(scafflist.index(thiselem))
	cnt += 1
	
matchlist.pop(0)
	
#print '\n'
#print 'scafflist: '
#print scafflist
#print '\n'
#print 'At these indexes, the previous element differs from the current one:'
#print matchlist
#print '\n'

#at the indexes of matchlist, start a new file
#try reading it into a list at first
linelist = []
linenum = 0
filecounter = 1
lenscafflist = len(scafflist)
#get the scafflist length so that if we come to the end the last string is written
for l in open(fileopen, 'r'):
	fileext = '.txt'
	filename = str(filecounter) + fileext
	fileout = open(filename, 'w')
	linelist.append(l)
	if (linenum + 1) in matchlist:
		for el in linelist:
			el = el.replace("\n", "")
			fileout.write('%s\n' % (el))
		fileout.close()
		filecounter += 1
		linelist = []
	if (linenum + 1) == lenscafflist:
		for el in linelist:
				el = el.replace("\n", "")
				fileout.write('%s\n' % (el))
	linenum += 1

	

print '\n'
print 'End of program, duration', time.time() - start, 'seconds.'
print '\n'