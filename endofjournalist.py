"""
pick the highest score out of the file

Usage:
  endofjournalist <spk> <jnl>
  endofjournalist -h | --help
"""

from docopt import docopt
import json

if __name__ == '__main__':
	arguments = docopt(__doc__)
	spk = arguments['<spk>']
	jnl = arguments['<jnl>']
	f = open(spk.split('.')[0]+'_journalist.etf0', 'w')
	spk = open(spk,'r')
	jnl = open(jnl,'r')
	journalist = []
	presenter = []
	eoj = {}
	start = 0
	for l in jnl:
	    presenter.append(l.split('\n')[0])

	for line in spk:
	    if start == 0:
	        speaker = line.split(' ')[2].split('\n')[0]
		start = float(line.split(' ')[0])
	        end = float(line.split(' ')[1])
		start = 1
	    elif line.split(' ')[2].split('\n')[0] in presenter:
		if speaker not in journalist and speaker not in presenter:
		    journalist.append(speaker)
		    eoj[speaker] = [end]
		    speaker = line.split(' ')[2].split('\n')[0]
		    start = float(line.split(' ')[0])
		    end = float(line.split(' ')[1])
		elif speaker in journalist and speaker not in presenter:
		    if eoj[speaker]!=[]:
		        lastend = max(eoj[speaker])
		        if start-lastend >= 150:
		    	    eoj[speaker].append(end)
		        else:
			    eoj[speaker].pop()
			    eoj[speaker].append(end)
		    elif eoj[speaker]==[]:
			eoj[speaker].append(end)
		    speaker = line.split(' ')[2].split('\n')[0]
		    start = float(line.split(' ')[0])
		    end = float(line.split(' ')[1])
	    elif line.split(' ')[2].split('\n')[0] not in presenter:
		    if speaker in journalist and speaker not in presenter:
			if eoj[speaker]!=[]:
		    	    lastend = max(eoj[speaker])
		            if start-lastend <= 150:
			        eoj[speaker].pop()
		    speaker = line.split(' ')[2].split('\n')[0]
		    start = float(line.split(' ')[0])
	            end = float(line.split(' ')[1])

	
	json.dump(eoj, f, indent=4, sort_keys=True)
	f.close()
	jnl.close()
	spk.close()
