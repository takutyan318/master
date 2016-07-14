#! /usr/bin/env python
# coding: utf-8

#いろいろなテスト用

import cv2
import numpy as np
import sys


# マウスイベント時に処理を行う
def mouse_event(event, x, y, flags, param):

    # 左クリックで赤い円形を生成
    if event == cv2.EVENT_LBUTTONUP:
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
        print '(' + str(x) + ', ' + str(y) + ')'

if __name__ == '__main__':
	# 画像の読み込み
	img = cv2.imread('../image/sample2_front.jpeg')
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