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
import sys

#入力画像の縦の情報取得
def zahyou_get(img):
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


	#img = cv2.imread(file)
	h = img.shape[0]
	w = img.shape[1]
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event_h)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()

	c = (float(face_point_h[0][1]) + float(face_point_h[1][1])) / 2.0
	c = int(round(c, 0))  #整数化
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
#引数は顔の縦と横の長さ + 変形するサンプル画像
def scale(s_h_length, s_w_length, i_h_length, i_w_length, img):
	#少数化
	s_h_length = float(s_h_length)
	s_w_length = float(s_w_length)
	i_h_length = float(i_h_length)
	i_w_length = float(i_w_length)

	#変形するサンプル画像のピクセル数取得
	height = img.shape[0]
	width = img.shape[1]

	compare_h = i_h_length / s_h_length   #縦の比率
	compare_w = i_w_length / s_w_length   #横の比率
	#リサイズ後のサイズ
	transeform_h = int(round(height*compare_h, 0))
	transeform_w = int(round(width*compare_w, 0))

	#リサイズ
	transeImg = cv2.resize(img, (transeform_h, transeform_w))
	return transeImg

#位置合わせ処理
#スケール変更後のサンプル(s_img)と入力画像(i_img)を引数にとりサンプル画像を平行移動させた画像を出力させる。
#i_face_cX : 入力画像の顔の中心x座標　i_face_cY : 入力画像の顔の中心y座標
#s_face_cX : サンプル画像の顔の中心x座標　s_face_cY : サンプル画像の顔の中心y座標
def matchPoint(s_img, i_img, i_face_cX, i_face_cY, s_face_cX, s_face_cY):
	#スケール変更したサンプル画像のサイズを取得
	height_s = float(s_img.shape[0])
	width_s = float(s_img.shape[1])
	#サンプル画像に合わせて入力画像をトリミングする（同じサイズにする）
	x = int(round(width_s/2.0, 0))
	y = int(round(height_s/2.0, 0))

	#入力画像のサイズを取得
	height_i = i_img.shape[0]
	width_i = i_img.shape[1]

	#トリミングの範囲に異常がないかの確認と処理
	triming_top = i_face_cY - y
	triming_bottom = i_face_cY + y
	triming_left = i_face_cX - x
	triming_right = i_face_cX + x
	if triming_top < 0:
		while (triming_top >= 0):
			triming_top += 1
			triming_bottom += 1
			if triming_bottom > height_i:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()
	elif triming_bottom > height_i:
		while (triming_bottom <= height_i):
			triming_top -= 1
			triming_bottom -= 1
			if triming_top < 0:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()
	elif triming_left < 0:
		while (triming_left >= 0):
			triming_left += 1
			triming_right += 1
			if triming_right > width_i:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()




	i_img_triming = i_img[triming_top : triming_bottom, triming_left : triming_right]  #トリミング処理

	
	
	#トリミング後の原点はトリミング前の(i_face_cX - x, i_face_cY - y)
	#入力画像のトリミング後の顔中心座標補正
	i_face_cX = i_face_cX - (i_face_cX - x)  #トリミング後の入力画像の顔の中心座標 (x)
	i_face_cY = i_face_cY - (i_face_cY - y)  #トリミング後の入力画像の顔の中心座標 (y)

	#test
	return i_face_cX, i_face_cY, i_img_triming







if __name__ == '__main__': 
	#サンプルの顔座標情報
	sampleFacePoint_h = [[160, 42], [160, 221]]
	sampleFacepoint_w = [[96, 131], [225, 131]]
	sFace_height = sampleFacePoint_h[1][1] - sampleFacePoint_h[0][1]  #サンプルの顔の縦の長さ
	sFace_width = sampleFacepoint_w[1][0] - sampleFacepoint_w[0][0]  #サンプルの顔の横の長さ
	#サンプル画像の中心座標を求める
	sFace_centerPointX = (float(sampleFacepoint_w[0][0]) + float(sampleFacepoint_w[1][0])) / 2.0
	sFace_centerPointX = int(round(sFace_centerPointX, 0))  #整数化
	sFace_centerPointY = (float(sampleFacePoint_h[0][1]) + float(sampleFacePoint_h[1][1])) / 2.0
	sFace_centerPointY = int(round(sFace_centerPointY, 0)) #整数化

	#入力顔画像情報取得
	inputImg = cv2.imread('../image/face/test_front.jpeg')
	inputFace_h_point, inputFace_w_point = zahyou_get(inputImg)  #入力画像の分析（必要な座標の取得)
	iFace_height = abs(inputFace_h_point[1][1] - inputFace_h_point[0][1])  #入力顔画像の縦の長さ
	iFace_width = abs(inputFace_w_point[1][0] - inputFace_w_point[0][0])   #入力顔画像の横の長さ
	#入力画像の顔の中心座標を求める
	iFace_centerPointX = (float(inputFace_w_point[0][0]) + float(inputFace_w_point[1][0])) / 2.0
	iFace_centerPointX = int(round(iFace_centerPointX, 0))  #整数化
	iFace_centerPointY = (float(inputFace_h_point[0][1]) + float(inputFace_h_point[1][1])) / 2.0
	iFace_centerPointY = int(round(iFace_centerPointY, 0))  #整数化


	#スケール合わせ
	sampleImg = cv2.imread('../image/sample2_front.jpeg')
	sampleImg_transe = scale(sFace_height, sFace_width, iFace_height, iFace_width, sampleImg)


	#位置合わせ
	#iFace_centerPointX_triming : 入力画像のトリミング後の顔中心座標(x) iFace_centerPointY_triming : 入力画像のトリミング後の顔中心座標(y)
	#inputImg_triming : 入力画像をトリミングした画像
	iFace_centerPointX_triming, iFace_centerPointY_triming, inputImg_triming = matchPoint(sampleImg_transe, inputImg, iFace_centerPointX, iFace_centerPointY, sFace_centerPointX, sFace_centerPointY)

	#cv2.circle(inputImg, (iFace_centerPointX, iFace_centerPointY), 10, (0, 0, 255), -1)
	#cv2.circle(inputImg_triming, (iFace_centerPointX_triming, iFace_centerPointY_triming), 10, (255, 0, 0), -1)
	while (True):
		#cv2.imshow('inputImg', inputImg)
		cv2.imshow('inputImg_triming', inputImg_triming)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()










