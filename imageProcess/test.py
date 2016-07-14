#! /usr/bin/env python
# coding: utf-8

#いろいろなテスト用

import cv2
import numpy as np
import sys


# マウスイベント時に処理を行う
def mouse_event(event, x, y, flags, param):

    # 条件によって同じ場所に色の異なる円を入れる
    if y == c:
    	cv2.circle(img, (10,10), 7, (255,0,0), -1)
    else:
    	cv2.circle(img, (10,10), 7, (0,0,255), -1)
    print x, y
        
if __name__ == '__main__':
	# 画像の読み込み
	img = cv2.imread('../image/sample2_front.jpeg')
	h = img.shape[0]
	print h
	w = img.shape[1]
	c = h / 2
	print c
	cv2.line(img, (0,c), (w,c), (255,0,0), 1)
	# ウィンドウのサイズを変更可能にする
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	# マウスイベント時に関数mouse_eventの処理を行う
	cv2.setMouseCallback('img', mouse_event)

	# 「Q」が押されるまで画像を表示する
	while (True):
	    cv2.imshow('img', img)
	    if cv2.waitKey(1) & 0xFF == ord("q"):
	        break

	cv2.destroyAllWindows()