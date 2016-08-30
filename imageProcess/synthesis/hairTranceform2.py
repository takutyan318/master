#! /usr/bin/env python
# coding: utf-8

#スケール合わせ　＋　位置合わせ
#フィッティングに関する論文を参考にしたプログラム
#（変更点）顔の肌領域の左上を基準点にスケール、位置を合わせる方法

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
#スケール変更に伴ってサンプル画像の顔中心点を更新する必要あり
#s_baseX, s_baseYはスケール変更前の基準座標
#img : サンプル画像
def scale(s_h_length, s_w_length, i_h_length, i_w_length, img, s_baseX, s_baseY):
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
	transeImg = cv2.resize(img, (transeform_w, transeform_h))
	#リサイズ後のヘアスタイル画像の顔の中心座標を求める。
	s_baseX_resize = s_baseX * compare_w
	s_baseY_resize = s_baseY * compare_h
	s_baseX_resize = int(round(s_baseX_resize,0))
	s_baseY_resize = int(round(s_baseY_resize,0))

	return transeImg, s_baseX_resize, s_baseY_resize

#位置合わせ処理で扱う関数
#画像を平行移動した際に生じる黒い部分を白に変更する関数
def blackToWhite(tx, ty, imgTranselation, h ,w):
	if (tx>0) and (ty>0):
		for i in range(ty):
			for j in range(w):
				imgTranselation[i][j] = [255, 255, 255]
		for i in range(ty, h):
			for j in range(tx):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx>0) and (ty==0):
		for i in range(h):
			for j in range(tx):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx>0) and (ty<0):
		for i in range(h+ty):
			for j in range(tx):
				imgTranselation[i][j] = [255, 255, 255]
		for i in range(h+ty, h):
			for j in range(w):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx==0) and (ty>0):
		for i in range(ty):
			for j in range(w):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx==0) and (ty<0):
		for i in range(h+ty, h):
			for j in range(w):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx<0) and (ty>0):
		for i in range(ty):
			for j in range(w):
				imgTranselation[i][j] = [255, 255, 255]
		for i in range(ty, h):
			for j in range(w+tx, w):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx<0) and (ty==0):
		for i in range(h):
			for j in range(w+tx, w):
				imgTranselation[i][j] = [255, 255, 255]
	elif (tx<0) and (ty<0):
		for i in range(h+ty):
			for j in range(w+tx, w):
				imgTranselation[i][j] = [255, 255, 255]
		for i in range(h+ty, h):
			for j in range(w):
				imgTranselation[i][j] = [255, 255, 255]
	else:
		pass

#入力画像とヘア画像の基準座標を合わせる部分
#s_img:スケール変更をしたヘア画像, i_img:入力画像
#i_face_bX, i_face_bY:入力画像の基準座標
#s_face_bX, s_face_bY:スケール変更後のヘア画像の基準座標
#i_face_cX, i_face_cY:入力画像の顔の中心座標
def matchPoint(s_img, i_img, i_face_bX, i_face_bY, s_face_bX, s_face_bY, i_face_cX, i_face_cY):
	#入力画像のサイズをリサイズしたサンプル画像のサイズに合わせる
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
		while (triming_top < 0):
			triming_top += 1
			triming_bottom += 1
			if triming_bottom > height_i:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()
	elif triming_bottom > height_i:
		while (triming_bottom > height_i):
			triming_top -= 1
			triming_bottom -= 1
			if triming_top < 0:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()
	elif triming_left < 0:
		while (triming_left < 0):
			triming_left += 1
			triming_right += 1
			if triming_right > width_i:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()
	elif triming_right > width_i:
		while (triming_right > width_i):
			triming_left -= 1
			triming_right -= 1
			if triming_left < 0:
				print 'ImageError : Please re-take the face photo.'
				sys.exit()
	#トリミング処理
	i_img_triming = i_img[triming_top : triming_bottom, triming_left : triming_right]

	#トリミング後の入力画像の基準座標の更新
	i_face_bX = i_face_bX - triming_left
	i_face_bY = i_face_bY - triming_top

	#移動方向を決める
	transelationX = i_face_bX - s_face_bX
	transelationY = i_face_bY - s_face_bY

	#サンプル画像の平行移動処理
	M = np.float32([[1,0,transelationX], [0,1,transelationY]])
	sampleTranselation = cv2.warpAffine(s_img, M, (int(width_s), int(height_s)))

	#平行移動後に生じる黒い部分に対する処理
	blackToWhite(transelationX, transelationY, sampleTranselation,  int(height_s), int(width_s))

	#トリミング処理をした入力画像と位置合わせをしたサンプル画像を返す
	#この後に返した二つの画像をクロマキー合成すればヘアスタイル合成が出来る
	return i_img_triming, sampleTranselation


if __name__ == '__main__':
	#サンプルの顔座標情報
	sampleFacePoint_h = [[160, 45], [160, 218]]  
	sampleFacePoint_w = [[96, 131], [225, 131]]
	sampleFace_baseX = sampleFacePoint_w[0][0]  #サンプル画像の顔の基準点(x)
	sampleFace_baseY = sampleFacePoint_h[0][1]  #サンプル画像の顔の基準点(y)
	sFace_height = sampleFacePoint_h[1][1] - sampleFacePoint_h[0][1]  #サンプルの顔の縦の長さ
	sFace_width = sampleFacePoint_w[1][0] - sampleFacePoint_w[0][0]  #サンプルの顔の横の長さ

	#入力顔画像情報取得
	inputImg = cv2.imread('../image/face/test_front.jpeg')
	inputFace_h_point, inputFace_w_point = zahyou_get(inputImg)  #入力画像の分析（必要な座標の取得)
	iFace_height = abs(inputFace_h_point[1][1] - inputFace_h_point[0][1])  #入力顔画像の縦の長さ
	iFace_width = abs(inputFace_w_point[1][0] - inputFace_w_point[0][0])   #入力顔画像の横の長さ
	#入力画像の顔の基準座標を求める
	inputFace_baseX = min(inputFace_w_point[0][0], inputFace_w_point[1][0])
	inputFace_baseY = min(inputFace_h_point[0][1], inputFace_h_point[1][1])
	#入力画像の顔の中心座標を求める
	iFace_centerPointX = (float(inputFace_w_point[0][0]) + float(inputFace_w_point[1][0])) / 2.0
	iFace_centerPointX_int = int(round(iFace_centerPointX, 0))  #整数化
	iFace_centerPointY = (float(inputFace_h_point[0][1]) + float(inputFace_h_point[1][1])) / 2.0
	iFace_centerPointY_int = int(round(iFace_centerPointY, 0))  #整数化

	#顔情報取得時に描かれた図形が邪魔なので再び同じものを読み込む
	inputImg = cv2.imread('../image/face/test_front.jpeg')
	#ヘア画像の読み込み
	sampleImg = cv2.imread('../image2/sample18_front.jpeg')

	#スケール合わせ
	sampleImg_transe, sampleFace_baseX_transe, sampleFace_baseY_transe \
		= scale(sFace_height, sFace_width, iFace_height, iFace_width, sampleImg, sampleFace_baseX, sampleFace_baseY)

	#位置合わせ
	#ここで受け取る二つの画像をクロマキーにかける
	inputImg_triming, sampleImg_match = matchPoint(sampleImg_transe, inputImg, inputFace_baseX, inputFace_baseY, \
		sampleFace_baseX_transe, sampleFace_baseY_transe, iFace_centerPointX_int, iFace_centerPointY_int)




	#test
	while (True):
		cv2.imshow('input', inputImg_triming)
		cv2.imshow('hair', sampleImg_match)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()











	