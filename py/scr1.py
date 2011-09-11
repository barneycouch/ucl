import re
import sys

targfile = sys.argv[1] #provide the filename as an argument
infile = open(targfile, 'r') #open file to read

scaffid = []
pos = []
cat = []
#strip whitespace, append lists with the elements
for line in infile:
	line2 = line.replace("\n", "")
	scaffidi, posi, cati = line2.split()
	scaffid.append(scaffidi)
	pos.append(int(posi))
	cat.append(cati)

#print '\n'
#print scaffid #scaffid holds the scaffold id
#print '\n'
#print pos #pos holds the position
#print '\n'
print cat #cat holds the category
print cat.pop(11)

#count the frequency of the categories
#abbacnt = cat.count('ABBA')
#babacnt = cat.count('BABA')
#abbbcnt = cat.count('ABBB')
#babbcnt = cat.count('BABB')
#othercnt = cat.count('other')
#no_datacnt = cat.count('no_data')

windlength = 10 #length of sliding window
windinc = 1 #step of sliding window

for i in pos:
	fcount = []
	#region = int(i) + (windlength - 1)
	indi = pos.index(i)
	print i
	print indi
	print cat.pop(indi)
	#fcount.append(ref)
	abbacnt = fcount.count('ABBA')
	babacnt = fcount.count('BABA')
	abbbcnt = fcount.count('ABBB')
	babbcnt = fcount.count('BABB')
	othercnt = fcount.count('other')
	no_datacnt = fcount.count('no_data')
	
	i += windinc

	
	
