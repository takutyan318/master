#! /usr/bin/env python
# coding: utf-8

#合成後の後処理用
#白抜き部分の背景同化を行う

import cv2
import numpy as np


class ProcessAfterSynthesis3(object):
	def zahyou_get_mouse(self, img):
		#クリックした座標の画素値を取得
		def mouse_event(event, x, y, flags, param):
		    # 左クリックで赤い円形を生成
			if event == cv2.EVENT_LBUTTONUP:
				print img[y,x]

		#縦の座標を取得
		cv2.namedWindow("img", cv2.WINDOW_NORMAL)
		cv2.setMouseCallback('img', mouse_event)
		while (True):
			cv2.imshow('img', img)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		cv2.destroyAllWindows()

	#合成画像の背景と白抜き部分の同化を行うメソッド
	#img : 合成処理後の画像
	#backColor : imgの背景の画素値(３チャンネル)
	def backAssimilation(self, img, backColor):
		#変数宣言
		height = img.shape[0]   #imgの高さ
		width = img.shape[1]    #imgの幅
		img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #RGBからグレースケールへ

		#白抜き部分を背景色に変更
		for h in range(height):
			for w in range(width):
				if (img_gray[h,w] >= 230) and (img_gray[h,w] <=255):
					img[h,w] = backColor
		
		




if __name__ == '__main__':
	imgName = '/Users/takuya/ihairsystem/imageProcess/synthesis/result/base2/hairSyn18_front.jpeg'
	backColor = [139, 139, 139]  #合成画像の背景の画素値
	#imgAssimilation = 0  #背景同化した画像
	pas = ProcessAfterSynthesis3()  #クラス参照
	img = cv2.imread(imgName)

	pas.backAssimilation(img, backColor)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()
	


