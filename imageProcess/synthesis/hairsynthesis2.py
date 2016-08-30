#! /usr/bin/env python
# coding: utf-8


#ヘアスタイル合成のメインコード
#基準座標型フィッテング手法
#スケール変更　→　位置合わせ　→　クロマキー合成

import cv
import cv2
import numpy as np
import pylab as plt
import synthesis     #クロマキー合成
import hairTranceform2   #スケール変更　＋　位置合わせ


#入力
samplenum = raw_input('合成するヘアスタイル番号を指定してください : ')
sampleName = '../image2/sample' + samplenum + '_front.jpeg'
inputImageName = '../image/face/test_front.jpeg'  #入力顔画像のファイル名
out_inputImageName = '../image/face/inputNoHair.jpeg'

#サンプルの顔座標情報
sampleFacePoint_h = [[160, 45], [160, 218]]  
sampleFacePoint_w = [[96, 131], [225, 131]]
sampleFace_baseX = sampleFacePoint_w[0][0]  #サンプル画像の顔の基準点(x)
sampleFace_baseY = sampleFacePoint_h[0][1]  #サンプル画像の顔の基準点(y)
sFace_height = sampleFacePoint_h[1][1] - sampleFacePoint_h[0][1]  #サンプルの顔の縦の長さ
sFace_width = sampleFacePoint_w[1][0] - sampleFacePoint_w[0][0]  #サンプルの顔の横の長さ

#入力顔画像情報取得
inputImg = cv2.imread(inputImageName)
inputFace_h_point, inputFace_w_point = hairTranceform2.zahyou_get(inputImg)  #入力画像の分析（必要な座標の取得)
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
inputImg = cv2.imread(out_inputImageName)
#ヘア画像の読み込み
sampleImg = cv2.imread(sampleName)

#スケール合わせ
sampleImg_transe, sampleFace_baseX_transe, sampleFace_baseY_transe \
	= hairTranceform2.scale(sFace_height, sFace_width, iFace_height, iFace_width, sampleImg, sampleFace_baseX, sampleFace_baseY)

#位置合わせ
#ここで受け取る二つの画像をクロマキーにかける
inputImg_triming, sampleImg_match = hairTranceform2.matchPoint(sampleImg_transe, inputImg, inputFace_baseX, inputFace_baseY, \
	sampleFace_baseX_transe, sampleFace_baseY_transe, iFace_centerPointX_int, iFace_centerPointY_int)
#一度ファイル名をつけて保存
cv2.imwrite('hair_front.jpeg', sampleImg_match)

#クロマキー合成処理
mask_f = synthesis.mask_front('hair_front.jpeg') #マスク画像作成
#合成出力先の領域作成
h = sampleImg_match.shape[0]
w = sampleImg_match.shape[1]
image_out_ipl = cv.CreateImage((w, h), cv.IPL_DEPTH_8U, 3)
image_out_mat = cv.GetMat(image_out_ipl)
image_out = np.asarray(image_out_mat)
#合成処理
synImage_f = synthesis.syn(sampleImg_match, inputImg_triming, image_out, mask_f)
cv2.imwrite('result/base/hairSyn' + samplenum + '_front.jpeg', synImage_f)



