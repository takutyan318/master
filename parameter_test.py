#! /usr/bin/env python
# coding: utf-8

#加重平均k近傍法並列パラメータ推定の評価実験のためのプログラム
#中心座標を入力として推定パラメータ値を出力
#これはシステムに実装しないでください

import math
import csv
import numpy
import random
import kyouritukyouki
import sys

m = 5 #パラメータ推定において参照するサンプルの数, k近傍法のパラメータ
paramnum = 6 #パラメータの数
frontshape_para = 7 #前形のパラメータ値が格納されている番号(self.sample[])

def weight_k_estimate(act, inte, weight, friend):  #引数は印象推定部から受け取る
	dis = {} #探索範囲の中心からの全てのサンプルに対する非類似度
	base = [0]*m #パラメータ推定で参照するサンプル番号
	estimatedParam = [0.0] * paramnum #推定されたパラメータ値格納用
	estimatedPara_kinji = [0] * paramnum #推定値を四捨五入したもの

	sample = readfile("zahyou3.csv")

	for j in range(545):
		dis[j] = math.sqrt(math.pow(act-sample[j][0],2) + math.pow(inte-sample[j][1],2) + math.pow(weight-sample[j][2],2) + math.pow(friend-sample[j][3],2))
	print dis
	#非類似度で辞書disをソーティングする
	sortlist = sorted(dis.items(), key=lambda x:x[1])
	print sortlist
	#soetlist[i][0] = キー sortlist[i][1] = 非類似度
	#参照されるサンプル番号をbaseに格納する
	for j in range(m):
		base[j] = sortlist[j][0]
	print base

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
				bunnsi = bunnsi + (1/dis[k]) * sample[k][j]
			estimatedParam[j-4] = bunnsi / bunnbo
			estimatedPara_kinji[j-4] = round(estimatedParam[j-4], 0)
		#k近傍法
		else:
			k_kosuu = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0} #前形のそれぞれのパラメータ値の出現回数をカウント
			for k in base:
				if sample[k][j] == 0:
					k_kosuu[0] = k_kosuu[0] + 1
				elif sample[k][j] == 1:
					k_kosuu[1] = k_kosuu[1] + 1
				elif sample[k][j] == 2:
					k_kosuu[2] = k_kosuu[2] + 1
				elif sample[k][j] == 3:
					k_kosuu[3] = k_kosuu[3] + 1
				elif sample[k][j] == 4:
					k_kosuu[4] = k_kosuu[4] + 1
				elif sample[k][j] == 5:
					k_kosuu[5] = k_kosuu[5] + 1
				else:
					k_kosuu[6] = k_kosuu[6] + 1

			print k_kosuu
			tasuuketu = sorted(k_kosuu.items(), key=lambda x:x[1], reverse = True) #出現回数が多いパラメータ値の順番に並び変える
			maxkaisuu = tasuuketu[0][1] #一番多い回数
			same = [] #前形のそれぞれにパラメータ値の回数が被った時用　→　ランダムで決めるため
			for z in tasuuketu:
				print z
				if z[1] == maxkaisuu:
					print z[1]
					print z[0]
					same.append(z[0])
			print same
			random.shuffle(same)
			print same

			estimatedParam[j-4] = same[0]
			estimatedPara_kinji[j-4] = same[0]


	#return estimatedParam
	return estimatedPara_kinji


def searchFromPara(parameter):
	sample = readfile("zahyou3.csv")
	matchingnum = 0 #マッチングしたサンプル番号

	for i in range(545):
		arraytrue = sample[i][4:] == parameter
		if arraytrue.all():
			print "該当サンプルあり"
			matchingnum = i+1

	print u"推定された近似パラメータ"
	print parameter
	print u"推定されたサンプル情報"
	print sample[matchingnum-1]
	return matchingnum



def readfile(file):
	allparam = 4 + paramnum #ヘアスタイルのパラメータ + 因子軸数
	sample = numpy.zeros((545, allparam))  #サンプル座標格納用
	try:
		samplenum = 0
		elementnum = 0
		f = open(file,'rU')
		point = csv.reader(f)
		#各サンプルの座標値の格納
		for row in point:
			for col in row:
				sample[samplenum][elementnum] = float(col)
				elementnum = elementnum + 1
			samplenum = samplenum + 1
			elementnum = 0
	except IOError:
		print "ファイルが開けませんでした"
	finally:
		f.close()

	return sample



if __name__ == '__main__':
	#imageword = u"軽い"
	#ie = kyouritukyouki.ImpressionEstimate()
	#ie.preprocess(imageword)
	#ie.estimateFactorValue()
	#voltAct = ie.getVoltage(0)
	#voltInteli = ie.getVoltage(1)
	#voltWeghit = ie.getVoltage(2)
	#voltClose = ie.getVoltage(3)
	#voltAct = 0.5
	#voltInteli = -0.2
	#voltWeghit = -0.34
	#voltClose = 0.3
	#result = weight_k_estimate(voltAct, voltInteli, voltWeghit, voltClose)
	#print result
	c_hikisuu = sys.argv
	param = c_hikisuu[1:]
	param_int = map(int, param)
	print "-------------------------------------------------------------------"
	print param_int
	estimatedImage = searchFromPara(param_int)
	print u"推定画像番号は" + str(estimatedImage)




