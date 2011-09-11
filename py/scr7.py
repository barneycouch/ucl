import re, sys
from collections import Counter

targfile = sys.argv[1] #provide the filename as an argument
infile = open(targfile, 'r') #open file to read

dict1 = {}
#strip whitespace, append lists with the elements
for line in infile:
	line2 = line.replace("\n", "")
	scaffidi, posi, cati = line2.split()
	#print scaffidi
	#print posi
	#print cati
	dict1[posi] = cati
	
#dict1 contains UNORDERED positions and category pairs:
#k = position (eg 1, 2, 3, 4 etc.)
#v = category (eg ABBA, BABA etc.)
	
#print '\n'
#print 'Dict1: '
#print dict1
#print '\n'

#make a list of all the position values, incremental of 1
idlist = []
keylist = dict1.keys()
keylist.sort()
for key in keylist:
	idlist.append(key)
#print idlist
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

def asint(s):
	try: return int(s), ''
	except ValueError: return sys.maxint, s
	
dict2 = [(k, dict1[k]) for k in sorted(dict1, key=asint)]

catlist = []
idlist = []

for k, v in dict2:
	idlist.append(int(k))
	catlist.append(v)

print '\n'
print 'idlist: '
print idlist
print '\n'
print 'catlist: '
print catlist
print '\n'
	
#initialise the sliding window function:
def slidingWindow(sequence, winSize, step=1):
	try: it = iter(sequence)
	except TypeError:
		raise Exception("no.1.")
	if not ((type(winSize) == type(0)) and (type(step) == type(0))):
		raise Exception("no.2.")
	if step>winSize:
		raise Exception("no.3.")
	if winSize > len(sequence):
		raise Exception("no.4.")
		
	numofChunks = ((len(sequence)-winSize)/step)+1
	
	for i in range(0, numofChunks, step):
		yield sequence[i:i+winSize]

#print '\n'

chunklist = []
#make a list of n-chunks of the idlist, aka chunklist		
chunks = slidingWindow(idlist, windl, windi)
for chunk in chunks:
	#print chunk
	#print '\n'
	chunklist.append(chunk)
	
#chunklist2 = []
#for i in chunklist:
#	for z in i:
#		chunklist2.append(z)

#do the same, but for the categories:

#initialise the sliding window function:
def slidingWindow(sequence, winSize, step=1):
	try: it = iter(sequence)
	except TypeError:
		raise Exception("no.1.")
	if not ((type(winSize) == type(0)) and (type(step) == type(0))):
		raise Exception("no.2.")
	if step>winSize:
		raise Exception("no.3.")
	if winSize > len(sequence):
		raise Exception("no.4.")
		
	numofChunks = ((len(sequence)-winSize)/step)+1
	
	for i in range(0, numofChunks, step):
		yield sequence[i:i+winSize]

#print '\n'

chunklist3 = []
#make a list of n-chunks of the idlist, aka chunklist		
chunks = slidingWindow(catlist, windl, windi)
for chunk in chunks:
	chunklist3.append(chunk)
	
#chunklist4 = []
#for i in chunklist3:
#	for z in i:
#		chunklist4.append(z)

fpout = open("l.txt", 'w')
fpout.write("POS\tABBA\tBABA\tABBB\tBABB\tother\tno_data")

print '\n'
#print 'chunklist: '
#print chunklist
#print '\n'
#print 'chunklist3: '
#print chunklist3
print '\n'

idlistcnt = 0
poswrite = []
while idlistcnt <= (len(idlist) - 1):
	if windi >= len(idlist):
		break
	forwrite = idlist.pop(idlistcnt)
	poswrite.append(forwrite)
	idlistcnt += (windi - 1)

idint = 0	
	
for i in chunklist3:
	cnt = Counter()
	for word in i:
		cnt[word] += 1
	forwriteABBA = str(cnt['ABBA'])
	forwriteBABA = str(cnt['BABA'])
	forwriteABBB = str(cnt['ABBB'])
	forwriteBABB = str(cnt['BABB'])
	forwriteother = str(cnt['other'])
	forwriteno_data = str(cnt['no_data'])
	idwrite = poswrite.pop(idint)
	fpout.write('\n')
	fpout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idwrite, forwriteABBA, forwriteBABA, forwriteABBB, forwriteBABB, forwriteother, forwriteno_data))

fpout.close()