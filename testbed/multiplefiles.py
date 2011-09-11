import os, sys
txtfolder = sys.argv[1]
print txtfolder
if len(sys.argv) != 2:
	print 'PLEASE PROVIDE A FILEPATH!'

files = os.listdir(txtfolder)

print '\n'
print files
print '\n'

######

fullist = []
slash = '/'
for i in files:
	if "txt" in i:
		path = txtfolder
		filename = i
		full = path + slash + filename
		fullist.append(full)

print fullist

######

for el in fullist:
	fileopen = open(el, 'r')
	for line in fileopen:
		print line
		
