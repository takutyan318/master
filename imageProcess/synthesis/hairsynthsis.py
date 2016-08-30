#! /usr/bin/env python
# coding: utf-8


#ヘアスタイル合成のメインコード
#顔中心合わせ型フィッテング手法
#スケール変更　→　位置合わせ　→　クロマキー合成


import cv
import cv2
import numpy as np
import pylab as plt
import synthesis     #クロマキー合成
import hairTranceform   #スケール変更　＋　位置合わせ


#入力
samplenum = raw_input('合成するヘアスタイル番号を指定してください : ')
sampleName = '../image2/sample' + samplenum + '_front.jpeg'
inputImageName = '../image/face/test_front.jpeg'  #入力顔画像のファイル名
out_inputImageName = '../image/face/inputNoHair.jpeg'

#サンプル画像の顔情報
sampleFacePoint_h = [[160, 45], [160, 218]]
sampleFacepoint_w = [[97, 132], [224, 132]]
sFace_height = sampleFacePoint_h[1][1] - sampleFacePoint_h[0][1]  #サンプルの顔の縦の長さ
sFace_width = sampleFacepoint_w[1][0] - sampleFacepoint_w[0][0]  #サンプルの顔の横の長さ
#サンプル画像の中心座標を求める
sFace_centerPointX = (float(sampleFacepoint_w[0][0]) + float(sampleFacepoint_w[1][0])) / 2.0
sFace_centerPointX_int = int(round(sFace_centerPointX, 0))  #整数化
sFace_centerPointY = (float(sampleFacePoint_h[0][1]) + float(sampleFacePoint_h[1][1])) / 2.0
sFace_centerPointY_int = int(round(sFace_centerPointY, 0)) #整数化

#入力顔画像情報取得
inputImg = cv2.imread(inputImageName)
inputFace_h_point, inputFace_w_point = hairTranceform.zahyou_get(inputImg)  #入力画像の分析（必要な座標の取得)
iFace_height = abs(inputFace_h_point[1][1] - inputFace_h_point[0][1])  #入力顔画像の縦の長さ
iFace_width = abs(inputFace_w_point[1][0] - inputFace_w_point[0][0])   #入力顔画像の横の長さ
#入力画像の顔の中心座標を求める
iFace_centerPointX = (float(inputFace_w_point[0][0]) + float(inputFace_w_point[1][0])) / 2.0
iFace_centerPointX_int = int(round(iFace_centerPointX, 0))  #整数化
iFace_centerPointY = (float(inputFace_h_point[0][1]) + float(inputFace_h_point[1][1])) / 2.0
iFace_centerPointY_int = int(round(iFace_centerPointY, 0))  #整数化

#顔情報取得時に描かれた図形が邪魔なので再び同じものを読み込む
inputImg = cv2.imread(out_inputImageName)

#スケール合わせ
sampleImg = cv2.imread(sampleName)
sampleImg_transe, sFace_centerPointX_transe, sFace_centerPointY_transe= hairTranceform.scale(sFace_height, sFace_width, iFace_height, iFace_width, sampleImg, sFace_centerPointX, sFace_centerPointY)

#位置合わせ
#iFace_centerPointX_triming : 入力画像のトリミング後の顔中心座標(x) iFace_centerPointY_triming : 入力画像のトリミング後の顔中心座標(y)
#inputImg_triming : 入力画像をトリミングした画像
#ここで受け取った二つの画像に対してクロマキー合成処理を行う
inputFaceImg, hairImg = hairTranceform.matchPoint(sampleImg_transe, inputImg, iFace_centerPointX_int, iFace_centerPointY_int, sFace_centerPointX_transe, sFace_centerPointY_transe)
cv2.imwrite('hair_front.jpeg', hairImg)



#クロマキー合成処理
mask_f = synthesis.mask_front('hair_front.jpeg') #マスク画像作成
#合成出力先の領域作成
h = hairImg.shape[0]
w = hairImg.shape[1]
image_out_ipl = cv.CreateImage((w, h), cv.IPL_DEPTH_8U, 3)
image_out_mat = cv.GetMat(image_out_ipl)
image_out = np.asarray(image_out_mat)
#合成処理
synImage_f = synthesis.syn(hairImg, inputFaceImg, image_out, mask_f)
cv2.imwrite('result/hairSys' + samplenum + '_front.jpeg', synImage_f)













