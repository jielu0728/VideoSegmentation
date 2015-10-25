"""
detect logos

Usage:
  detect_logo <video> <logo> <xmin> <ymin> <xmax> <ymax> [--logo2=<l>] [--mask=<m>] [--scale=<scale>] [--shift=<shift>]
  detect_logo -h | --help
Options:
  --logo2=<l>                    second logo if possible
  --mask=<m>                     the mask
  --scale=<scale>                the scale for operation convertScaleAbs
  --shift=<shift>                the shift for operation convertScaleAbs
"""

import numpy as np
import cv, cv2
import json
import tools
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	video = arguments['<video>']
	logo = arguments['<logo>']
	logo2 = arguments['--logo2']
	mask = arguments['--mask']
	scale = int(arguments['--scale'])
	shift = int(arguments['--shift'])
	xmin = int(arguments['<xmin>'])
	ymin = int(arguments['<ymin>'])
	xmax = int(arguments['<xmax>'])
	ymax = int(arguments['<ymax>'])
	x = xmax-xmin
	y = ymax-ymin
	cap = cv.CaptureFromFile(video)
	width = int(cv.GetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_WIDTH))
	height = int(cv.GetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_HEIGHT))
	
	mask = cv.LoadImage(mask, iscolor=cv.CV_LOAD_IMAGE_GRAYSCALE)
	logo = cv2.imread(logo)
	hist_logo = tools.calcul_hist(logo, x, y, mask)
	logo2 = cv2.imread(logo2)
	logo2 = cv2.convertScaleAbs(logo2, alpha=scale, beta=shift)
	logo2 = np.asarray(logo2)
	hist_logo2 = tools.calcul_hist(logo2, x, y, mask)

	score = {}	
	c_frame = -1

	while(c_frame<(cv.GetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_COUNT)-1)):
	    print c_frame
	    frame = cv.QueryFrame(cap)
	    c_frame += 1
            if frame:

		    frame = frame[ymin:ymax, xmin:xmax]
		    if cv.WaitKey(1) & 0xFF == ord('q'):
			break
		    frame_a = np.asarray(frame)	
		    hist = tools.calcul_hist(frame_a, x, y, mask)
		    result = cv.CompareHist(hist_logo, hist, cv.CV_COMP_CORREL)
		    cv.ShowImage('frame',frame)

		    cv.ConvertScaleAbs(frame, frame, scale=scale, shift=shift)

		    frame_a = np.asarray(frame)
		    hist = tools.calcul_hist(frame_a, x, y, mask)
		    result2 = cv.CompareHist(hist_logo2, hist, cv.CV_COMP_CORREL)
	
		    score[c_frame] = [result , result2]
	    	    
	
	with open('/home/lujie/Bureau/'+video.split('/')[-1]+'.logo.json', 'w') as f:
	    json.dump(score, f, indent=4, sort_keys=True) 

	cv.DestroyAllWindows()
