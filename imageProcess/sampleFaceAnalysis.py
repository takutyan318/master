#! /usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

#サンプルの顔情報を得るためのプログラム
#入力画像の顔情報を得るのにも使える
def zahyou_get():
	face_point = []

	#マウスイベント
	def mouse_event(event, x, y, flags, param):
	    # 左クリックで赤い円形を生成
	    if event == cv2.EVENT_LBUTTONUP:
	        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
	        print '(' + str(x) + ', ' + str(y) + ')'
	        a = [x, y]
	        face_point.append(a)


	img = cv2.imread('../image/sample2_front.jpeg')
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

	cv2.destroyAllWindows()
	return face_point

#顔の縦の長さから顔の横の長さを決めるための座標をきめる
def decide_wZahyou(point_h):
	#顔の横の長さを決める特徴点の座標(x,y)
	w_point = []

	#顔のy座標の中心を求める
	centerY = (point_h[1][1] + point_h[0][1]) / 2
	print centerY
	#y = centerYの画素上を横に探索していき画素値が変化した位置を顔領域とする
	img = cv2.imread('../image/sample2_front.jpeg', 0)
	width = img.shape[1]
	backColor = img[0][0]
	#左から探索
	for w in range(width):
		if img[centerY][w] != backColor:
			w_point.append([w, centerY])
			break
	#右から探索
	for w in range(width-1, -1, -1):
		if img[centerY][w] != backColor:
			w_point.append([w, centerY])
			break

	return w_point




if __name__ == '__main__':
	point_h = zahyou_get()  #point = (トップ座標, 顎先座標)
	point_w = decide_wZahyou(point_h)
	img2 = cv2.imread('../image/sample2_front.jpeg')
	cv2.circle(img2, (point_h[0][0], point_h[0][1]), 10, (0, 0, 255), -1)
	cv2.circle(img2, (point_h[1][0], point_h[1][1]), 10, (0, 0, 255), -1)
	cv2.circle(img2, (point_w[0][0], point_w[0][1]), 10, (0, 0, 255), -1)
	cv2.circle(img2, (point_w[1][0], point_w[1][1]), 10, (0, 0, 255), -1)
	while (True):
		cv2.imshow('img', img2)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()
	print point_h, point_w


	