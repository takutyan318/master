#! /usr/bin/env python
# coding: utf-8

#２値化

import cv
import cv2
import numpy as np
import pylab as plt
import sys

#マスク画像作成（フロント用）
def mask_front(fileName):
	img_gray = cv2.imread(fileName, 0)  #グレースケールで読み込み
	img_gray_mat = cv.fromarray(img_gray)  #配列型からマット型へ
	img_bw = cv.CreateImage(cv.GetSize(img_gray_mat), cv.IPL_DEPTH_8U, 1) #マスク画像を描画する場所作成
	img_bw_mat = cv.GetMat(img_bw)  #マット型の情報取得

	threshold = 70
	cv.Threshold(img_gray_mat, img_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV)   #２値化処理
	img_bw_array = np.asarray(img_bw_mat)  #マット型から配列型へ
	
	#ノイズ除去
	#[200:300, 50:150]でノイズが発生している
	#if flag == 1:
	#	for h in range(230,301):
	#		for w in range(50,151):
	#			if img_bw_array[h,w] == 255:
	#				img_bw_array[h,w] = 0

	return img_bw_array
	#画像表示
	#plt.imshow(img_bw_array, 'gray')
	#plt.show()
	#cv2.waitKey(0)
	#cv2.destroyAllWindows


#マスク画像作成（サイド用）
def mask_side(fileName):
	img_gray = cv2.imread(fileName, 0)  #グレースケールで読み込み
	img_gray_mat = cv.fromarray(img_gray)  #配列型からマット型へ
	img_bw = cv.CreateImage(cv.GetSize(img_gray_mat), cv.IPL_DEPTH_8U, 1) #マスク画像を描画する場所作成
	img_bw_mat = cv.GetMat(img_bw)  #マット型の情報取得

	threshold = 70
	cv.Threshold(img_gray_mat, img_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV)   #２値化処理
	img_bw_array = np.asarray(img_bw_mat)  #マット型から配列型へ
	
	#ノイズ除去
	#[200:240, 70:140]でノイズが発生している
	#for h in range(200,241):
	#	for w in range(70,141):
	#		if img_bw_array[h,w] == 255:
	#			img_bw_array[h,w] = 0
	#[260:300, 140:200]でもノイズ発生
	#for h in range(260,301):
	#	for w in range(140,201):
	#		if img_bw_array[h,w] == 255:
	#			img_bw_array[h,w] = 0

	return img_bw_array
	#画像表示
	#plt.imshow(img_bw_array, 'gray')
	#plt.show()
	#cv2.waitKey(0)
	#cv2.destroyAllWindows


#マスク画像作成（バック用）
def mask_back(fileName):
	img_gray = cv2.imread(fileName, 0)  #グレースケールで読み込み
	img_gray_mat = cv.fromarray(img_gray)  #配列型からマット型へ
	img_bw = cv.CreateImage(cv.GetSize(img_gray_mat), cv.IPL_DEPTH_8U, 1) #マスク画像を描画する場所作成
	img_bw_mat = cv.GetMat(img_bw)  #iplからマット型の情報を取得

	threshold = 80
	cv.Threshold(img_gray_mat, img_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV)   #２値化処理
	img_bw_array = np.asarray(img_bw_mat)  #マット型から配列型へ
	
	return img_bw_array

	#画像表示
	#plt.imshow(img_bw_array, 'gray')
	#plt.show()
	#cv2.waitKey(0)
	#cv2.destroyAllWindows

#合成プロセス
#引数は前景（ヘアスタイル）、背景（顔画像）、出力先、前景のマスク画像
def syn(foreground, background, out, mask):
	#画像サイズ取得
	HEIGHT = foreground.shape[0]
	WIDTH = foreground.shape[1]

	#色チャンネル毎に分ける
	foreground_b = cv2.split(foreground)[0]   #前景の青チャンネル
	foreground_g = cv2.split(foreground)[1]   #前景の緑チャンネル
	foreground_r = cv2.split(foreground)[2]   #前景の赤チャンネル
	background_b = cv2.split(background)[0]   #背景の青チャンネル
	background_g = cv2.split(background)[1]   #背景の緑チャンネル
	background_r = cv2.split(background)[2]   #背景の赤チャンネル
	out_b = cv2.split(out)[0]                 #出力先の青チャンネル
	out_g = cv2.split(out)[1]                 #出力先の緑チャンネル
	out_r = cv2.split(out)[2]                 #出力先の赤チャンネル

	#クロマキーの計算
	for h in range(HEIGHT):
		for w in range(WIDTH):
			bb1 = foreground_b[h][w]
			gg1 = foreground_g[h][w]
			rr1 = foreground_r[h][w]
			bb2 = background_b[h][w]
			gg2 = background_g[h][w]
			rr2 = background_r[h][w]
			if mask[h][w] == 0:
				kk = 0
			elif mask[h][w] == 255:
				kk = 1
			else:
				print 'ERROR'
				sys.exit()

			out_b[h][w] = bb1*kk + bb2*(1-kk)
			out_g[h][w] = gg1*kk + gg2*(1-kk)
			out_r[h][w] = rr1*kk + rr2*(1-kk)
			
	return cv2.merge((out_b, out_g, out_r))




if __name__ == '__main__':
	#画像読み込み（前景）
	fn_f = '../image2/sample18_front.jpeg'   #合成するヘアサンプル画像の名前
	fn_s = '../image2/sample18_side.jpeg'
	fn_b = '../image2/sample18_back.jpeg'
	im_f = cv2.imread(fn_f, cv2.IMREAD_COLOR)
	im_s = cv2.imread(fn_s, cv2.IMREAD_COLOR)
	im_b = cv2.imread(fn_b, cv2.IMREAD_COLOR)


	#画像読み込み（背景）
	fn_input = 'backgroundWhite.jpeg'
	im_input = cv2.imread(fn_input, cv2.IMREAD_COLOR)

	#２値化処理
	mask_f = mask_front(fn_f, 0)
	mask_s = mask_side(fn_s)
	mask_b = mask_back(fn_b)

	#合成出力先の領域作成
	image_out_ipl = cv.CreateImage((320, 320), cv.IPL_DEPTH_8U, 3)
	image_out_mat = cv.GetMat(image_out_ipl)
	image_out = np.asarray(image_out_mat)

	#合成処理
	synImage_f = syn(im_f, im_input, image_out, mask_f)
	synImage_s = syn(im_s, im_input, image_out, mask_s)
	synImage_b = syn(im_b, im_input, image_out, mask_b)

	
	while (True):
		cv2.imshow('mask', mask_s)
		cv2.imshow('clomakie', synImage_s)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()