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
	return mean, u_min, u_max, var

#img : ３チャンネルの画像
def colorAnalyze_3channel(img, searchPoint):
	data_B = []  #統計分析をかけるデータの集合（青チャンネル）
	data_G = []  #統計分析をかけるデータの集合（緑チャンネル）
	data_R = []  #統計分析をかけるデータの集合（赤チャンネル）
	hanni = 25
	t = 1.98  #区間推定の係数
	n = 0   #標本数
	mean_B = 0.0  #青チャンネルの標本平均
	mean_G = 0.0  #緑チャンネルの標本平均
	mean_R = 0.0  #赤チャンネルの標本平均
	var_B = 0.0  #青チャンネルの不偏分散
	var_G = 0.0  #緑チャンネルの不偏分散
	var_R = 0.0  #赤チャンネルの不偏分散
	u_min_B = 0.0 #青チャンネルの下限値
	u_max_B = 0.0 #青チャンネルの上限値
	u_min_G = 0.0 #緑チャンネルの下限値
	u_max_G = 0.0 #緑チャンネルの上限値
	u_min_R = 0.0 #赤チャンネルの下限値
	u_max_R = 0.0 #赤チャンネルの上限値

	#統計処置にかけるサンプルを収集
	for i in searchPoint:
		for j in range(10):
			sx = random.randint(i[0]-hanni,i[0]+hanni)
			sy = random.randint(i[1]-hanni,i[1]+hanni)
			data_B.append(int(img[sy,sx,0]))
			data_G.append(int(img[sy,sx,1]))
			data_R.append(int(img[sy,sx,2]))
	print '青チャンネルデータ'
	print data_B
	print '緑チャンネルデータ'
	print data_G
	print '赤チャンネルデータ'
	print data_R

	#統計処置
	data_B = np.array(data_B)
	data_G = np.array(data_G)
	data_R = np.array(data_R)
	n = len(data_B)
	print n
	mean_B = np.average(data_B)
	mean_G = np.average(data_G)
	mean_R = np.average(data_R)
	var_B = np.var(data_B, ddof=1)
	var_G = np.var(data_G, ddof=1)
	var_R = np.var(data_R, ddof=1)
	u_min_B = mean_B - t*math.sqrt(var_B/n)
	u_max_B = mean_B + t*math.sqrt(var_B/n)
	u_min_G = mean_G - t*math.sqrt(var_G/n)
	u_max_G = mean_G + t*math.sqrt(var_G/n)
	u_min_R = mean_R - t*math.sqrt(var_R/n)
	u_max_R = mean_R + t*math.sqrt(var_R/n)

	mean = [mean_B, mean_G, mean_R]
	var = [var_B, var_G, var_R]
	u_min = [u_min_B, u_min_G, u_min_R]
	u_max = [u_max_B, u_max_G, u_max_R]
	return mean, u_min, u_max, var
			



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
	#img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	m, sita, ue, var = colorAnalyze_3channel(img, sp)
	print '標本平均'
	print m
	print '下限値'
	print sita
	print '上限値'
	print ue
	print '不偏分散'
	print var

	#test
	#while (True):
	#	cv2.imshow('test', img)
	#	if cv2.waitKey(1) & 0xFF == ord("q"):
	#		break
	#cv2.destroyAllWindows()






