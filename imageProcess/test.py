#! /usr/bin/env python
# coding: utf-8

#いろいろなテスト用

import cv2
import numpy as np


if __name__ == '__main__':
	img = cv2.imread('../image/sample227_front.jpeg', 0)
	height1 = img.shape[0]
	width1 = img.shape[1]
	img_large = cv2.resize(img,(2*height1, 2*width1))
	height2 = img_large.shape[0]
	width2 = img_large.shape[1]

	count1 = 0
	for i in range(height1):
		for j in range(width1):
			if img[i][j] < 10:
				count1 += 1
	print 'hair region in normal image is ' + str(count1)

	count2 = 0
	for i in range(height2):
		for j in range(width2):
			if img_large[i][j] < 10:
				count2 += 1
	print 'hair region in large image is ' + str(count2)

	print ''
	print count2 / count1
