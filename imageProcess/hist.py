#! /usr/bin/env python
# coding: utf-8

#ヒストグラム化(平均化)


import cv
import cv2
import numpy as np
import pylab as plt
import pramToSample


#全てのサンプルのヒストグラム平均化
def hist_average():
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

#一つのサンプルに対するヒストグラム
def hist_one(sampleNum):
	fn_f = '../image/sample' + sampleNum + '_front.jpeg'
	fn_s = '../image/sample' + sampleNum + '_side.jpeg'
	fn_b = '../image/sample' + sampleNum + '_back.jpeg'
	im_f = cv2.imread(fn_f, 0)
	im_s = cv2.imread(fn_s, 0)
	im_b = cv2.imread(fn_b, 0)
	hist_f = im_f.ravel()
	hist_s = im_s.ravel()
	hist_b = im_b.ravel()

	plt.subplot(2,2,1)
	plt.hist(hist_f, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title(str(sampleNum) + '_' + u'フロント')

	plt.subplot(2,2,2)
	plt.hist(hist_s, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title(str(sampleNum) + '_' + u'サイド')

	plt.subplot(2,2,3)
	plt.hist(hist_b, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title(str(sampleNum) + '_' + u'バック')

	plt.show()

#グループごとのヒストグラム(プロント)平均化
#groupNum:平均化を行う髪の長さ(1~4)
def hist_groupAverage_f(groupNum):
	#フロント
	#指定のサンプルのヒストグラムをhist_fに格納
	hist_f = []
	serchParameter = 4   
	serchValue = groupNum

	hist_sample = pramToSample.paraToSample(serchParameter, serchValue)
	for i in hist_sample:
		img = cv2.imread('../image/sample' + str(i) + '_front.jpeg', 0)
		hist = img.ravel()
		hist_f.append(hist)
	#全てのヒストグラムの平均を求める
	hist_f_avr = []  #平均化されたhist
	pxelNum = len(hist_f[0]) #画素数
	sampleNum = len(hist_sample) #平均化するサンプルの数
	for i in range(pxelNum):
		summ = 0
		for j in hist_f:
			summ += j[i]
		hist_f_avr.append(summ/sampleNum)
	
	return hist_f_avr

#グループごとのヒストグラム(サイド)平均化
#groupNum:平均化を行う髪の長さ(1~4)
def hist_groupAverage_s(groupNum):
	#サイド
	#全てのサンプルのヒストグラムをhist_sに格納
	hist_s = []
	serchParameter = 5
	serchValue = groupNum

	hist_sample = pramToSample.paraToSample(serchParameter, serchValue)
	for i in hist_sample:
		img = cv2.imread('../image/sample' + str(i) + '_side.jpeg', 0)
		hist = img.ravel()
		hist_s.append(hist)
	#全てのヒストグラムの平均を求める
	hist_s_avr = []  #平均化されたhist
	pxelNum = len(hist_s[0]) #画素数
	sampleNum = len(hist_sample) #平均化するサンプルの数
	for i in range(pxelNum):
		summ = 0
		for j in hist_s:
			summ += j[i]
		hist_s_avr.append(summ/sampleNum)
	
	return hist_s_avr

#グループごとのヒストグラム(バック)平均化
#groupNum:平均化を行う髪の長さ(1~4)
def hist_groupAverage_b(groupNum):
	#バック
	#全てのサンプルのヒストグラムをhist_fに格納
	hist_b = []
	serchParameter = 6
	serchValue = groupNum

	hist_sample = pramToSample.paraToSample(serchParameter, serchValue)
	for i in hist_sample:
		img = cv2.imread('../image/sample' + str(i) + '_back.jpeg', 0)
		hist = img.ravel()
		hist_b.append(hist)
	#全てのヒストグラムの平均を求める
	hist_b_avr = []  #平均化されたhist
	pxelNum = len(hist_b[0]) #画素数
	sampleNum = len(hist_sample) #平均化するサンプルの数
	for i in range(pxelNum):
		summ = 0
		for j in hist_b:
			summ += j[i]
		hist_b_avr.append(summ/sampleNum)
	
	return hist_b_avr






if __name__ == '__main__':
	#表示するものを決定する
	inp = int(raw_input('見たい部位を選択してください。前:1 横:2 後ろ:3　'))
	if inp == 1:
		figure1 = hist_groupAverage_f(1)
		figure2 = hist_groupAverage_f(2)
		figure3 = hist_groupAverage_f(3)
		figure4 = hist_groupAverage_f(4)
	elif inp == 2:
		figure1 = hist_groupAverage_s(1)
		figure2 = hist_groupAverage_s(2)
		figure3 = hist_groupAverage_s(3)
		figure4 = hist_groupAverage_s(4)
	else:
		figure1 = hist_groupAverage_b(1)
		figure2 = hist_groupAverage_b(2)
		figure3 = hist_groupAverage_b(3)
		figure4 = hist_groupAverage_b(4)


	#長さ１
	plt.subplot(2,2,1)
	plt.hist(figure1, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title('length = 1')

	#長さ２
	plt.subplot(2,2,2)
	plt.hist(figure2, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title('length = 2')

	#長さ３
	plt.subplot(2,2,3)
	plt.hist(figure3, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title('length = 3')

	#長さ４
	plt.subplot(2,2,4)
	plt.hist(figure4, 256, [0,256])
	plt.xlim([-10,256])
	plt.ylim([0,1000])
	plt.title('length = 4')

	plt.show()




