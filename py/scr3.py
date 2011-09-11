import re
import sys

targfile = sys.argv[1] #provide the filename as an argument
infile = open(targfile, 'r') #open file to read

dict1 = {}
#strip whitespace, append lists with the elements
for line in infile:
	line2 = line.replace("\n", "")
	scaffidi, posi, cati = line2.split()
	dict1[posi] = cati

#dict1 contains positions and category pairs:
#k = position (eg 1, 2, 3, 4 etc.)
#v = category (eg ABBA, BABA etc.)
	
print '\n'
print dict1
print '\n'

el = []
for k, v in dict1.items():
	el.append(v)

#count the frequency of the categories
abbacnt = el.count('ABBA')
babacnt = el.count('BABA')
abbbcnt = el.count('ABBB')
babbcnt = el.count('BABB')
othercnt = el.count('other')
no_datacnt = el.count('no_data')

print '\n'
print 'In the whole file, ABBA - %g, BABA - %g, ABBB - %g, BABB - %g, Other - %g, No Data - %g' % (abbacnt, babacnt, abbbcnt, babbcnt, othercnt, no_datacnt)
print '\n'

windl = int(sys.argv[2]) #length of sliding window
windi = int(sys.argv[3]) #step of sliding window

#sort the dictionary by position, make a list of both sets

poslist = []
catlist = []
for key in sorted(dict1.iterkeys()):
	pos = key
	cat = dict1[key]
	poslist.append(pos)
	catlist.append(cat)

print poslist
print catlist
print '\n'
	
#initialise the sliding window function:
def slidingWindow(sequence, winSize, step=1):
	try: it = iter(sequence)
	except TypeError:
		raise Exception("no.")
	if not ((type(winSize) == type(0)) and (type(step) == type(0))):
		raise Exception("no.2.")
	if step>winSize:
		raise Exception("no.3.")
	if winSize > len(sequence):
		raise Exception("no.4.")
		
	numofChunks = ((len(sequence)-winSize)/step)+1
	
	for i in range(0, numofChunks, step):
		yield sequence[i:i+winSize]

print '\n'

chunklist = []
#make a list of n-chunks of the poslist, aka chunklist		
chunks = slidingWindow(poslist, windl, windi)
for chunk in chunks:
	chunklist.append(chunk)

print chunklist

for i in chunklist:
	for z in i:
		print i.index(z)
		print z
