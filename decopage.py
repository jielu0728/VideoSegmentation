"""
decoupage de video en reportage

Usage:
  decoupage <src> <dst>
  decoupage -h | --help
"""

from docopt import docopt
import numpy as np
from sklearn.calibration import CalibratedClassifierCV

if __name__ == '__main__':
	arguments = docopt(__doc__)
	src = arguments['<src>']
	dst = arguments['<dst>']
	src = open(src,'r')
	dst = open(dst,'r')

	cut_time = []
	cut_silence = []
	cut_keyword = []
	cut_speaker = []
	cut_logo = []
	cut_time_n = []
	cut_silence_n = []
	cut_keyword_n = []
	cut_speaker_n = []
	cut_logo_n = []
	num = 0	

	X = []
	Y = []	

	for line in src:
	    if '*' in line:
		pass
	    else:
		#cut
		cut = line.split('\'')[9]
		cut = open(cut,'r')
		cut_time.append([])
		cut_time_n.append([])
		for l in cut:
		    if 'fin' in l:
			pass
		    else:
			cut_time[num].append(float(l.split('\t')[1]))
			start = int(l.split('\t')[0])
			end = int(l.split('\t')[1])
			if end - start > 30:
			    for i in range(start+10,end-10,3):
				cut_time_n[num].append(float(i))
		cut.close()

		#silence
		silence = line.split('\'')[1]
		silence = open(silence,'r')
		cut_silence.append([])
		cut_silence_n.append([])
		for obj in cut_time[num]:#positive
		    finish = 0
		    for l in silence:
			if obj-float(l.split('        ')[0]) > -1 and obj-float(l.split('        ')[0]) < float(l.split('        ')[1].split('\n')[0]) + 1:
			    cut_silence[num].append(1)
			    finish = 1
			    break
		    if finish == 0:
			cut_silence[num].append(0)
		    silence.seek(0)
		for obj in cut_time_n[num]:#negative
		    finish = 0
		    for l in silence:
			if obj-float(l.split('        ')[0]) > -1 and obj-float(l.split('        ')[0]) < float(l.split('        ')[1].split('\n')[0]) + 1:
			    cut_silence_n[num].append(1)
			    finish = 1
			    break
		    if finish == 0:
			cut_silence_n[num].append(0)
		    silence.seek(0)
		silence.close()
		
		#keyword
		keyword = line.split('\'')[3]
		keyword = open(keyword,'r')
		cut_keyword.append([])
		cut_keyword_n.append([])
		for obj in cut_time[num]:#positive
		    temp = []
		    for l in keyword:
			temp.append(abs(obj-float(l.split('          ')[1].split('\n')[0])))
		    cut_keyword[num].append(round(min(temp),3))
		    keyword.seek(0)
		for obj in cut_time_n[num]:#negative
		    temp = []
		    for l in keyword:
			temp.append(abs(obj-float(l.split('          ')[1].split('\n')[0])))
		    cut_keyword_n[num].append(round(min(temp),3))
		    keyword.seek(0)
		keyword.close()
			
		#speaker
		speaker = line.split('\'')[5]
		speaker = open(speaker,'r')
		cut_speaker.append([])
		cut_speaker_n.append([])
		for obj in cut_time[num]:#positive
		    temp = []
		    for l in speaker:
			if '.' in l and ',' in l:
			    temp.append(abs(obj-float(l.split('        ')[1].split(',')[0])))
			elif '.' in l:
			    temp.append(abs(obj-float(l.split('        ')[1].split('\n')[0])))
		    cut_speaker[num].append(round(min(temp),3))
		    speaker.seek(0)
		for obj in cut_time_n[num]:#negative
		    temp = []
		    for l in speaker:
			if '.' in l and ',' in l:
			    temp.append(abs(obj-float(l.split('        ')[1].split(',')[0])))
			elif '.' in l:
			    temp.append(abs(obj-float(l.split('        ')[1].split('\n')[0])))
		    cut_speaker_n[num].append(round(min(temp),3))
		    speaker.seek(0)
		speaker.close()
		
		#logo
		logo = line.split('\'')[7]
		logo = open(logo,'r')
		cut_logo.append([])
		cut_logo_n.append([])
		for obj in cut_time[num]:#positive
		    temp = []
		    for l in logo:
			if '.' in l:
			    temp.append(abs(obj-float(l.split(': ')[1].split(',')[0])))
		    cut_logo[num].append(round(min(temp),3))
		    logo.seek(0)
		for obj in cut_time_n[num]:#negative
		    temp = []
		    for l in logo:
			if '.' in l:
			    temp.append(abs(obj-float(l.split(': ')[1].split(',')[0])))
		    cut_logo_n[num].append(round(min(temp),3))
		    logo.seek(0)
		logo.close()


	        num = num + 1

	time = []
	silence = []
	keyword = []
	speaker = []
	logo = []
	for i in range(len(cut_time)):
	    time = time + cut_time[i]
	    silence = silence + cut_silence[i]
	    keyword = keyword + cut_keyword[i]
	    speaker = speaker + cut_speaker[i]
	    logo = logo + cut_logo[i]
	for i in range(len(time)):
	    temp = (silence[i],keyword[i],speaker[i],logo[i])
	    X.append(temp)
	    Y.append(1)
	time = []
	silence = []
	keyword = []
	speaker = []
	logo = []
	for i in range(len(cut_time_n)):
	    time = time + cut_time_n[i]
	    silence = silence + cut_silence_n[i]
	    keyword = keyword + cut_keyword_n[i]
	    speaker = speaker + cut_speaker_n[i]
	    logo = logo + cut_logo_n[i]
	for i in range(len(time)):
	    temp = (silence[i],keyword[i],speaker[i],logo[i])
	    X.append(temp)
	    Y.append(0)


	clf = CalibratedClassifierCV()
        clf.fit(X, Y)
	
	for line in dst:
	    if * in line:
		pass
	    else:
		

	
	print X
		
