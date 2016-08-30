#! /usr/bin/env python
# coding: utf-8

#パラメータ検索からそれにあったサンプル番号リストを返すプログラム

import numpy
import csv

#parameter : パラメータ名  value : その値
#parameter名について
# (0:活動性因子 1:品性因子 2:重量感因子 3:親密性因子) 4:前長 5:横長 6:後長　7:前形 8:横形 9:後形
#valueについて
#長さ:1~4, 前形:0~6, トップ形、後形:1~2

def paraToSample(parameter, value):
	#DB読み込み
	paramnum = 6 #ヘアスタイルのパラメータ数
	allparam = 4 + paramnum #ヘアスタイルのパラメータ + 因子軸数
	sample = numpy.zeros((545, allparam))  #サンプル座標格納用
	resultList = []  #この関数で返すリスト
	try:
		samplenum = 0
		elementnum = 0
		f = open('../zahyou3.csv','rU')
		point = csv.reader(f)
		#各サンプルの座標値の格納
		for row in point:
			for col in row:
				sample[samplenum][elementnum] = float(col)
				elementnum = elementnum + 1
			samplenum = samplenum + 1
			elementnum = 0
	except IOError:
		print "ファイルが開けませんでした: zahyou3.csv"
	finally:
		f.close()

	#DB検索
	for i in range(545):
		v = int(sample[i][parameter]) #検索対象のパラメータの値を一つずつ抽出
		if v == value:
			resultList.append(i+1)  #一致すればそのその時のサンプル番号をresultListに加える

	return resultList
	


if __name__ == '__main__':
	print paraToSample(5,3)






