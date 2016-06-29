#! /usr/bin/env python
# coding: utf-8

#２値化

import cv
import cv2
import numpy as np
import pylab as plt

#マスク画像作成（フロント用）
def mask_front(fileName):
	img_gray = cv2.imread(fileName, 0)  #グレースケールで読み込み
	img_gray_mat = cv.fromarray(img_gray)  #配列型からマット型へ
	img_bw = cv.CreateImage(cv.GetSize(img_gray_mat), cv.IPL_DEPTH_8U, 1) #マスク画像を描画する場所作成
	img_bw_mat = cv.GetMat(img_bw)  #マット型の情報取得

	threshold = 25
	cv.Threshold(img_gray_mat, img_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV)   #２値化処理
	img_bw_array = np.asarray(img_bw_mat)  #マット型から配列型へ
	
	#ノイズ除去
	#[200:300, 50:150]でノイズが発生している
	for h in range(200,301):
		for w in range(50,151):
			if img_bw_array[h,w] == 255:
				img_bw_array[h,w] = 0

	#画像表示
	plt.imshow(img_bw_array, 'gray')
	plt.show()
	cv2.waitKey(0)
	cv2.destroyAllWindows


#マスク画像作成（サイド用）
def mask_side(fileName):
	img_gray = cv2.imread(fileName, 0)  #グレースケールで読み込み
	img_gray_mat = cv.fromarray(img_gray)  #配列型からマット型へ
	img_bw = cv.CreateImage(cv.GetSize(img_gray_mat), cv.IPL_DEPTH_8U, 1) #マスク画像を描画する場所作成
	img_bw_mat = cv.GetMat(img_bw)  #マット型の情報取得

	threshold = 25
	cv.Threshold(img_gray_mat, img_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV)   #２値化処理
	img_bw_array = np.asarray(img_bw_mat)  #マット型から配列型へ
	
	#ノイズ除去
	#[200:240, 70:140]でノイズが発生している
	for h in range(200,241):
		for w in range(70,141):
			if img_bw_array[h,w] == 255:
				img_bw_array[h,w] = 0
	#[260:300, 140:200]でもノイズ発生
	for h in range(260,301):
		for w in range(140,201):
			if img_bw_array[h,w] == 255:
				img_bw_array[h,w] = 0

	#画像表示
	plt.imshow(img_bw_array, 'gray')
	plt.show()
	cv2.waitKey(0)
	cv2.destroyAllWindows


#マスク画像作成（バック用）
def mask_back(fileName):
	img_gray = cv2.imread(fileName, 0)  #グレースケールで読み込み
	img_gray_mat = cv.fromarray(img_gray)  #配列型からマット型へ
	img_bw = cv.CreateImage(cv.GetSize(img_gray_mat), cv.IPL_DEPTH_8U, 1) #マスク画像を描画する場所作成
	img_bw_mat = cv.GetMat(img_bw)  #マット型の情報取得

	threshold = 50
	cv.Threshold(img_gray_mat, img_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV)   #２値化処理
	img_bw_array = np.asarray(img_bw_mat)  #マット型から配列型へ
	

	#画像表示
	plt.imshow(img_bw_array, 'gray')
	plt.show()
	cv2.waitKey(0)
	cv2.destroyAllWindows




if __name__ == '__main__':
	fn_f = '../image/sample1_front.jpeg'   #合成するヘアサンプル画像の名前
	fn_s = '../image/sample1_side.jpeg'
	fn_b = ''
	fn_b = '/Users/takuya/Desktop/test.jpg'
	mask_side(fn_b)