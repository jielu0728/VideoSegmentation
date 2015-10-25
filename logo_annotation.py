import numpy as np
import cv2, cv
import sys
import json

import tools

if __name__ == '__main__':
    p = tools.read_param(sys.argv)
    data_out = {'cut_manual':{'list':{}}}
    
    p, frame, capture, desired_frame, c_frame = tools.start_read_video(p)
    cv2.imshow('img',frame)        

    while (c_frame<p.end):        
        p, c_frame, frame, k = tools.player(p, c_frame, frame, capture)
        timestamp = capture.get(cv.CV_CAP_PROP_POS_MSEC)    
        if k == ord('a') :
            data_out['cut_manual']['list'][c_frame] = {'time':timestamp/1000, 'type':'1'}
        if k == ord('p') :
            data_out['cut_manual']['list'][c_frame] = {'time':timestamp/1000, 'type':'2'}
        if k == ord('u') :
            data_out['cut_manual']['list'][c_frame] = {'time':timestamp/1000, 'type':'0'}

        cv2.putText(frame, "frame: "+str(c_frame) ,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255,0,0),1,10)
        cv2.putText(frame, "step: "+str(p.step) ,(10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255,0,0),1,10)            
        cv2.imshow('img',frame)        
        
    with open(p.video+".cut_manu.json", 'w') as f:
        json.dump(data_out, f, indent=4, sort_keys=True)    

    capture.release()
    cv2.destroyAllWindows()	
