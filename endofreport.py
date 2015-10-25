"""
get all ends of reports in a video
source: spk_seg transcription

Usage:
  endofreport <mdtm> <trs>
  endofreport -h | --help
"""

from docopt import docopt
import json

if __name__ == '__main__':
	arguments = docopt(__doc__)
	mdtm = arguments['<mdtm>']
	trs = arguments['<trs>']
	f = open(mdtm.split('.')[0]+'.eor', 'w')
	mdtm = open(mdtm,'r')
	trs = open(trs,'r')
	journalist = []
	traited = []
	start = 0.0
	last = 0.0
	end = 0.0
	time = {}
	for line in trs:
	    if 'accent="R3"' in line:
		journalist.append(line.split(' ')[2].split('"')[1])
	for l in mdtm:
	    if l.split(' ')[7].split('\n')[0] in journalist:
	        if l.split(' ')[7].split('\n')[0] not in traited:
		    start = float(l.split(' ')[2])
		    last = float(l.split(' ')[3])
		    end = round(start + last,3)
		    name = l.split(' ')[7].split('\n')[0]
		    time[name] = [end]
		    traited.append(name)
	        elif l.split(' ')[7].split('\n')[0] in traited:
		    start = float(l.split(' ')[2])
		    last = float(l.split(' ')[3])
		    end = round(start + last,3)
		    name = l.split(' ')[7].split('\n')[0]
		    if start - max(time[name]) > 150:
		        time[name].append(end)
		    else:
		        time[name].pop()
		        time[name].append(end)
	json.dump(time, f, indent=4, sort_keys=True)
	f.close()
	mdtm.close()
	trs.close()

