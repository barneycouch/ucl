fileopen = 'shortncp'
with open(fileopen) as f:
	for i, l in enumerate(f):
		pass
linecnt = (i + 1)
print linecnt
startdecrease = 5000 #distance from end to start decreasing window length
windmin = 500 #minimum window length
decreaseinc = 500 #amount to decrease the window size by every time
windl = 10000
windinc = 1000

#SOME PSEUDOCODE:
while windl >= windmin:
	print windl
	print 'still decreasing'
	windl -= decreaseinc