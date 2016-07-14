#! /usr/bin/env python
# coding: utf-8

#抽出したヘアスタイル画像を入力画像に合うようにスケール変換、位置合わせを行う。
#顔情報を得てヘアスタイルの画像を変形をするプロセス

#(入力画像内の座標取得に関して)
#１、このプログラムを実行したら表示される顔画像の「生え際」と「顎先」をマウスで選択（左クリック）してもらう
#２、「生え際」と「顎先」を選択したら「q」を押してもらう
#３、横線の入った顔画像が表示されるので、その線上でかつ顔の輪郭と背景の境界線である部分を左部分と右部分の二つをマウスで選択する
#４、3の選択の際、左上の円が青色になった時にクリックしてもらう

import cv2
import numpy as np

#入力画像の縦の情報取得
def zahyou_get(file = '../image/face/test_front.jpeg'):
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



#ヘアスタイルのスケールを顔の大きさに合わせる
#引数は入力画像の顔の縦と横の長さ
#def scale(h, w):


if __name__ == '__main__': 
	#サンプルの顔座標情報
	sampleFacePoint_h = [[158, 43], [159, 221]]
	sampleFacepoint_w = [[80, 132], [239, 132]]

	#入力画像のパスを入力
	#input_img_name = raw_input('Please input path of input image : ')
	inputFace_h_point, inputFace_w_point = zahyou_get()  #入力画像の分析（必要な座標の取得)
	










