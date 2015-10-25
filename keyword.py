#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
find the keywords in a video 
source: transcription (automatic)

Usage:
  keyword <ctm>
  keyword -h | --help
"""

from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	ctm = arguments['<ctm>']
	f = open(ctm.split('.')[0]+'.keya', 'w')
	ctm = open(ctm,'rb')

	keyword = [["à","suivre"], ["merci"], ["dans","l'","actualité","également"]]

	for obj in keyword:
	    t = 0
	    length = len(obj)
	    num = 0
	    mark = 0
	    for line in ctm:
		num = num + 1
		if line.split(' ')[4] == obj[t] and t == 0:
		    if length == 1:
			f.write(obj[t]+'           '+line.split(' ')[2]+'\n')
		    else:
		    	t = 1
		    	mark = num
		elif line.split(' ')[4] == obj[t] and t != 0 and num - mark == 1:
		    t = t + 1
		    mark = num
		    if t == length:
			for item in obj:
			    f.write("%s " % item)
			f.write('           '+line.split(' ')[2]+'\n')
			t = 0
		elif num - mark > 1:
		    t = 0
	    ctm.seek(0)

	f.close()
	ctm.close()

		
	    
