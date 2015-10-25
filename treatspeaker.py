"""
pick the highest score out of the file

Usage:
  treatspeaker <spk>
  treatspeaker -h | --help
"""


from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	spk = arguments['<spk>']
	f = open(spk.split('.')[0]+'_top.etf0', 'w')
	spk = open(spk,'r')
	for line in spk:
	    if 'top_score' in line:
		start = float(line.split(' ')[2])
		end = start + float(line.split(' ')[3])
		f.write(str(start)+' '+str(end)+' '+line.split(' ')[6]+'\n')
	
