"""
split

Usage:
  split <name>
  split -h | --help
"""

from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	name = arguments['<name>']
	f = open('TASR_QCOMPERE_Primary.ctm')
	fn = open('TASR_'+name+'.ctm','w')
	for line in f:
	    if name in line:
		fn.write(line)
	f.close()
	fn.close()
