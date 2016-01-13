#! /usr/bin/env python
# coding: utf-8

#パラメータ推定を導入した修正部
#パラメータ推定に関して、前形はk近傍法を使い、その他のパラメータは加重平均を用いて行う。


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
	def searchRange(self,v):
		r = self.alpha * math.fabs(7-v)
		return r

	#各サンプルの感性情報とパラメータ値の格納
	#0:活動性値, 1:品性値, 2:重量感値, 3:親密値, 4:前長, 5:横長, 6:後長, 7:前形, 8:ボリューム値, 9:ハネ有無
	#file = "zahyou3.csv"
	def readfile(self, file):
		self.sample = numpy.zeros((545,10))  #サンプル座標格納用
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
			print "ファイルが開けませんでした: zahyou2.csv"
		finally:
			f.close()

	#座標を選ぶ＋パラメータ推定
	def m1select(self, r, bestnum):
		n = 5 #選出個数
		m = 5 #パラメータ推定において参照するサンプルの数
		dis = {} #探索範囲の中心からの全てのサンプルに対する非類似度
		base = [0]*m #パラメータ推定で参照するサンプル番号

		
		#探索の中心座標
		center1 = self.sample[bestnum-1][0]
		center2 = self.sample[bestnum-1][1]
		center3 = self.sample[bestnum-1][2]
		center4 = self.sample[bestnum-1][3]
		
		range1_bottom = center1 - r #１軸の探索範囲
		range1_top = center1 + r #１軸の探索範囲
		range2_bottom = center2 - r #２軸の探索範囲
		range2_top = center2 + r #２軸の探索範囲
		range3_bottom = center3 - r #３軸の探索範囲
		range3_top = center3 + r #３軸の探索範囲
		range4_bottom = center4 - r #４軸の探索範囲
		range4_top = center4 + r #４軸の探索範囲

		#パラメータ推定を行う座標, 0:活動性軸値, 1:品性軸値, 2:重量感値, 3:親密性値
		selectedPoint = numpy.zeros((n,4))
		for i in range(n):
			selectedPoint[i][0] = random.uniform(range1_bottom, range1_top)
			selectedPoint[i][1] = random.uniform(range2_bottom, range2_top)
			selectedPoint[i][2] = random.uniform(range3_bottom, range3_top)
			selectedPoint[i][3] = random.uniform(range4_bottom, range4_top)







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
	md1 = modify1(1,1)
	md1.readfile("zahyou3.csv")
	print md1.sample[544]


