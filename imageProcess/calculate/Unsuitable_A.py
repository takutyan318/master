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
	#h2 : ヘアスタイルと顔画像の合成後の顎先の座標(リスト)
	def cleatSquar_A(self, synImg, h2):
		#変数宣言
		synImg_gray = 0               #合成画像のグレースケール
		h1 = []                       #顔＋ヘア領域のトップの座標
		backgroundRange = [120, 160]  #背景のグレースケールでの画素値の範囲

		synImg_gray = cv2.cvtColor(synImg, cv2.COLOR_RGB2GRAY)
		#顔＋ヘア領域のトップの座標取得
		for i in range(h2[1]+1):
			x = h2[0]  #顎先のx座標
			if (synImg_gray[i,x]>=backgroundRange[0]) and (synImg_gray[i,x]<=backgroundRange[1]):
				continue
			else:
				h1 = [x, i]
				break

		return h1



if __name__ == '__main__':
	#変数宣言
	hs3 = hairsynthesis3.HairSynthesis3()
	us_a = Unsuitable_A()
	h2 = []   #ヘアスタイルと顔画像の合成後の顎先の座標(リスト)
	h1 = []   #顔＋ヘア領域のトップの座標
	synImgNum = 0
	synImgName = ''
	synImg = 0  #合成後の画像

	
	h2 = hs3.synthesisMain()
	synImgNum = raw_input('非似合い度を算出したい合成画像の番号を入力してください : ')
	synImgName = '/Users/takuya/ihairsystem/imageProcess/synthesis/result/base2/hairSyn' +  synImgNum + '_front.jpeg'
	synImg = cv2.imread(synImgName)  
	#test
	h1 = us_a.cleatSquar_A(synImg, h2)
	print h1, h2
	cv2.circle(synImg, (h1[0],h1[1]), 5, (0,0,255), -1)
	cv2.circle(synImg, (h2[0],h2[1]), 5, (0,0,255), -1)
	while (True):
		cv2.imshow('test', synImg)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()


	



