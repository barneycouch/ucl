import tempfile, sys, time
from os import removedirs
start = time.time()

fileopen = sys.argv[1]
infile = open(fileopen, 'r')

if len(sys.argv) != 2:
	print 'ERROR!'

scafflist = []
dict1 = {}
for line in infile:
	line2 = line.replace("\n", "")
	scaffidi, posi, cati = line2.split()
	scafflist.append(scaffidi)
	dict1[posi] = cati

dirname = tempfile.mkdtemp()

tempfile = tempfile.mktemp()

scaffids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

removedirs(dirname)

print 'Program duration', time.time() - start, 'seconds.'