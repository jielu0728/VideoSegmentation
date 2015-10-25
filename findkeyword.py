#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
find the keywords in a video
source: transcription

Usage:
  findkeyword <trs>
  findkeyword -h | --help
"""

from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	trs = arguments['<trs>']
	f = open(trs.split('.')[0]+'.key', 'w')
	trs = open(trs,'rb')#.read().decode("iso-8859-1")

	keyword = ["à suivre".decode("utf8").encode("iso-8859-1"), "merci".decode("utf8").encode("iso-8859-1"), "dans l'actualité également".decode("utf8").encode("iso-8859-1")]

	time = 0.0
	keytime = []
	for line in trs:
	    if '<Sync time' in line:
		time = float(line.split('"')[1])
	    for kwd in keyword:
		if kwd in line:
		    keytime.append((kwd,time))
	for obj in keytime:
	    (fst, snd) = obj
	    f.write(fst+'          '+str(snd)+'\n')

	f.close()

