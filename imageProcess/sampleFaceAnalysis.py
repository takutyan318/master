#! /usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

#サンプルの顔情報を得るためのプログラム
def zahyou_get():
	face_point = []
	def mouse_event(event, x, y, flags, param):
	    # 左クリックで赤い円形を生成
	    if event == cv2.EVENT_LBUTTONUP:
	        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
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


if __name__ == '__main__':
	point = zahyou_get()
	print point