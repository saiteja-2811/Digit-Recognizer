# -*- coding: utf-8 -*-
"""
@author: mahitha.sree
"""
#%%
from skimage.feature import hog
import numpy as np
import pickle
from PIL import Image as im
from PIL import ImageOps
import cv2
import glob


def predict_letter(iage):
    nn_3 = pickle.load(open('neuralapp_2.pkl', 'rb'))
    
    img = cv2.imread('canvas.jpg')
    img = cv2.copyMakeBorder(img,20,20,20,20,cv2.BORDER_CONSTANT,value=[255,255,255])
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,60,255,cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    c = list()
    for i in range(len(hierarchy[0,:,0])):
        if (hierarchy[0,i,3] != -1):
            c.append(i)
    for index in sorted(c, reverse=True):
        del contours[index]       
        
    h_list=[]
    for i in range(len(contours)):
        [x,y,w,h] = cv2.boundingRect(contours[i])
        h_list.append([x,y,w,h]) 
    
    ziped_list=zip(*h_list)
    x_list=list(ziped_list)[0]
    dic=dict(zip(x_list,h_list))
    x_list = list(x_list)
    x_list.sort()
    j=0
    for x in x_list:
        [x,y,w,h]=dic[x]
        im3=img[y:y+h,x:x+w]
        cv2.imwrite('pix'+str(j)+'.png',im3)
        j+=1
    
    onlyfiles = glob.glob("pix*.png")
    test_features = []
    
    for st in onlyfiles:
        image = im.open(st).convert("L")
        image = image.resize((28,28),im.ANTIALIAS)
        invert_im = ImageOps.invert(image)
        image =np.array(invert_im)
        image[image <= 60] = 0
        image[image > 60] = 255
        test_features.append(image)
    
    test_list_hog_fd = []
    for feature in test_features:
        fd = hog(feature, orientations=9, pixels_per_cell=(7,7), cells_per_block=(1, 1), visualise=False)
        test_list_hog_fd.append(fd)
        
    test_hog_features = np.array(test_list_hog_fd, 'float64')
    test_l = nn_3.predict(test_hog_features)
    #test_ll = [n for n in list(map(int,test_l[::,0]))]
    k = 0
    for x in x_list:
        loc = tuple(dic[x][0:2])
        cv2.putText(img,test_l[k,0],loc,cv2.FONT_HERSHEY_PLAIN,2,(255,16,16),2)
        k = k + 1
    cv2.imshow("img",img)
#%%
