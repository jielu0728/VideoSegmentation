"""
detect logos

Usage:
  detect_contours <video> <logo> [--logo2=<l>] <xmin> <ymin> <xmax> <ymax> 
  detect_contours -h | --help

"""


import numpy as np
import cv, cv2
import json
import tools
from docopt import docopt
from pylab import array, uint8


if __name__ == '__main__':
	arguments = docopt(__doc__)
	video = arguments['<video>']
	logo = arguments['<logo>']
	logo2 = arguments['--logo2']
	xmin = int(arguments['<xmin>'])
	ymin = int(arguments['<ymin>'])
	xmax = int(arguments['<xmax>'])
	ymax = int(arguments['<ymax>'])
	x = xmax-xmin
	y = ymax-ymin
	cap = cv.CaptureFromFile(video)
	score = {}	
	c_frame = -1

	maxIntensity = 255.0
	phi = 1
	theta = 1
	
	contours = cv2.imread(logo)
	hist_logo = tools.calcul_hist(contours, x*4, y*4, None)
	contours2 = cv2.imread(logo2)
	hist_logo2 = tools.calcul_hist(contours2, x*4, y*4, None)


	while(c_frame<(cv.GetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_COUNT)-1)):
	    frame = cv.QueryFrame(cap)
	    c_frame += 1
            if frame:
		frame = frame[ymin:ymax, xmin:xmax]
		frame_a = np.asarray(frame)
		frame_a = cv2.resize(frame_a, (0,0), fx=4, fy=4) 
		if cv.WaitKey(1) & 0xFF == ord('q'):
	            break
		newImage0 = (maxIntensity/phi)*(frame_a/(maxIntensity/theta))**2
		newImage0 = array(newImage0,dtype=uint8)
		gray2 = cv2.cvtColor(newImage0,cv2.COLOR_BGR2GRAY)
		ret2, binary2 = cv2.threshold(gray2,127,255,0)
		contour2, hierarchy2 = cv2.findContours(binary2, 2, 1)
		img = np.zeros(frame_a.shape, np.uint8)
		cv2.drawContours(img, contour2, -1, (0,255,0), 3)
		hist_img = tools.calcul_hist(img, x*4, y*4, None)
		res1 = cv.CompareHist(hist_logo, hist_img, cv.CV_COMP_CHISQR)
		res2 = cv.CompareHist(hist_logo2, hist_img, cv.CV_COMP_CHISQR)
		print c_frame
		cv2.imshow("img", img)
		score[c_frame] = [res1, res2]

	    	    
	
	with open('/home/lujie/'+video.split('/')[-1]+'_contours.logo.json', 'w') as f:
	    json.dump(score, f, indent=4, sort_keys=True) 

