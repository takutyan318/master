#! /usr/bin/env python
# coding: utf-8

#入力された画像の顔の長さを出力する確認用プログラム

import cv2
import numpy as np

def zahyou_get(file = 'scale.jpeg'):
	face_point_h = []  #顔の縦の情報
	face_point_w = []  #顔の横の情報

	#マウスイベント
	def mouse_event_h(event, x, y, flags, param):
	    # 左クリックで赤い円形を生成
	    if event == cv2.EVENT_LBUTTONUP:
	        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
	        a = [x, y]
	        face_point_h.append(a)

	def mouse_event_w(event, x, y, flags, param):
		#マウスの位置によって判定を行う（円が青の時クリックしてOK）
		if y == c:
			cv2.circle(img, (10,10), 7, (255,0,0), -1)
		else:
			cv2.circle(img, (10,10), 7, (0,0,255), -1)

		#左クリックでクリックした場所の座標を取得
		if event == cv2.EVENT_LBUTTONUP:
    			cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
	        	b = [x, y]
	        	face_point_w.append(b)


	img = cv2.imread(file)
	h = img.shape[0]
	w = img.shape[1]
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event_h)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()

	c = (face_point_h[0][1] + face_point_h[1][1]) / 2
	cv2.line(img, (0,c), (w,c), (0,255,0), 1)
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event_w)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()
	return face_point_h, face_point_w


if __name__ == '__main__':
	height, width = zahyou_get()
	heightLength = abs(height[1][1] - height[0][1])
	widthLength = abs(width[1][0] - width[0][0])
	print heightLength, widthLength