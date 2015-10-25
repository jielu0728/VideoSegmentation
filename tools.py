import numpy as np
import cv2, cv
import os, sys, getopt, glob
import itertools 



class PARAM:
    def __init__(self):
        self.video = 'BFMTV_BFMStory_2012-11-15_175800.MPG'
        self.start = 0
        self.end = -1
        self.seek_nb=''
        self.play = True
        self.step = 1
        self.delay = 40
        self.complete = False
        self.threshold_cut_hist = 0.7
        self.threshold_cut_OF = 0.7        
        self.scaleFactor = 1.1          #scaleFactor - Parameter specifying how much the image size is reduced at each image scale. Basically the scale factor is used to create your scale pyramid. More explanation can be found here. 1.05 is a good possible value for this, which means you use a small step for resizing, i.e. reduce size by 5%, you increase the chance of a matching size with the model for detection is found.
        self.minNeighbors = 10          #minNeighbors - Parameter specifying how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces. Higher value results in less detections but with higher quality. 3~6 is a good value for it.
        self.threshold_OF = 0.3       

class ROI:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.area = float((ymax-ymin) * (xmax-xmin))

        
def usage():
    print "-v --video       video path"

def read_param(argv):
    p = PARAM()
    try:                                
        opts, args = getopt.getopt(argv[1:], "v:s:e:c:t:c:f:m:o:", ['video=', 'start=', 'end=', 'complete=', 'threshold_cut_hist=', 'threshold_cut_OF=', 'scaleFactor=', 'minNeighbors=', 'threshold_OF=']) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2) 
    for opt, arg in opts:                
        if opt in ("-v", "--video"):      
            p.video =  arg
        if opt in ("-s", "--start"):      
            p.start =  int(arg)
        if opt in ("-e", "--end"):      
            p.end =  int(arg)    
        if opt in ("-c", "--complete"):      
            p.complete =  float(arg)            
        if opt in ("-t", "--threshold_cut_hist"):      
            p.threshold_cut_hist =  float(arg)
        if opt in ("-c", "--threshold_cut_OF"):      
            p.threshold_cut_OF =  float(arg)            
        if opt in ("-f", "--scaleFactor"):      
            p.scaleFactor =  float(arg)
        if opt in ("-m", "--minNeighbors"):      
            p.minNeighbors =  int(arg)     
        if opt in ("-m", "--minNeighbors"):      
            p.minNeighbors =  int(arg)  
    return p
    
def seek_to_frame(c_frame, desired_frame, capture):
    if c_frame>desired_frame:
        capture.set(cv.CV_CAP_PROP_POS_FRAMES, desired_frame-10)
    ret, frame = capture.read()
    c_frame = int(capture.get(cv.CV_CAP_PROP_POS_FRAMES))
    while (c_frame<desired_frame):
        ret, frame = capture.read()
        c_frame = int(capture.get(cv.CV_CAP_PROP_POS_FRAMES))
    return c_frame, frame

def start_read_video(p):
    capture = cv2.VideoCapture(p.video)
    nb_frame = int(capture.get(cv.CV_CAP_PROP_FRAME_COUNT)-1)
    if p.end == -1:
        p.end = nb_frame
    if p.end > nb_frame:
        p.end = nb_frame     
    c_frame = capture.get(cv.CV_CAP_PROP_POS_FRAMES)    
    c_frame, frame = seek_to_frame(c_frame, p.start, capture)
    desired_frame = c_frame
    return p, frame, capture, desired_frame, c_frame

def read_face_detection_file(p, ext):
    dic_face = {} 
    dic_cluster = {}
    for i in range(p.start, p.end+1):
        dic_face.setdefault(i, {})
    i_face = 0
    for line in open(p.video+ext):
        l = line[:-1].split(' ')
        frame =int(l[0])
        if frame in dic_face:
            nb_face = int(l[2])
            for face in range(nb_face):
                c,x,y,w,h = map(int, l[3+5*face:8+5*face])       
                dic_face[frame][i_face] = ROI(x, y, x+w, y+h)
                dic_cluster[i_face] = i_face
                i_face+=1
    return dic_face, dic_cluster

def read_existing_annotation_file(video, end):
    last_annotation_file=""
    last_nb = 0
    for file in glob.glob(video+".face_manu_*"):
        nb = int(file.split('_')[-1])
        if nb > last_nb:
            last_annotation_file = file
            last_nb = nb

    current_annotation = {}
    if last_nb != 0:
        for line in open(last_annotation_file):
            l = line[:-1].split()
            frame = int(l[0])
            nb_face = int(l[1])
            if nb_face != 0 :
                for face in range(nb_face):
                    c,x,y = map(int, l[2+3*face:5+3*face])  
                    current_annotation.setdefault(frame, set([])).add((x,y))
    return current_annotation, last_nb

def read_cut_annotation(p):
    dic_cut = {}
    for line in open(p.video+'.cut_'+str(p.threshold_cut)):
        frame, timestamp, value = line[:-1].split(' ')
        dic_cut[int(float(frame))] = float(value)    
    return dic_cut

def player(p, c_frame, frame, capture):
    k = cv2.waitKey(p.delay) & 0xff
    if k>=ord('0') and k<=ord('9'):
        p.seek_nb+=str(chr(k))
    if k == 10 and p.seek_nb != '': #10: enter
        print 'seek to', p.seek_nb
        c_frame, frame=seek_to_frame(c_frame, int(p.seek_nb), capture)
        p.seek_nb = ''
    if k == 84: #  84: down arrow   
        p.step+=1
    if k == 82: # 82: up arrow
        p.step-=1
    if k == 32 and not p.play: # 32: space
        p.play = True
    elif k == 32 and p.play: # 32: space
        p.play = False
    if k == 83:  #  83: right arrow        
        c_frame, frame=seek_to_frame(c_frame, int(c_frame-p.step), capture)    
    if p.play or k == 81: # 81: left arrow
        c_frame, frame=seek_to_frame(c_frame, int(c_frame+p.step), capture)      
    if k == 27: # 27: esc
        c_frame = p.end        
    return p, c_frame, frame, k
    
    
def calcul_hist(src_np, width, height, m):    
    src = cv.CreateImageHeader((src_np.shape[1], src_np.shape[0]), cv.IPL_DEPTH_8U, 3)
    cv.SetData(src, src_np.tostring(), src_np.dtype.itemsize * 3 * src_np.shape[1])
    hsv = cv.CreateImage((width, height), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
    
    h_plane = cv.CreateMat(height, width, cv.CV_8UC1)
    s_plane = cv.CreateMat(height, width, cv.CV_8UC1)
    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]    
    
    h_bins = 30
    s_bins = 32
    hist_size = [h_bins, s_bins]    
    h_ranges = [0, 180]

    s_ranges = [0, 255]
    ranges = [h_ranges, s_ranges]
    scale = 10
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)    
    
    cv.CalcHist([cv.GetImage(i) for i in planes], hist, mask = m)
    return hist    


def score_coverage_ROI(ROI1, ROI2):
    width = min(ROI1.xmax, ROI2.xmax)-max(ROI1.xmin, ROI2.xmin)
    height = min(ROI1.ymax, ROI2.ymax)-max(ROI1.ymin, ROI2.ymin)
    if width < 0 or height < 0:
        return 0.0
    area_intersection = width * height
    area_union = ROI1.area + ROI2.area - area_intersection
    return float(area_intersection) / area_union

def score_OF(roi, frame1, frame0, lk_params, feature_params):
    img0 = cv2.cvtColor(frame0[roi.ymin:roi.ymax, roi.xmin:roi.xmax], cv2.COLOR_BGR2GRAY)
    img1 = cv2.cvtColor(frame1[roi.ymin:roi.ymax, roi.xmin:roi.xmax], cv2.COLOR_BGR2GRAY)

    p0 = cv2.goodFeaturesToTrack(img0, mask = None, **feature_params)    
    p1 = cv2.goodFeaturesToTrack(img1, mask = None, **feature_params)    
    if p0 is None or  p1 is None:
        return -1.0, 0.0, 0.0, 0.0, 0.0
    
    p1_0, st1_0, err1_0 = cv2.calcOpticalFlowPyrLK(img0, img1, p0, p1, **lk_params)
    p0_1, st0_1, err0_1 = cv2.calcOpticalFlowPyrLK(img1, img0, p1, p0, **lk_params)
    
    nb_c_p0=0.0
    nb_p0=0.0
    nb_c_p1=0.0
    nb_p1=0.0
    move_x = 0.0
    move_y = 0.0

    for pts0, pts1, s in itertools.izip(p0, p1_0, st1_0):
        nb_p0+=1
        if s[0] == 1:
            nb_c_p0+=1
            move_x+=(pts1[0][0]-pts0[0][0])
            move_y+=(pts1[0][1]-pts0[0][1])
    if nb_c_p0>0:
        move_x=int(round(move_x/nb_c_p0,0))
        move_y=int(round(move_y/nb_c_p0,0))
    
    for pts0, pts1, s in itertools.izip(p1, p0_1, st0_1):
        nb_p1+=1
        if s[0] == 1:
            nb_c_p1+=1

    return (nb_c_p0/nb_p0+nb_c_p1/nb_p1)/2, nb_p0, nb_p1, move_x, move_y
    
