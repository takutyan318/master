#! /usr/bin/env python
# coding: utf-8

#スケール合わせ　＋　位置合わせ
#フィッティングに関する論文を参考にしたプログラム
#顔の肌領域の左上を基準点にスケール、位置を合わせる方法
#（変更点）顔幅のスケール合わせを口元の顔幅で行う

#(入力画像内の座標取得に関して)
#１、このプログラムを実行したら表示される顔画像の「生え際」→「口元」→「顎先」の順にをマウスで選択（左クリック）してもらう
#２、上記の選択したら「q」を押してもらう
#３、顔の中心に横線が入るのでその線上の「左側輪郭」、「右側輪郭」の順にクリックする
#４、上記を終えたら「q」を押す
#５、口元に横線が入るので「口元左側」、「口元右側」の順にクリックする
#６、上記を終えたら「q」を押す
#7、3,5の選択の際、左上の円が青色になった時にクリックしてもらう

import cv2
import numpy as np
import sys


#入力画像の縦の情報取得
def zahyou_get(img):
	#ローカル変数
	face_point_h = []  #顔の縦の情報(生え際、口元、顎先)
	face_point_w = []  #顔の横の情報（口元の顔幅）, [中心左側, 中心右側, 口元左側, 口元右側]
	h = img.shape[0]
	w = img.shape[1]
	c = 0              #顔の中心の横線のy座標

	#マウスイベント
	#生え際、口元、顎先を選択
	def mouse_event_h(event, x, y, flags, param):
	    # 左クリックで赤い円形を生成
		if event == cv2.EVENT_LBUTTONUP:
			cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
			a = [x, y]
			face_point_h.append(a)
	#口元の顔幅を選択
	def mouse_event_w(event, x, y, flags, param):
		#マウスの位置によって判定を行う（円が青の時クリックしてOK）
		if (y == c) or (y == face_point_h[1][1]):
			cv2.circle(img, (10,10), 7, (255,0,0), -1)
		else:
			cv2.circle(img, (10,10), 7, (0,0,255), -1)

		#左クリックでクリックした場所の座標を取得
		if event == cv2.EVENT_LBUTTONUP:
    			cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
	        	b = [x, y]
	        	face_point_w.append(b)


	#img = cv2.imread(file)
	#縦の座標を取得
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event_h)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()

	if (face_point_h[0][1] < face_point_h[1][1]) and (face_point_h[1][1] < face_point_h[2][1]):
		pass
	else:
		print 'please redo click!!'
		sys.exit()
	#横線を入れる
	#顔の中心に横線をいれる
	c = (float(face_point_h[0][1]) + float(face_point_h[2][1])) / 2.0
	c = int(round(c, 0))
	cv2.line(img, (0,c), (w,c), (0,255,0), 1)
	#横の座標を取得(中心)(右 → 左)
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event_w)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()

	if face_point_w[0][0] < face_point_w[1][0]:
		pass
	else:
		print 'please redo click!!'
		sys.exit()

	#口元のy座標に横線を入れる
	cv2.line(img, (0,face_point_h[1][1]), (w,face_point_h[1][1]), (0,255,0), 1)
	cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('img', mouse_event_w)
	while (True):
		cv2.imshow('img', img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()

	if face_point_w[2][0] < face_point_w[3][0]:
		return face_point_h, face_point_w
	else:
		print 'please redo click!!'
		sys.exit()
	


#ヘアスタイルのスケールを顔の大きさに合わせる
#引数は顔の縦と横の長さ + 変形するサンプル画像
#スケール変更に伴ってサンプル画像の顔中心点を更新する必要あり
#s_baseX, s_baseYはスケール変更前の基準座標
#img : サンプル画像
def scale(s_h_length, s_w_length, i_h_length, i_w_length, img, s_baseX, s_baseY):
	#変数宣言
	height = 0        #サンプル画像の縦のピクセル数
	width = 0         #サンプル画像の横のピクセル数
	compare_h = 0.0   #入力顔のサンプル顔に対する縦の比率
	compare_w = 0.0   #入力顔のサンプル顔に対する横の比率
	transeform_h = 0  #スケール合わせ後のサンプル画像の縦の長さ
	transeform_w = 0  #スケール合わせ後のサンプル画像の横の長さ
	transeImg = 0     #スケール合わせしたサンプル画像
	s_baseX_resize = 0.0   #スケール変更後のサンプル画像の基準点(x)
	s_baseY_resize = 0.0   #スケール変更後のサンプル画像の基準点(y)

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
#i_face_ago : 入力画像の顎先の座標（リスト）→ 非似合い度算出プロセスにおいて使用する
def matchPoint(s_img, i_img, i_face_bX, i_face_bY, s_face_bX, s_face_bY, i_face_cX, i_face_cY, i_face_ago):
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
	#トリミング後の入力が画像の顎先の座標の更新
	i_face_ago[0] = i_face_ago[0] - triming_left
	i_face_ago[1] = i_face_ago[1] - triming_top

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
	return i_img_triming, sampleTranselation, i_face_ago


if __name__ == '__main__':
	#変数宣言
	samplenum = ''              #サンプル画像番号
	sampleName = ''             #サンプル画像名
	inputImageName = ''         #入力画像名
	sampleFacePoint_h = []      #サンプルの顔の座標[生え際座標, 口元座標, 顎先座標]
	sampleFacePoint_w = []      #サンプルの顔の座標[中央左側座標, 中央右側座標, 口元左側座標, 口元右側座標]
	sampleFace_baseX = 0        #サンプル画像の顔の基準点(x)
	sampleFace_baseY = 0        #サンプル画像の顔の基準点(y)
	sFace_height = 0            #サンプルの顔の縦の長さ
	sFace_width = 0             #サンプルの顔の横の長さ（口元）
	inputImg = 0                #入力画像
	inputFace_h_point = []      #入力顔の座標[生え際座標, 口元座標, 顎先座標]
	inputFace_w_point = []      #入力顔の座標[中央左側座標, 中央右側座標, 口元左側座標, 口元右側座標]
	iFace_height = 0            #入力顔画像の縦の長さ
	iFace_width = 0             #入力顔画像の横の長さ
	inputFace_baseX = 0         #入力画像の基準点(x)
	inputFace_baseY = 0         #入力画像の基準点(y)
	iFace_centerPointX = 0.0    #入力顔の中心座標(x)
	iFace_centerPointX_int = 0
	iFace_centerPointY = 0.0    #入力顔の中心座標(y)
	iFace_centerPointY_int = 0
	sampleImg_transe = 0           #スケール合わせ後のサンプル画像
	sampleFace_baseX_transe = 0    #スケール合わせ後のサンプル画像の基準点(x)
	sampleFace_baseY_transe = 0    #スケール合わせ後のサンプル画像の基準点(y)
	inputImg_triming = 0        #スケール合わせ後のサンプル画像にサイズを合わせるためトリミングした入力画像
	sampleImg_match = 0         #基準点をトリミング後の入力画像の基準点と合わせたサンプル画像

	#入力
	samplenum = raw_input('合成するヘアスタイル番号を指定してください : ')
	sampleName = '../image2/sample' + samplenum + '_front.jpeg'
	inputImageName = '../image/face/test_front.jpeg'  #入力顔画像のファイル名

	#サンプルの顔座標情報
	sampleFacePoint_h = [[160, 45], [160, 175], [160, 218]] #[生え際座標, 口元座標, 顎先座標]
	sampleFacePoint_w = [[96, 132], [223, 132], [104, 175], [216, 175]]  #[中央左側座標, 中央右側座標, 口元左側座標, 口元右側座標]
	sampleFace_baseX = sampleFacePoint_w[2][0]  #サンプル画像の顔の基準点(x) (口元の左側座標で合わせる or 中央の左側座標で合わせる)
	sampleFace_baseY = sampleFacePoint_h[0][1]  #サンプル画像の顔の基準点(y)
	sFace_height = sampleFacePoint_h[2][1] - sampleFacePoint_h[0][1]  #サンプルの顔の縦の長さ
	sFace_width = sampleFacePoint_w[3][0] - sampleFacePoint_w[2][0]  #サンプルの顔の横の長さ（口元）

	#入力顔画像情報取得
	inputImg = cv2.imread(inputImageName)
	inputFace_h_point, inputFace_w_point = zahyou_get(inputImg)  #入力画像の分析（必要な座標の取得)
	iFace_height = abs(inputFace_h_point[2][1] - inputFace_h_point[0][1])  #入力顔画像の縦の長さ
	iFace_width = abs(inputFace_w_point[3][0] - inputFace_w_point[2][0])   #入力顔画像の横の長さ
	#入力画像の顔の基準座標を求める
	inputFace_baseX = inputFace_w_point[2][0]
	inputFace_baseY = inputFace_h_point[0][1]
	#入力画像の顔の中心座標を求める
	iFace_centerPointX = (float(inputFace_w_point[0][0]) + float(inputFace_w_point[1][0])) / 2.0
	iFace_centerPointX_int = int(round(iFace_centerPointX, 0))  #整数化
	iFace_centerPointY = (float(inputFace_h_point[0][1]) + float(inputFace_h_point[2][1])) / 2.0
	iFace_centerPointY_int = int(round(iFace_centerPointY, 0))  #整数化

	#顔情報取得時に描かれた図形が邪魔なので再び同じものを読み込む
	inputImg = cv2.imread(inputImageName)
	#ヘア画像の読み込み
	sampleImg = cv2.imread(sampleName)
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
		cv2.imshow('sample', sampleImg_match)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()



