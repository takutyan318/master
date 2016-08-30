#! /usr/bin/env python
# coding: utf-8


#ヘアスタイル合成のメインコード
#基準座標型フィッテング手法
#（変更点）横幅には口元の部分時から取得
#スケール変更　→　位置合わせ　→　クロマキー合成
#合成のmain

import cv
import cv2
import numpy as np
import pylab as plt
import synthesis     #クロマキー合成
import hairTranceform3   #スケール変更　＋　位置合わせ
import processAfterSynthesis3

class HairSynthesis3(object):
	def synthesisMain(self):
		#変数宣言
		samplenum = ''              #サンプル画像番号
		sampleName = ''             #サンプル画像名
		inputImageName = ''         #入力画像名
		out_inputImageName = ''     #合成用入力画像
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
		inputImg_ago = []           #入力画像のトリミング後の顎先の座標
		pas = processAfterSynthesis3.ProcessAfterSynthesis3()  #クラス参照
		backColor = [139, 139, 139]  #合成画像の背景の画素値

		#入力
		samplenum = raw_input('合成するヘアスタイル番号を指定してください : ')
		sampleName = '/Users/takuya/ihairsystem/image2/sample' + samplenum + '_front.jpeg'
		inputImageName = '/Users/takuya/ihairsystem/inputImage/input1.jpeg'  #入力顔画像のファイル名
		out_inputImageName = '/Users/takuya/ihairsystem/inputImage/input1_noHair.jpeg'

		#サンプルの顔座標情報
		sampleFacePoint_h = [[160, 45], [160, 175], [160, 218]] #[生え際座標, 口元座標, 顎先座標]
		sampleFacePoint_w = [[96, 132], [223, 132], [104, 175], [216, 175]]  #[中央左側座標, 中央右側座標, 口元左側座標, 口元右側座標]
		sampleFace_baseX = sampleFacePoint_w[2][0]  #サンプル画像の顔の基準点(x) (口元の左側座標で合わせる or 中央の左側座標で合わせる)
		sampleFace_baseY = sampleFacePoint_h[0][1]  #サンプル画像の顔の基準点(y)
		sFace_height = sampleFacePoint_h[2][1] - sampleFacePoint_h[0][1]  #サンプルの顔の縦の長さ
		sFace_width = sampleFacePoint_w[3][0] - sampleFacePoint_w[2][0]  #サンプルの顔の横の長さ（口元）

		#入力顔画像情報取得
		inputImg = cv2.imread(inputImageName)
		inputFace_h_point, inputFace_w_point = hairTranceform3.zahyou_get(inputImg)  #入力画像の分析（必要な座標の取得)
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
		inputImg = cv2.imread(out_inputImageName)
		#ヘア画像の読み込み
		sampleImg = cv2.imread(sampleName)
		#スケール合わせ
		sampleImg_transe, sampleFace_baseX_transe, sampleFace_baseY_transe \
			= hairTranceform3.scale(sFace_height, sFace_width, iFace_height, iFace_width, sampleImg, sampleFace_baseX, sampleFace_baseY)
		#位置合わせ
		#ここで受け取る二つの画像をクロマキーにかける
		inputImg_triming, sampleImg_match, inputImg_ago = hairTranceform3.matchPoint(sampleImg_transe, inputImg, inputFace_baseX, inputFace_baseY, \
			sampleFace_baseX_transe, sampleFace_baseY_transe, iFace_centerPointX_int, iFace_centerPointY_int, inputFace_h_point[2])

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
		#合成後処理
		pas.backAssimilation(synImage_f, backColor)

		cv2.imwrite('/Users/takuya/ihairsystem/imageProcess/synthesis/result/base2/hairSyn' + samplenum + '_front.jpeg', synImage_f)
		return inputImg_ago  #非似合い度算出プログラムにこの値を入れる


		#test






