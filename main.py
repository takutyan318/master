#! /usr/bin/env python
# coding: utf-8

import kyouritukyouki
import output3
import modify
import sys


#入力部
imageword = sys.argv[1]
imageword = imageword.decode('utf-8')  #日本語の文字列処理を行うため文字列をunicode文字列に変換する必要がある
print u"入力語: " + imageword


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
md1 = modify.modify1(best, absolute)
md1.readfile('zahyou2.csv')
currentcenter = [md1.sample[best-1][0], md1.sample[best-1][1], md1.sample[best-1][2], md1.sample[best-1][3]]
print u"中心"
print currentcenter
r = md1.searchRange()  #探索範囲
print "半径"
print r
nextcandidate = md1.m1select(r)  #新たな候補１０個

#２回目以降の表示と修正（無限loop）
n = 2
while(True):
	s_out = output3.App2(nextcandidate, best)
	s_out.display()
	s_out.display2()
	s_out.pack()
	s_out.mainloop()

	#２回目以降の修正
	print str(n) + "回目の修正"
	absolute = s_out.abhyouka_kakutei #絶対評価値
	relative = s_out.rehyouka_kakutei #相対評価値（リスト）
	md2 = modify.modify2(best,absolute,relative)
	md2.readfile('zahyou2.csv')
	c = md2.cmove(relative, best, nextcandidate)  #新たな探索範囲の中心
	print "中心"
	print c
	r = md2.searchRange() #新たな探索範囲
	print "半径"
	print r
	nextcandidate = md2.m2select(r,c)
	best = s_out.sampimg[s_out.bestnum]
	n = n + 1





