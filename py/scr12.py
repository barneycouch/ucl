import time
start = time.time()
import re, sys
from collections import Counter
from itertools import islice

if len(sys.argv) != 4:
	print "!Input Error! Need <source file>  <window length>  <window increment> arguments."
	exit(1)

targfile = sys.argv[1] #provide the filename as an argument
infile = open(targfile, 'r') #open file to read

dict1 = {}
scafflist = []
#strip whitespace, append lists with the elements
for line in infile:
	line2 = line.replace("\n", "")
	scaffidi, posi, cati = line2.split()
	scafflist.append(scaffidi)
	dict1[posi] = cati
	
#print 'scafflist: '
#print scafflist
#print '\n'
	
#dict1 contains UNORDERED positions and category pairs:
#k = position (eg 1, 2, 3, 4 etc.)
#v = category (eg ABBA, BABA etc.)

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

def asint(s):
	try: return int(s), ''
	except ValueError: return sys.maxint, s
	
dict2 = [(k, dict1[k]) for k in sorted(dict1, key=asint)]

catlist = []
idlist = []
print 'Constructing idlist, catlist.... '
print '\n'
for k, v in dict2:
	idlist.append(int(k))
	catlist.append(v)

windl = int(sys.argv[2]) #length of sliding window
windinc = int(sys.argv[3]) #step of sliding window
writelist = []

print 'Constructing idlistcopy.... '
print '\n'
idlistcopy = []
for i in idlist:
	idlistcopy.append(i)

print 'Constructing idlist2.... '
print '\n'
idlist2 = []
removecnt = 0
for i in idlistcopy:
	while removecnt <= (len(idlistcopy) - 1):
		element = idlistcopy.pop(removecnt)
		idlist2.append(element)
		removecnt += (windinc-1)

lenidlist2 = len(idlist2) - 1
maxidlist2 = idlist2.pop(lenidlist2)
idlist2.append(maxidlist2)

print 'Constructing idlistdummy.... '
print '\n'
idlistdummy = set(range(maxidlist2 + 1))

idlistdummy.remove(0)
#idlistdummy is a list of integers from 1 to the maximum in idlist2

if windl >= len(idlistdummy):
	print "!Error! The Window Length is too great."
	print '\n'
	exit(1)

faillist = []

print 'Constructing faillist.... '
print '\n'
for i in idlistdummy:
	if not i in idlist:
		faillist.append(i)
	
#faillist contains the list of dummy ids not found in idlist2		
print 'Inserting no_data points.... '
print '\n'
for i in faillist:
	inserti = int(i) - 1
	catlist.insert(inserti, 'no_data')

print 'Initializing the sliding window function.... '
print '\n'
def window(seq, n=2):
	it = iter(seq)
	result = tuple(islice(it, n))
	if len(result) == n:
		yield result
	for elem in it:
		result = result[1:] + (elem,)
		yield result

for el in islice(window(catlist, n=windl),None,None,windinc):
	writelist.append(el)

fpout = open("t.txt", 'w')
fpout.write("POS\tABBA\tBABA\tABBB\tBABB\tother\tno_data")

#idlist2 = []
#removecnt = 0
#for i in idlist:
#	while removecnt <= (len(idlist) - 1):
#		element = idlist.pop(removecnt)
#		idlist2.append(element)
#		removecnt += (windinc-1)

print 'Constructing idlistdummy2.... '
print '\n'
idlistdummy2 = []
idlistdummy4 = sorted(list(idlistdummy))
removecnt = 0
for i in idlistdummy:
	while removecnt <= (len(idlistdummy4) - 1):
		element = idlistdummy4.pop(removecnt)
		idlistdummy2.append(element)
		removecnt += (windinc-1)

#idlistdummy2 contains the final writeable position numbers, with increment
print 'Constructing idlistdummy3.... '
print '\n'
idlistdummy3 = []
for el in idlistdummy2:
	idlistdummy3.append((el + (windl - 1)/2))
	
#idlistdummy3 contains the midpoint of the windows	
print 'Counting ABBA, BABBA, BABB.... '
print '\n'
for i in writelist:
	cnt = Counter()
	for word in i:
		cnt[word] += 1
	forwriteABBA = str(cnt['ABBA'])
	forwriteBABA = str(cnt['BABA'])
	forwriteABBB = str(cnt['ABBB'])
	forwriteBABB = str(cnt['BABB'])
	forwriteother = str(cnt['other'])
	forwriteno_data = str(cnt['no_data'])
	idwrite = idlistdummy3.pop(0)
	fpout.write('\n')
	fpout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idwrite, forwriteABBA, forwriteBABA, forwriteABBB, forwriteBABB, forwriteother, forwriteno_data))

fpout.close()

print 'Program duration', time.time() - start, 'seconds.'