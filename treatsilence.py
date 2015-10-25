"""
pick the silence out of the file

Usage:
  treatsilence <spk>
  treatsilence -h | --help
"""

from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	spk = arguments['<spk>']
	f = open(spk.split('.')[0]+'_slience.etf0', 'w')
	spk = open(spk,'r')
	end = 0
	for line in spk:
	    start = float(line.split(' ')[0])
	    diff = start - end
	    if diff != 0.0:
		f.write(str(end)+' '+str(start)+' '+str(diff)+'\n')
	    end = float(line.split(' ')[1])

