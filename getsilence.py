"""
get all silences of a video

Usage:
  getsilence <mdtm>
  getsilence -h | --help
"""

from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	mdtm = arguments['<mdtm>']
	f = open(mdtm.split('.')[0]+'.sil', 'w')
	mdtm = open(mdtm,'r')
	start = 0.0
	last = 0.0
	for line in mdtm:
	    if start == 0.0:
		start = float(line.split(' ')[2])
		last = float(line.split(' ')[3])
	    else:
		if line.split(' ')[2] == start:
		    pass
	        elif float(line.split(' ')[2]) - float(start) - float(last) > 0.01:
		    a = float(start) + float(last)
		    b = float(line.split(' ')[2]) - float(start) - float(last)
		    f.write(str(a)+'        '+str(b)+'\n')
		start = float(line.split(' ')[2])
		last = float(line.split(' ')[3])
	f.close()
	mdtm.close()
