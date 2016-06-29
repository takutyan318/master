#! /usr/bin/env python
# coding: utf-8

#ヒストグラム化(平均化)


import cv
import cv2
import numpy as np
import pylab as plt


#フロント
#全てのサンプルのヒストグラムをhist_fに格納
hist_f = []
for i in range(1,546):
	img = cv2.imread('../image/sample' + str(i) + '_front.jpeg', 0)
	hist = img.ravel()
	hist_f.append(hist)
#全てのヒストグラムの平均を求める
hist_f_avr = []  #平均化されたhist
pxelNum = len(hist_f[0]) #画素数
print pxelNum
for i in range(pxelNum):
	summ = 0
	for j in hist_f:
		summ += j[i]
	hist_f_avr.append(summ/545)
plt.subplot(2,2,1)
plt.hist(hist_f_avr, 256, [0,256])
plt.xlim([-10,256])
plt.ylim([0,1000])
plt.title(u'フロント')
#plt.show()


#サイド
#全てのサンプルのヒストグラムをhist_sに格納
hist_s = []
for i in range(1,546):
	img = cv2.imread('../image/sample' + str(i) + '_side.jpeg', 0)
	hist = img.ravel()
	hist_s.append(hist)
#全てのヒストグラムの平均を求める
hist_s_avr = []  #平均化されたhist
pxelNum = len(hist_s[0]) #画素数
print pxelNum
for i in range(pxelNum):
	summ = 0
	for j in hist_s:
		summ += j[i]
	hist_s_avr.append(summ/545)
plt.subplot(2,2,2)
plt.hist(hist_f_avr, 256, [0,256])
plt.xlim([-10,256])
plt.ylim([0,1000])
plt.title(u'サイド')
#plt.show()


#バック
#全てのサンプルのヒストグラムをhist_fに格納
hist_b = []
for i in range(1,546):
	img = cv2.imread('../image/sample' + str(i) + '_back.jpeg', 0)
	hist = img.ravel()
	hist_b.append(hist)
#全てのヒストグラムの平均を求める
hist_b_avr = []  #平均化されたhist
pxelNum = len(hist_b[0]) #画素数
print pxelNum
for i in range(pxelNum):
	summ = 0
	for j in hist_b:
		summ += j[i]
	hist_b_avr.append(summ/545)
plt.subplot(2,2,3)
plt.hist(hist_b_avr, 256, [0,256])
plt.xlim([-10,256])
plt.ylim([0,1000])
plt.title(u'バック')
plt.show()