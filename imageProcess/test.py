#! /usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

img = cv2.imread('/Users/takuya/ihairsystem/imageProcess/synthesis/result/base2/hairSyn18_front.jpeg')
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
h = img.shape[0]
w = img.shape[1]
for i in range(h):
	for j in range(w):
		if (img_gray[i,j]>=120) and (img_gray[i,j]<=160):
			img[i,j] = [255,0,0]
while (True):
	cv2.imshow('test', img)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
cv2.destroyAllWindows()



