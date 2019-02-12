#!/usr/bin/env python
# coding: utf-8

# In[1]:


from skimage.io import imread
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage import img_as_float
import math
from skimage.io import imsave
from os import listdir
from os.path import isfile, join
from skimage.transform import rescale
import time


# In[2]:


## Setting the input output file path
imageDir = '../Images/';
imageName = 'cathedral.jpg';
outDir = '../Results/';
onlyfiles = [f for f in listdir(imageDir) ]
print(onlyfiles)


# In[3]:

# method to saveImages
def saveImage(rgbImage, fileName):
    plt.imshow(rgbImage)
    # save the image into a folder
    imsave(outDir + fileName, rgbImage);
    
# circular shift implementaion
def circShift(image, i, j):
    return np.roll(image,[i,j], axis = (0,1))


# image cropping
def crop(image, margin=0.1):
    print('cropping image')
    height, width = image.shape
    y1, y2 = int(margin * height), int((1 - margin) * height)
    x1, x2 = int(margin * width), int((1 - margin) * width)
    return image[y1:y2, x1:x2]

## normalized cross-correlation
def normalized_crosscorrelation(image1, image2):
    product = np.sum((image1 - image1.mean()) * (image2 - image2.mean()))
    stds = np.sqrt((np.sum(np.power(image1-image1.mean(),2)))*(np.sum(np.power(image2-image2.mean(),2))))
    # stds = image1.std() * image2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product



# In[4]:

# get shift naive implementation
def getShift(im,ref, sf, xc=0,yc=0):
    maxCorr = float('-inf');
    max_x = 0
    max_y = 0
    for i in range(-sf+xc,sf+xc):
        for j in range(-sf+yc,sf+xc):
            img = circShift(im, i, j)
            ncc = normalized_crosscorrelation(img,ref);
            if ncc > maxCorr:
                maxCorr = ncc;
                max_x = i;
                max_y = j;
    print(maxCorr)
    return (max_x,max_y)


# In[5]:

# get Shift pyramid approach with recursion top-down implementation
def getShiftPyramid(im,ref):
    if(im.shape[0] < 400 and im.shape[1] < 400):
        return getShift(im,ref,15)
    
    im_rescale = rescale(im, 1.0 / 2.0)
    ref_rescale = rescale(ref, 1.0/ 2.0)
    
    tmp_disp_x ,tmp_disp_y = getShiftPyramid(im_rescale, ref_rescale)
    return getShift(im,ref,1,2*tmp_disp_x,2*tmp_disp_y)
    


# In[6]:

# get shift pyramid approach with recursion bottom-up implementation
def getShiftPyramidIterative(im, ref):
    l = max(im.shape)
    level = max(2**(math.ceil(math.log2(l/400.0))), 1)
    sp = 15
    xc =0
    yc =0
    while(level >= 1):
        im_resize = rescale(im, 1.0/level)
        ref_resize = rescale(ref, 1.0/level)
        disp_x, disp_y = getShift(im_resize, ref_resize, sp,xc, yc)
        xc = 2*disp_x
        yc = 2*disp_y
        level = level/2
        sp = 1
    return disp_x, disp_y  


# In[7]:

# align single image and save the output
# replace the getShitPyramid with getShift or getShiftPyramidIterative for different approaches
def getRGBImage(imageDir, filename):
    image = cv2.imread(imageDir + filename,0)
    image = img_as_float(image)
    
    imageheight = math.floor(image.shape[0]/3)
    b = image[0:imageheight]
    g =  image[imageheight: 2*imageheight]
    r = image[2*imageheight: 3*imageheight]
    startTime = time.time()
    b = crop(b)
    g = crop(g)
    r = crop(r)
    
    x_bg,y_bg = getShiftPyramid(g,b)
    x_br,y_br = getShiftPyramid(r,b)
    endTime = time.time()
    print(filename)
    print("blue-green disp :" , " x: " , x_bg, " y: ", y_bg)
    print("blue-red disp :" , " x: " , x_br, " y: ", y_br)
    print('Time(sec): ',endTime - startTime)
    print('\n')
    #rolling
    g = np.roll(g, x_bg, axis=0)
    g = np.roll(g, y_bg, axis=1)

    r = np.roll(r, x_br, axis=0)
    r = np.roll(r, y_br, axis=1)
    
    # create a color image
    im_out = np.dstack([r, g, b])
    # save the image
    fname = outDir + filename.split('.')[0] + '.jpg'
    imsave(fname, im_out)


# In[9]:


# running the shift for all the images
for file in onlyfiles: 
    getRGBImage(imageDir,file)
    


# In[ ]:




