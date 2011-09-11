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

print 'ABBA - %g, BABA - %g, ABBB - %g, BABB - %g, Other - %g, No Data - %g' % (abbacnt, babacnt, abbbcnt, babbcnt, othercnt, no_datacnt)

windl = 10 #length of sliding window
windi = 1 #step of sliding window

for pos, cat in dict1.items():	
	print cat

