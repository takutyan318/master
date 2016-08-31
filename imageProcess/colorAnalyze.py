#! /usr/bin/env python
# coding: utf-8

#色の均一部分（背景や肌）の画素値の平均とその９５%信頼区間を取得するためのプログラム
#これはシステムに組み込むものではない（分析用）

import cv2
import numpy as np
import random
import math


def colorAnalyze_getSample(img):
	hanni = 25
	h = img.shape[0]
	w = img.shape[1]
	searchPoint = []
	#ピクセルサンプルを取得
	def getSample(event, x, y, flags, param):
		if (x-hanni >= 0) and (x+hanni < w) and (y-hanni >= 0) and (y+hanni < h):
			cv2.circle(img, (10,10), 7, (255,0,0), -1)
		else:
			cv2.circle(img, (10,10), 7, (0,0,255), -1)
	    # 左クリックで赤い円形を生成
		if event == cv2.EVENT_LBUTTONUP:
			cv2.rectangle(img, (x-hanni, y-hanni),(x+hanni, y+hanni), (0, 0, 255), 1)
			searchPoint.append([x,y])
			
	#サンプル収集
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', getSample)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()
	return searchPoint

#img : グレースケール画像
#searchPoint : サンプル
def colorAnalyze_mono(img, searchPoint):
	data = []  #統計分析をかけるデータの集合
	hanni = 25
	t = 1.98  #区間推定の係数
	n = 0.0
	mean = 0.0
	var = 0.0 #不偏分散
	u_min = 0.0  #信頼区間下限値
	u_max = 0.0  #信頼区間上限値

	#統計処置にかけるサンプルを収集
	for i in searchPoint:
		for j in range(10):
			sx = random.randint(i[0]-hanni,i[0]+hanni)
			sy = random.randint(i[1]-hanni,i[1]+hanni)
			data.append(int(img[sy,sx]))

	#統計処理
	data = np.array(data)
	n = len(data)  #標本サイズ
	mean = np.average(data)  #標本平均
	var = np.var(data, ddof=1)
	u_min = mean - t*math.sqrt(var/n)
	u_max = mean + t*math.sqrt(var/n)
	return mean, u_min, u_max

			



if __name__ == '__main__':
	#変数宣言
	synNum = raw_input('分析したい合成画像の番号を入力してください : ')
	imgName = '/Users/takuya/ihairsystem/imageProcess/synthesis/result/base2/hairSyn' + synNum + '_front.jpeg'
	img = 0  #カラースケールで読み込み
	sp = []  #サンプル取得の中心座標の集合
	img_gray = 0  #グレースケール画像
	
	#サンプル取得
	img = cv2.imread(imgName)
	sp = colorAnalyze_getSample(img)

	#分析
	img = cv2.imread(imgName)
	img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	m, sita, ue = colorAnalyze_mono(img_gray, sp)
	print '標本平均'
	print m
	print '下限値'
	print sita
	print '上限値'
	print ue

	#test
	#while (True):
	#	cv2.imshow('test', img)
	#	if cv2.waitKey(1) & 0xFF == ord("q"):
	#		break
	#cv2.destroyAllWindows()






