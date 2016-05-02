#! /usr/bin/env python
# coding: utf-8

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

	#座標抽出
	def readfile(self, file):
		self.sample = numpy.zeros((545,4))  #サンプル座標格納用
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

	#１回目の探索範囲内からランダムに１０個選出
	def m1select(self, r):
		n = 10 #選出個数
		h = {} #中心座標からの距離とそのサンプル番号
		inR = [] #探索範囲内にあるサンプル番号
		nextk = [] #１０個ランダムに選んで格納
		#探索の中心座標
		center1 = self.sample[self.bestnum-1][0]
		center2 = self.sample[self.bestnum-1][1]
		center3 = self.sample[self.bestnum-1][2]
		center4 = self.sample[self.bestnum-1][3]
		for i in range(0,545):
			hirui = math.sqrt(math.pow(center1-self.sample[i][0],2) + math.pow(center2-self.sample[i][1],2) + math.pow(center3-self.sample[i][2],2) + math.pow(center4-self.sample[i][3],2))
			h[i+1] = hirui
		#非類似度がr以下のものを選び出す
		for i in range(1,546):
			if h[i] < r:
				inR.insert(len(inR), i)

		#ランダムに選ぶ
		random.shuffle(inR)
		if len(inR)>=10:
			for i in range(n):
				nextk.insert(len(nextk), inR[i])
		else:
			nextk = inR
		return nextk




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
	test = [1,2,3,4,5,6]
	out1 = output3.App(test)
	out1.pack()
	out1.mainloop()
	md = modify1(5, 2)
	print md.nextkouho


