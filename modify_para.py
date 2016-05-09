#! /usr/bin/env python
# coding: utf-8

#パラメータ推定を導入した修正部
#パラメータ推定に関して、前形はk近傍法を使い、その他のパラメータは加重平均を用いて行う。
#これはあくまでサブシステムである

import kyouritukyouki
import output3
import math
import csv
import numpy
import random

#１回目の修正
class modify1(object):
	alpha = 0.05  #探索範囲計算に使うパラメータ

	def __init__(self, bestnum, bestvalue):
		self.bestnum = bestnum #これが初回修正での探索範囲の中心座標となる
		self.bestvalue = bestvalue #これは探索範囲の半径を決めるパラメータ

		#self.r = self.serchRange(self.bestvalue) #探索範囲の半径を計算
		#self.readfile('zahyou2.csv')
		#self.nextkouho = self.m1select(self.r, self.bestnum)

	#探索範囲
	def searchRange(self):
		r = self.alpha * math.fabs(7-self.bestvalue)
		return r

	#各サンプルの感性情報とパラメータ値の格納
	#0:活動性値, 1:品性値, 2:重量感値, 3:親密値, 4:前長, 5:横長, 6:後長, 7:前形, 8:ボリューム値, 9:ハネ有無
	#file = "zahyou3.csv"
	def readfile(self, file):
		paramnum = 6 #ヘアスタイルのパラメータ数
		allparam = 4 + paramnum #ヘアスタイルのパラメータ + 因子軸数
		self.sample = numpy.zeros((545, allparam))  #サンプル座標格納用
		try:
			samplenum = 0
			elementnum = 0
			f = open(file,'rU')
			point = csv.reader(f)
			#各サンプルの座標値の格納
			for row in point:
				for col in row:
					self.sample[samplenum][elementnum] = float(col)
					elementnum = elementnum + 1
				samplenum = samplenum + 1
				elementnum = 0
		except IOError:
			print "ファイルが開けませんでした: zahyou3.csv"
		finally:
			f.close()

	#座標を選ぶ＋パラメータ推定
	def m1select(self, r):
		n = 10 #選出個数
		m = 5 #パラメータ推定において参照するサンプルの数, k近傍法のパラメータ
		paramnum = 6 #パラメータの数
		frontshape_para = 7 #前形のパラメータ値が格納されている番号(self.sample[])
		dis = {} #探索範囲の中心からの全てのサンプルに対する非類似度
		base = [0]*m #パラメータ推定で参照するサンプル番号
		sortlist = []
		estimatedParam = numpy.zeros((n,paramnum)) #推定されたパラメータ値格納用
		estimatedParam_kinji = numpy.zeros((n,paramnum)) #estimatedParamの要素を整数化にする

		
		#探索の中心座標
		center1 = self.sample[self.bestnum-1][0]
		center2 = self.sample[self.bestnum-1][1]
		center3 = self.sample[self.bestnum-1][2]
		center4 = self.sample[self.bestnum-1][3]
		
		range1_bottom = center1 - r #１軸の探索範囲
		range1_top = center1 + r #１軸の探索範囲
		range2_bottom = center2 - r #２軸の探索範囲
		range2_top = center2 + r #２軸の探索範囲
		range3_bottom = center3 - r #３軸の探索範囲
		range3_top = center3 + r #３軸の探索範囲
		range4_bottom = center4 - r #４軸の探索範囲
		range4_top = center4 + r #４軸の探索範囲


		selectedPoint = numpy.zeros((n,4))  #パラメータ推定を行う座標, 0:活動性軸値, 1:品性軸値, 2:重量感値, 3:親密性値
		for i in range(n):
			selectedPoint[i][0] = random.uniform(range1_bottom, range1_top)
			selectedPoint[i][1] = random.uniform(range2_bottom, range2_top)
			selectedPoint[i][2] = random.uniform(range3_bottom, range3_top)
			selectedPoint[i][3] = random.uniform(range4_bottom, range4_top)

			#上記の点から非類似度が小さい順にn個見つけてくる
			#上記の点と全てのサンプルの非類似度を求めて辞書disに格納
			#dis = {0:サンプル１に対する非類似度, 1:サンプル２に対する非類似度, ・・・}
			for j in range(545):
				dis[j] = math.sqrt(math.pow(selectedPoint[i][0]-self.sample[j][0],2) + math.pow(selectedPoint[i][1]-self.sample[j][1],2) + math.pow(selectedPoint[i][2]-self.sample[j][2],2) + math.pow(selectedPoint[i][3]-self.sample[j][3],2))
			#非類似度で辞書disをソーティングする
			sortlist = sorted(dis.items(), key=lambda x:x[1])
			#soetlist[i][0] = キー sortlist[i][1] = 非類似度
			#参照されるサンプル番号をbaseに格納する
			for j in range(m):
				base[j] = sortlist[j][0]

			#加重平均によるパラメータ推定
			#使うもの：baseに格納されたサンプル番号のパラメータ値 = self.sample[base[i]][4~9]、その非類似度 = dis[base[i]]
			#前形パラメータ以外は加重平均、前形パラメータはk近傍法
			for j in range(4,4+paramnum):
				#加重平均
				if j != frontshape_para: #jがfrontshape_paraの場合はスルー
					bunnbo = 0.0
					bunnsi = 0.0
					for k in base:
						bunnbo = bunnbo + 1/dis[k]
						bunnsi = bunnsi + (1/dis[k]) * self.sample[k][j]
					estimatedParam[i][j-4] = bunnsi / bunnbo
					estimatedParam_kinji[i][j-4] = round(estimatedParam[i][j-4],0)
				#k近傍法
				else:
					k_kosuu = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0} #前形のそれぞれのパラメータ値の出現回数をカウント
					for k in base:
						if self.sample[k][j] == 0:
							k_kosuu[0] = k_kosuu[0] + 1
						elif self.sample[k][j] == 1:
							k_kosuu[1] = k_kosuu[1] + 1
						elif self.sample[k][j] == 2:
							k_kosuu[2] = k_kosuu[2] + 1
						elif self.sample[k][j] == 3:
							k_kosuu[3] = k_kosuu[3] + 1
						elif self.sample[k][j] == 4:
							k_kosuu[4] = k_kosuu[4] + 1
						elif self.sample[k][j] == 5:
							k_kosuu[5] = k_kosuu[5] + 1
						else:
							k_kosuu[6] = k_kosuu[6] + 1

					tasuuketu = sorted(k_kosuu.items(), key=lambda x:x[1], reverse = True) #出現回数が多いパラメータ値の順番に並び変える
					maxkaisuu = tasuuketu[0][1] #一番多い回数
					same = [] #前形のそれぞれにパラメータ値の回数が被った時用　→　ランダムで決めるため
					for z in tasuuketu:
						if z[1] == maxkaisuu:
							same.append(z[0])
					print same
					random.shuffle(same)
					print same
					estimatedParam[i][j-4] = same[0]
					estimatedParam_kinji[i][j-4] = same[0]

		return estimatedParam_kinji

	#候補のヘアスタイル番号を返す
	def hairdesign(estimatedParam):
		samplepara = self.sample[i][4:]
		matchingnum = 0
		for i in range(545):
			if estimatedParam == samplepara:
				matchingnum = i + 1   #推定パラメータと完全に一致した画像番号

		#完全一致するパラメータをもったサンプルがなかった場合
		#if matchingnum == 0:
			

					







#２回目以降の修正
class modify2(modify1):
	def __init__(self, bestnum, bestvalue, revalue):
		modify1.__init__(self, bestnum, bestvalue)
		self.revalue = revalue
		self.revaluenum = len(self.revalue)

	#中心座標の移動
	def cmove(self, relative, prec, prekouho):  #relative:相対評価　prec:前回のベスト番号 prekouho:相対評価を与えた候補(リスト)
		#移動先
		relativesum = 0
		for i in range(self.revaluenum):
			relativesum = relativesum + math.fabs(relative[i])
		m = [0,0,0,0]
		summ = [0,0,0,0]
		for i in range(4):
			for j in range(self.revaluenum):
				summ[i] = summ[i] + relative[j]*(self.sample[prekouho[j]-1][i]-self.sample[prec-1][i])
			m[i] = summ[i]/relativesum
		
		#新たな探索の中心
		nextc = [0.0,0.0,0.0,0.0]
		for i in range(4):
			nextc[i] = self.sample[prec-1][i] + m[i]

		return nextc


	#次世代生成
	def m2select(self, r, center):
		n = 10 #選出個数
		h = {} #中心座標からの距離とそのサンプル番号
		inR = [] #探索範囲内にあるサンプル番号
		nextk = [] #１０個ランダムに選んで格納

		for i in range(0,545):
			hirui = math.sqrt(math.pow(center[0]-self.sample[i][0],2) + math.pow(center[1]-self.sample[i][1],2) + math.pow(center[2]-self.sample[i][2],2) + math.pow(center[3]-self.sample[i][3],2))
			h[i+1] = hirui
		#非類似度がr以下のものを選び出す
		for i in range(1,546):
			if h[i] < r:
				inR.insert(len(inR), i)

		#ランダムに選ぶ
		random.shuffle(inR)
		print inR
		if len(inR)>=10:
			for i in range(n):
				nextk.insert(len(nextk), inR[i])
		else:
			nextk = inR
		return nextk



		






if __name__ == '__main__':
	#入力部
	imageword = u"かわいい"

	#印象推定部
	ie = kyouritukyouki.ImpressionEstimate()
	ie.preprocess(imageword)  #イメージ語の言語的処理
	ie.estimateFactorValue()  #印象値推定
	voltAct = ie.getVoltage(0)
	voltInteli = ie.getVoltage(1)
	voltWeghit = ie.getVoltage(2)
	voltClose = ie.getVoltage(3)
	select = kyouritukyouki.Select(voltAct,voltInteli,voltWeghit,voltClose)
	select.readPoint('zahyou2.csv')
	select.sensyutu()

	#初期出力表示
	firstkouho = select.getSyokinum()
	f_out = output3.App(firstkouho)
	f_out.display()
	f_out.pack()
	f_out.mainloop()

	#１回目修正部
	print "------------------------------"
	print "１回目の修正"
	absolute = f_out.abhyouka_kakutei  #絶対評価値
	best = f_out.sampimg[f_out.bestnum]  #ベストの番号
	md1 = modify1(best, absolute)
	md1.readfile('zahyou3.csv')
	currentcenter = [md1.sample[best-1][0], md1.sample[best-1][1], md1.sample[best-1][2], md1.sample[best-1][3]]
	print u"中心"
	print currentcenter
	r = md1.searchRange()  #探索範囲
	print "半径"
	print r
	print md1.m1select(r)




