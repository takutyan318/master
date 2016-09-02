#! /usr/bin/env python
# coding: utf-8

#非似合い度Aを求めるプログラム

import sys
sys.path.append('/Users/takuya/ihairsystem/imageProcess/synthesis')
import hairsynthesis3
import cv2
import numpy as np


class Unsuitable_A(object):
	#四角形Aを作成
	#synImg : 合成後の画像(３チャンネル)
	#silBottom : ヘアスタイルと顔画像の合成後の顎先の座標(リスト)
	def cleatSquar_A(self, synImg, silBottom):
		#変数宣言
		synImg_gray = 0               #合成画像のグレースケール
		h1 = []                       #四角形Aの上角の座標
		h2 = []                       #四角形Aの下角の座標
		silTop = []                   #ヘア＋顔領域のトップの座標
		backgroundRange = [120, 160]  #背景のグレースケールでの画素値の範囲
		w1 = [0, 0]                   #四角形Aの左角の座標
		w2 = [0, 0]                   #四角形Aの右角の座標
		horizontalHalf = 0            #四角形Aの横対角線の長さの半分
		silleft = []                  #ヘア＋顔領域の左側座標
		silRight = []                 #ヘア＋顔領域の右側座標
		height = synImg.shape[0]      #合成画像の縦のピクセル数
		width = synImg.shape[1]       #合成画像の横のピクセル数

		h2 = silBottom
		synImg_gray = cv2.cvtColor(synImg, cv2.COLOR_RGB2GRAY)
		#顔＋ヘア領域のトップの座標取得
		for i in range(h2[1]+1):
			x = h2[0]  #顎先のx座標
			if (synImg_gray[i,x]>=backgroundRange[0]) and (synImg_gray[i,x]<=backgroundRange[1]):
				continue
			else:
				h1 = [x, i]
				silTop = [x, i]
				break

		#w1, w2の初期座標の決定
		w1[1] = int(round((float(h1[1]) + float(h2[1])) / 2.0, 0))
		w2[1] = int(round((float(h1[1]) + float(h2[1])) / 2.0, 0))
		horizontalHalf = int(round((float(h2[1])-float(h1[1])) * (2.0/3.0) * (1.0/2.0), 0))
		w1[0] = h1[0] - horizontalHalf
		w2[0] = h1[0] + horizontalHalf

		#シルエットの左側座標、右側座標を求める
		for i in range(width):
			y = w1[1]
			if (synImg_gray[y,i] >= backgroundRange[0]) and (synImg_gray[y,i] <= backgroundRange[1]):
				continue
			else:
				silleft = [i,y]
				break
		for i in range(width-1,0,-1):
			y = w1[1]
			if (synImg_gray[y,i] >= backgroundRange[0]) and (synImg_gray[y,i] <= backgroundRange[1]):
				continue
			else:
				silRight = [i,y]
				break

		
		
		




if __name__ == '__main__':
	#変数宣言
	hs3 = hairsynthesis3.HairSynthesis3()
	us_a = Unsuitable_A()
	h2 = []   #四角形Aの下角の座標
	h1 = []   #四角形Aの上角の座標
	w1 = []   #四角形Aの左角の座標
	w2 = []   #四角形Aの右角の座標
	silBottom = []    # ヘアスタイルと顔画像の合成後の顎先の座標(リスト)
	synImgNum = 0
	synImgName = ''
	synImg = 0  #合成後の画像

	
	silBottom = hs3.synthesisMain()
	synImgNum = raw_input('非似合い度を算出したい合成画像の番号を入力してください : ')
	synImgName = '/Users/takuya/ihairsystem/imageProcess/synthesis/result/base2/hairSyn' +  synImgNum + '_front.jpeg'
	synImg = cv2.imread(synImgName)  
	#test
	st, sl, sr, sb = us_a.cleatSquar_A(synImg, silBottom)
	cv2.circle(synImg, (st[0], st[1]), 3, (255, 0, 0), -1)
	cv2.circle(synImg, (sl[0], sl[1]), 3, (0, 255, 0), -1)
	cv2.circle(synImg, (sb[0], sb[1]), 3, (0, 0, 0), -1)
	cv2.circle(synImg, (sr[0], sr[1]), 3, (0, 0, 255), -1)
	while (True):
		cv2.imshow('test', synImg)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()


	



