import time
start = time.time()
import re, sys
from collections import Counter
from itertools import islice

if len(sys.argv) != 6:
	print "!Input Error! Need <source file>  <window length>  <window increment> <decreasing window increment> <minimum window size> arguments."
	exit(1)

targfile = sys.argv[1] #provide the filename as an argument
infile = open(targfile, 'r') #open file to read

#############	COUNTING TOTAL ABBA/BABBA, CONSTRUCTING LISTS/DICTS OF ALL 3 VALUES    #############

dict1 = {}
scafflist = []
linecnt = 0
#strip whitespace, append lists and dicts with the elements
for line in infile:
	line2 = line.replace("\n", "")
	scaffidi, posi, cati = line2.split()
	scafflist.append(scaffidi)
	dict1[posi] = cati
	linecnt += 1

#scafflist contains an ordered list of scaffold ids	
#dict1 contains UNORDERED positions and category pairs:
#k = position (eg 1, 2, 3, 4 etc.)
#v = category (eg ABBA, BABA, no_data)

el = []
for k, v in dict1.items():
	el.append(v)
	
#list el is a list of all the categories for counting

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

#############	SORTING THE DICTIONARY, MAKING A LIST OF IDS AND CATEGORIES   #############

#a short complicated function to sort a dictionary - dict used to provide amazing speed!

def asint(s):
	try: return int(s), ''
	except ValueError: return sys.maxint, s
	
dict2 = [(k, dict1[k]) for k in sorted(dict1, key=asint)]

#dict2 is sorted by k/position so a list can be created. Looks a bit like {1}:(ABBA),{2}:(other),{3}:(no_data) etc.

catlist = []
idlistforhash = []
print 'Constructing idlisthash, catlist.... '
print '\n'
for k, v in dict2:
	idlistforhash.append(int(k))
	catlist.append(v)

#idlistforhash is a list of the positions in the file that are increasing, eg. 1,2,3,5,6,7,8....	
#catlist is a list of categories ordered by increasing position, eg. ABBA, BABB, no_data.... 
	
idlisthash = set(idlistforhash)
#idlisthash is a hashed version (and thus a lot faster) of idlistforhash!	

print 'Constructing idlistcopy.... '
print '\n'
idlistcopy = sorted(list(idlisthash))
#idlistcopy is an unhashed version of idlisthash, sorted correctly

#############	INITIALIZE SLIDING WINDOW VARIABLES, NOT DOING THE SLIDE YET   #############

windl = int(sys.argv[2]) #length of sliding window
windinc = int(sys.argv[3]) #step of sliding window
writelist = []

#############	CONSTRUCT A DUMMY LIST OF IDS AND INSERT NO_DATAS, CHECK FOR SILLY ERRORS   #############

maxidlistforhash = idlistforhash[-1]

#get the maximum id

print 'Constructing idlistdummyhash.... '
print '\n'
idlistdummyhash = set(range(maxidlistforhash + 1))

idlistdummyhash.remove(0) #take out 0, duh.
#idlistdummyhash is a list of integers from 1 to the maximum in idlistforhash

if windl >= len(idlistdummyhash):
	print "!Error! The Window Length is too great."
	print '\n'
	exit(1)

#make sure the window length is not larger than the list - this is unlikely!

faillist = []

print 'Constructing faillist.... '
print '\n'
for i in idlistdummyhash:
	if not i in idlisthash:
		faillist.append(i)
				
		
faillist.sort()	
#faillist contains the list of dummy ids not found in idlistforhash	

print 'Inserting no_data points.... '
print '\n'
for i in faillist:
	inserti = int(i) - 1
	catlist.insert(inserti, 'no_data')
	
#where there is no data, insert a "no_data" string in the category list	


######

print 'catlist: '
print catlist

startdecrease = len(catlist) - windl #at this index of catlist, start to decrease window size
windmin = int(sys.argv[5]) #minimum window length
decreaseinc = int(sys.argv[4]) #amount to decrease the window size by every time
windpos = 0 

######

#############	TIME TO START SLIDING   #############

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

##############
print 'windpos'
print windpos
print 'startdecrease'
print startdecrease
print '\n'

#an end-tied subset of catlist:
windlneg = windl*-1
catlistsubset = catlist[windlneg:]
print 'catlistsubset'
print catlistsubset

windl2 = len(catlistsubset)
pos2 = 0

endlist = []
print 'shorter slices'
while windl2 >= windmin:
	endlist.append(catlistsubset[pos2:len(catlistsubset)])
	pos2 += decreaseinc
	windl2 -= decreaseinc

print 'endlist:'
print endlist
print '\n'

##############

for el in islice(window(catlist,windl),None,None,windinc):
	writelist.append(el)


#writelist contains a tuplified list of categories
#endlist contains the windowlength-decreasing subset that will go on the....end.

fpout = open("scr14out.txt", 'w')
fpout.write("START\tMID\tABBA\tBABA\tABBB\tBABB\tother\tno_data")


#############	GET THE FINAL WRITEABLE LISTS   #############


print 'Constructing idlistdummy2.... '
print '\n'
idlistdummy2 = []
idlistdummy = sorted(list(idlistdummyhash))
#idlistdummy is a list version of idlistdummyhash
removecnt = 0
for i in idlistdummyhash:
	while removecnt <= (len(idlistdummy) - 1):
		element = idlistdummy.pop(removecnt)
		idlistdummy2.append(element)
		removecnt += (windinc-1)

#idlistdummy2 contains the final writeable position numbers, with increment
#can't use idlistdummy, that's been pop'ed to nonexistence.

print 'Constructing idlistdummy3.... '
print '\n'
idlistdummy3 = []
for el in idlistdummy2:
	idlistdummy3.append((el + (windl - 1)/2))
	
#idlistdummy3 contains the midpoint of the windows, Kanchon-style.

print 'writelist: '
print writelist
print '\n'


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
	idwritestart = idlistdummy2.pop(0)
	idwritemid = idlistdummy3.pop(0)
	fpout.write('\n')
	fpout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idwritestart, idwritemid, forwriteABBA, forwriteBABA, forwriteABBB, forwriteBABB, forwriteother, forwriteno_data))

fpout.write('\n')

#############	CONSTRUCTING IDS FOR THE END (DECREASING) SEQUENCE   #############

rawpos = startdecrease #the start of the window, from where it starts to decrease
idlistendstart = []
idlistendmid = []

while rawpos < len(catlist) - 1:
	idlistendstart.append(rawpos + 1)
	rawpos += decreaseinc

print 'idlistendstart'
print idlistendstart

for i in idlistendstart:
	idlistendmid.append((i + (windl - 1)/2))
	windl -= decreaseinc
	
#############


for el in endlist:
	cnt = Counter()
	for word in el:
		cnt[word] += 1
	forwriteABBA = str(cnt['ABBA'])
	forwriteBABA = str(cnt['BABA'])
	forwriteABBB = str(cnt['ABBB'])
	forwriteBABB = str(cnt['BABB'])
	forwriteother = str(cnt['other'])
	forwriteno_data = str(cnt['no_data'])
	idlistendstartwrite = idlistendstart.pop(0)
	idlistendmidwrite = idlistendmid.pop(0)
	fpout.write('\n')
	fpout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idlistendstartwrite, idlistendmidwrite, forwriteABBA, forwriteBABA, forwriteABBB, forwriteBABB, forwriteother, forwriteno_data))


print 'Program duration', time.time() - start, 'seconds.'