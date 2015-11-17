#! /usr/bin/env python
# coding: utf-8

import sys
import WebHitxml2
import math
import csv
import numpy
import output2 as out

class ImpressionEstimate(object):
	inputAdj = "" #イメージ語後ろ
	copyAdj = "" #前
	searchword = ""
	#quote = '"'
	voltage = [0.0, 0.0, 0.0, 0.0] #各因子の印象値
	
	def preprocess(self, inputAdj):
		self.inputAdj = inputAdj
		if self.inputAdj.endswith(u"い") or self.inputAdj.endswith(u"な"):
			if self.inputAdj.endswith(u"い"):
				length = len(self.inputAdj)
				self.copyAdj = self.inputAdj[:length-1]
				self.copyAdj = self.copyAdj + u"くて"
			if self.inputAdj.endswith(u"な"):
				length = len(self.inputAdj)
				self.copyAdj = self.inputAdj[:length-1]
				self.copyAdj = self.copyAdj + u"で"

			return True
		else:
			return False

	def estimateFactorValue(self):
		#活動性因子のヒット件数
		activeHit = [0,0,0,0,0,0,0,0,0,0]
		unactiveHit = [0,0,0,0,0,0,0,0,0,0]
		#品性因子のヒット件数
		inteliHit = [0,0,0,0]
		uninteliHit = [0,0,0,0]
		#重量感因子のヒット件数
		lightHit = [0,0,0]
		heavyHit = [0,0,0]
		#親密性因子のヒット件数
		closeHit = [0,0]
		uncloseHit = [0,0]

		quote = '"'
		result = 0 #ヒット件数
		r1 = 0.0 #類似度（負）
		r2 = 0.0 #類似度（正）
		volt = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] #各印象語対に対する印象値
		m = 2.5 #指数の底
		search = WebHitxml2.Websearch()

		print "-----活動性因子の検索結果-----"
		#活動性因子に対する印象推定
		#共立競技表現の作成
		#消極的な - 積極的な
		#a:前 aA:後ろ
		act1a = u"積極的で"
		unact1a = u"消極的で"
		act1aA = u"積極的な"
		unact1aA = u"消極的な"
		#内向的な - 外交的な
		act2a = u"外交的で"
		unact2a = u"内向的で"
		act2aA = u"外交的な"
		unact2aA = u"内向的な"
		#弱気な - 強気な
		act3a = u"強気で"
		unact3a = u"弱気で"
		act3aA = u"強気な"
		unact3aA = u"弱気な"
		#弱々しい - たくましい
		act4a = u"たくましくて"
		unact4a = u"弱々しくて"
		act4aA = u"たくましい"
		unact4aA = u"弱々しい"
		#弱い - 強い
		act5a = u"強くて"
		unact5a = u"弱くて"
		act5aA = u"強い"
		unact5aA = u"弱い"
		#地味な - 派手な
		act6a = u"派手で"
		unact6a = u"地味で"
		act6aA = u"派手な"
		unact6aA = u"地味な"
		#大人しい - 活発な
		act7a = u"活発で"
		unact7a = u"大人しくて"
		act7aA = u"活発な"
		unact7aA = u"大人しい"
		#陰気な - 陽気な
		act8a = u"陽気で"
		unact8a = u"陰気で"
		act8aA = u"陽気な"
		unact8aA = u"陰気な"
		#穏やかな - 激しい
		act9a = u"激しくて"
		unact9a = u"穏やかで"
		act9aA = u"激しい"
		unact9aA = u"穏やかな"
		#頼りない - 頼もしい
		act10a = u"頼もしくて"
		unact10a = u"頼りなくて"
		act10aA = u"頼もしい"
		unact10aA = u"頼りない"

		#検索
		#消極的な - 積極的な
		#積極的な
		self.searchword = quote + act1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[0] = result
		print "「積極的な」のヒット件数 = " + str(activeHit[0])
		#消極的な
		self.searchword = quote + unact1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[0] = result
		print "「消極的な」のヒット件数 = " + str(unactiveHit[0])

		#内向的な - 外交的な
		#外交的な
		self.searchword = quote + act2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[1] = result
		print "「外交的な」のヒット件数 = " + str(activeHit[1])
		#内向的な
		self.searchword = quote + unact2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[1] = result
		print "「内向的な」のヒット件数 = " + str(unactiveHit[1])

		#弱気な - 強気な
		#強気な
		self.searchword = quote + act3a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act3aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[2] = result
		print "「強気な」のヒット件数 = " + str(activeHit[2])
		#弱気な
		self.searchword = quote + unact3a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact3aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[2] = result
		print "「弱気な」のヒット件数 = " + str(unactiveHit[2])

		#弱々しい - たくましい
		#たくましい
		self.searchword = quote + act4a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act4aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[3] = result
		print "「たくましい」のヒット件数 = " + str(activeHit[3])
		#弱々しい
		self.searchword = quote + unact4a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact4aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[3] = result
		print "「弱々しい」のヒット件数 = " + str(unactiveHit[3])

		#弱い - 強い
		#強い
		self.searchword = quote + act5a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act5aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[4] = result
		print "「強い」のヒット件数 = " + str(activeHit[4])
		#弱い
		self.searchword = quote + unact5a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact5aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[4] = result
		print "「弱い」のヒット件数 = " + str(unactiveHit[4])

		#地味な - 派手な
		#派手な
		self.searchword = quote + act6a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act6aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[5] = result
		print "「派手な」のヒット件数 = " + str(activeHit[5])
		#地味な
		self.searchword = quote + unact6a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact6aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[5] = result
		print "「地味な」のヒット件数 = " + str(unactiveHit[5])

		#大人しい - 活発な
		#活発な
		self.searchword = quote + act7a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act7aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[6] = result
		print "「活発な」のヒット件数 = " + str(activeHit[6])
		#大人しい
		self.searchword = quote + unact7a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact7aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[6] = result
		print "「大人しい」のヒット件数 = " + str(unactiveHit[6])

		#陰気な - 陽気な
		#陽気な
		self.searchword = quote + act8a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act8aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[7] = result
		print "「陽気な」のヒット件数 = " + str(activeHit[7])
		#陰気な
		self.searchword = quote + unact8a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact8aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[7] = result
		print "「陰気な」のヒット件数 = " + str(unactiveHit[7])

		#穏やかな - 激しい
		#激しい
		self.searchword = quote + act9a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act9aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[8] = result
		print "「激しい」のヒット件数 = " + str(activeHit[8])
		#穏やかな
		self.searchword = quote + unact9a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact9aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[8] = result
		print "「穏やかな」のヒット件数 = " + str(unactiveHit[8])

		#頼りない - 頼もしい
		#頼もしい
		self.searchword = quote + act10a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + act10aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		activeHit[9] = result
		print "「頼もしい」のヒット件数 = " + str(activeHit[9])
		#頼りない
		self.searchword = quote + unact10a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unact10aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		unactiveHit[9] = result
		print "「頼りない」のヒット件数 = " + str(unactiveHit[9])

		print ""
		print "------------------------"

		#各印象語対に対する印象値の算出
		for i in range(0,10):
			r1 = 1.0 / math.pow(m, math.log10(unactiveHit[i]))
			r2 = 1.0 / math.pow(m, math.log10(activeHit[i]))
			volt[i] = 2.0 * (r1/(r1+r2)) - 1.0

			#印象値出力
			if i == 0:
				print "「消極的な - 積極的な」の印象値 = " + str(volt[i])
			elif i == 1:
				print "「内向的な - 外交的な」の印象値 = " + str(volt[i])
			elif i == 2:
				print "「弱気な - 強気な」の印象値 = " + str(volt[i])
			elif i == 3:
				print "「弱々しい - たくましい」の印象値 = " + str(volt[i])
			elif i == 4:
				print "「弱い - 強い」の印象値 = " + str(volt[i])
			elif i == 5:
				print "「地味な - 派手な」の印象値 = " + str(volt[i])
			elif i == 6:
				print "「大人しい - 活発な」の印象値 = " + str(volt[i])
			elif i == 7:
				print "「陰気な - 陽気な」の印象値 = " + str(volt[i])
			elif i == 8:
				print "「穏やかな - 激しい」の印象値 = " + str(volt[i])
			else:
				print "「頼りない - 頼もしい」の印象値 = " + str(volt[i])

		print "-----------------------------"


		#因子軸上での印象値の算出
		pluscnt = 0     #印象値が正である数
		pluspre = 0     #正の傾向の中で２番目に大きいヒット件数
		pluspresite = 0 #正の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		plusmax = 0     #正の傾向の中で最も大きいヒット件数
		plusmaxsite = 0 #正の傾向の中で最も多いヒット件数をもつ印象語対の配列番号
		mainasucnt = 0   #印象値が負である数
		mainasupre = 0   #負の傾向の中で２番目に多いヒット件数
		mainasupresite = 0 #負の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		mainasumax = 0   #負の傾向の中で最も多いヒット件数
		mainasumaxsite = 0 #負の傾向の中で最も多いヒット件数の印象語対の配列番号

		for i in range(0,10):
			if volt[i] > 0.0:
				pluscnt = pluscnt + 1
				hitnum = activeHit[i]
				if plusmax < hitnum:
					pluspre = plusmax
					plusmax = hitnum
					pluspresite = plusmaxsite
					plusmaxsite = i

				elif pluspre < hitnum:
					pluspre = hitnum
					pluspresite = i

			if volt[i] < 0.0:
				mainasucnt = mainasucnt + 1
				hitnum = unactiveHit[i]
				if mainasumax < hitnum:
					mainasupre = mainasumax
					mainasumax = hitnum
					mainasupresite = mainasumaxsite
					mainasumaxsite = i
				elif mainasupre < hitnum:
					mainasupre = hitnum
					mainasupresite = i

		if pluscnt > mainasucnt:
			self.voltage[0] = volt[plusmaxsite]
			if pluscnt > 1:
				self.voltage[0] = 0.5*volt[plusmaxsite] + 0.5*volt[pluspresite]

		if pluscnt < mainasucnt:
			self.voltage[0] = volt[mainasumaxsite]
			if mainasucnt > 1:
				self.voltage[0] = 0.5*volt[mainasumaxsite] + 0.5*volt[mainasupresite]

		if pluscnt == mainasucnt:
			self.voltage[0] = 0.0


		print ""
		print u"-----品性因子の検索結果----"
		#品性因子に対する印象推定
		#共立競技表現の作成
		#滑稽な - 知的な
		#a:前 aA:後ろ
		inteli1a = u"知的で"
		uninteli1a = u"滑稽で"
		inteli1aA = u"知的な"
		uninteli1aA = u"滑稽な"
		#不安定な - 安定な
		inteli2a = u"安定で"
		uninteli2a = u"不安定で"
		inteli2aA = u"安定な"
		uninteli2aA = u"不安定な"
		#醜い - 美しい
		inteli3a = u"美しくて"
		uninteli3a = u"醜くて"
		inteli3aA = u"美しい"
		uninteli3aA = u"醜い"
		#不真面目な - 真面目な
		inteli4a = u"真面目で"
		uninteli4a = u"不真面目で"
		inteli4aA = u"真面目な"
		uninteli4aA = u"不真面目な"

		#検索
		#滑稽な - 知的な
		#知的な
		self.searchword = quote + inteli1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + inteli1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		inteliHit[0] = result
		print "「知的な」のヒット件数 = " + str(inteliHit[0])
		#滑稽な
		self.searchword = quote + uninteli1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + uninteli1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		uninteliHit[0] = result
		print "「滑稽な」のヒット件数 = " + str(uninteliHit[0])

		#不安定な - 安定な
		#安定な
		self.searchword = quote + inteli2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + inteli2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		inteliHit[1] = result
		print "「安定な」のヒット件数 = " + str(inteliHit[1])
		#不安定な
		self.searchword = quote + uninteli2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + uninteli2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		uninteliHit[1] = result
		print "「不安定な」のヒット件数 = " + str(uninteliHit[1])

		#醜い - 美しい
		#美しい
		self.searchword = quote + inteli3a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + inteli3aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		inteliHit[2] = result
		print "「美しい」のヒット件数 = " + str(inteliHit[2])
		#醜い
		self.searchword = quote + uninteli3a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + uninteli3aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		uninteliHit[2] = result
		print "「醜い」のヒット件数 = " + str(uninteliHit[2])

		#不真面目な - 真面目な
		#真面目な
		self.searchword = quote + inteli4a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + inteli4aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		inteliHit[3] = result
		print "「真面目な」のヒット件数 = " + str(inteliHit[3])
		#不真面目な
		self.searchword = quote + uninteli4a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + uninteli4aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		uninteliHit[3] = result
		print "「不真面目な」のヒット件数 = " + str(uninteliHit[3])


		
		print ""
		print "------------------------"

		#各印象語対に対する印象値の算出
		for i in range(0,4):
			r1 = 1.0 / math.pow(m, math.log10(uninteliHit[i]))
			r2 = 1.0 / math.pow(m, math.log10(inteliHit[i]))
			volt[i] = 2.0 * (r1/(r1+r2)) - 1.0

			#印象値出力
			if i == 0:
				print "「滑稽な - 知的な」の印象値 = " + str(volt[i])
			elif i == 1:
				print "「不安定な - 安定な」の印象値 = " + str(volt[i])
			elif i == 2:
				print "「醜い - 美しい」の印象値 = " + str(volt[i])
			elif i == 3:
				print "「不真面目な - 真面目な」の印象値 = " + str(volt[i])

		print "-----------------------------"


		#因子軸上での印象値の算出
		pluscnt = 0     #印象値が正である数
		pluspre = 0     #正の傾向の中で２番目に大きいヒット件数
		pluspresite = 0 #正の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		plusmax = 0     #正の傾向の中で最も大きいヒット件数
		plusmaxsite = 0 #正の傾向の中で最も多いヒット件数をもつ印象語対の配列番号
		mainasucnt = 0   #印象値が負である数
		mainasupre = 0   #負の傾向の中で２番目に多いヒット件数
		mainasupresite = 0 #負の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		mainasumax = 0   #負の傾向の中で最も多いヒット件数
		mainasumaxsite = 0 #負の傾向の中で最も多いヒット件数の印象語対の配列番号

		for i in range(0,4):
			if volt[i] > 0.0:
				pluscnt = pluscnt + 1
				hitnum = inteliHit[i]
				if plusmax < hitnum:
					pluspre = plusmax
					plusmax = hitnum
					pluspresite = plusmaxsite
					plusmaxsite = i

				elif pluspre < hitnum:
					pluspre = hitnum
					pluspresite = i

			if volt[i] < 0.0:
				mainasucnt = mainasucnt + 1
				hitnum = uninteliHit[i]
				if mainasumax < hitnum:
					mainasupre = mainasumax
					mainasumax = hitnum
					mainasupresite = mainasumaxsite
					mainasumaxsite = i
				elif mainasupre < hitnum:
					mainasupre = hitnum
					mainasupresite = i

		if pluscnt > mainasucnt:
			self.voltage[1] = volt[plusmaxsite]
			if pluscnt > 1:
				self.voltage[1] = 0.5*volt[plusmaxsite] + 0.5*volt[pluspresite]

		if pluscnt < mainasucnt:
			self.voltage[1] = volt[mainasumaxsite]
			if mainasucnt > 1:
				self.voltage[1] = 0.5*volt[mainasumaxsite] + 0.5*volt[mainasupresite]

		if pluscnt == mainasucnt:
			self.voltage[1] = 0.0



		print ""
		print u"-----重量感因子の検索結果-----"
		#重量感因子の印象推定
		#共立共起表現作成
		#暑苦しい - 涼しい
		light1a = u"涼しくて"
		heavy1a = u"暑苦しくて"
		light1aA = u"涼しい"
		heavy1aA = u"暑苦しい"
		#重い - 軽い
		light2a = u"軽くて"
		heavy2a = u"重くて"
		light2aA = u"軽い"
		heavy2aA = u"重い"
		#鬱陶しい - 爽やかな
		light3a = u"爽やかで"
		heavy3a = u"鬱陶しくて"
		light3aA = u"爽やかな"
		heavy3aA = u"鬱陶しい"

		#検索
		#暑苦しい - 涼しい
		#涼しい
		self.searchword = quote + light1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + light1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		lightHit[0] = result
		print "「涼しい」のヒット件数 = " + str(lightHit[0])
		#暑苦しい
		self.searchword = quote + heavy1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + heavy1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		heavyHit[0] = result
		print "「暑苦しい」のヒット件数 = " + str(heavyHit[0])

		#重い - 軽い
		#軽い
		self.searchword = quote + light2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + light2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		lightHit[1] = result
		print "「軽い」のヒット件数 = " + str(lightHit[1])
		#重い
		self.searchword = quote + heavy2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + heavy2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		heavyHit[1] = result
		print "「重い」のヒット件数 = " + str(heavyHit[1])

		#鬱陶しい - 爽やかな
		#爽やかな
		self.searchword = quote + light3a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + light3aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		lightHit[2] = result
		print "「爽やかな」のヒット件数 = " + str(lightHit[2])
		#鬱陶しい
		self.searchword = quote + heavy3a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + heavy3aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		heavyHit[2] = result
		print "「鬱陶しい」のヒット件数 = " + str(heavyHit[2])


		print ""
		print "------------------------"

		#各印象語対に対する印象値の算出
		for i in range(0,3):
			r1 = 1.0 / math.pow(m, math.log10(heavyHit[i]))
			r2 = 1.0 / math.pow(m, math.log10(lightHit[i]))
			volt[i] = 2.0 * (r1/(r1+r2)) - 1.0

			#印象値出力
			if i == 0:
				print "「暑苦しい - 涼しい」の印象値 = " + str(volt[i])
			elif i == 1:
				print "「重い - 軽い」の印象値 = " + str(volt[i])
			elif i == 2:
				print "「鬱陶しい - 爽やかな」の印象値 = " + str(volt[i])

		print "-----------------------------"


		#因子軸上での印象値の算出
		pluscnt = 0     #印象値が正である数
		pluspre = 0     #正の傾向の中で２番目に大きいヒット件数
		pluspresite = 0 #正の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		plusmax = 0     #正の傾向の中で最も大きいヒット件数
		plusmaxsite = 0 #正の傾向の中で最も多いヒット件数をもつ印象語対の配列番号
		mainasucnt = 0   #印象値が負である数
		mainasupre = 0   #負の傾向の中で２番目に多いヒット件数
		mainasupresite = 0 #負の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		mainasumax = 0   #負の傾向の中で最も多いヒット件数
		mainasumaxsite = 0 #負の傾向の中で最も多いヒット件数の印象語対の配列番号

		for i in range(0,3):
			if volt[i] > 0.0:
				pluscnt = pluscnt + 1
				hitnum = lightHit[i]
				if plusmax < hitnum:
					pluspre = plusmax
					plusmax = hitnum
					pluspresite = plusmaxsite
					plusmaxsite = i

				elif pluspre < hitnum:
					pluspre = hitnum
					pluspresite = i

			if volt[i] < 0.0:
				mainasucnt = mainasucnt + 1
				hitnum = heavyHit[i]
				if mainasumax < hitnum:
					mainasupre = mainasumax
					mainasumax = hitnum
					mainasupresite = mainasumaxsite
					mainasumaxsite = i
				elif mainasupre < hitnum:
					mainasupre = hitnum
					mainasupresite = i

		if pluscnt > mainasucnt:
			self.voltage[2] = volt[plusmaxsite]
			if pluscnt > 1:
				self.voltage[2] = 0.5*volt[plusmaxsite] + 0.5*volt[pluspresite]

		if pluscnt < mainasucnt:
			self.voltage[2] = volt[mainasumaxsite]
			if mainasucnt > 1:
				self.voltage[2] = 0.5*volt[mainasumaxsite] + 0.5*volt[mainasupresite]

		if pluscnt == mainasucnt:
			self.voltage[2] = 0.0


		print ""
		print u"-----親密性因子の検索結果-----"
		#親密性因子の印象推定
		#共立共起表現の作成
		#冷たい - 暖かい
		close1a = u"暖かくて"
		unclose1a = u"冷たくて"
		close1aA = u"暖かい"
		unclose1aA = u"冷たい"
		#冷淡な - 親切な
		close2a = u"親切で"
		unclose2a = u"冷淡で"
		close2aA = u"親切な"
		unclose2aA = u"冷淡な"

		#検索
		#冷たい - 暖かい
		#暖かい
		self.searchword = quote + close1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + close1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		closeHit[0] = result
		print "「暖かい」のヒット件数 = " + str(closeHit[0])
		#冷たい
		self.searchword = quote + unclose1a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unclose1aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		uncloseHit[0] = result
		print "「冷たい」のヒット件数 = " + str(uncloseHit[0])

		#冷淡な - 親切な
		#親切な
		self.searchword = quote + close2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + close2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		closeHit[1] = result
		print "「親切な」のヒット件数 = " + str(closeHit[1])
		#冷淡な
		self.searchword = quote + unclose2a + self.inputAdj + quote
		result = search.track_stream(self.searchword) #共立共起表現のヒット件数
		self.searchword = quote + self.copyAdj + unclose2aA + quote
		result = result + search.track_stream(self.searchword) #共立共起表現のヒット件数
		if result == 0:
			result = 1
			print "ヒット件数ゼロ"
		uncloseHit[1] = result
		print "「冷淡な」のヒット件数 = " + str(uncloseHit[1])


		print ""
		print "------------------------"

		#各印象語対に対する印象値の算出
		for i in range(0,2):
			r1 = 1.0 / math.pow(m, math.log10(uncloseHit[i]))
			r2 = 1.0 / math.pow(m, math.log10(closeHit[i]))
			volt[i] = 2.0 * (r1/(r1+r2)) - 1.0

			#印象値出力
			if i == 0:
				print "「冷たい - 暖かい」の印象値 = " + str(volt[i])
			elif i == 1:
				print "「冷淡な - 親切な」の印象値 = " + str(volt[i])

		print "-----------------------------"

		#因子軸上での印象値の算出
		pluscnt = 0     #印象値が正である数
		pluspre = 0     #正の傾向の中で２番目に大きいヒット件数
		pluspresite = 0 #正の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		plusmax = 0     #正の傾向の中で最も大きいヒット件数
		plusmaxsite = 0 #正の傾向の中で最も多いヒット件数をもつ印象語対の配列番号
		mainasucnt = 0   #印象値が負である数
		mainasupre = 0   #負の傾向の中で２番目に多いヒット件数
		mainasupresite = 0 #負の傾向の中で２番目にヒット件数が多い印象語対の配列番号
		mainasumax = 0   #負の傾向の中で最も多いヒット件数
		mainasumaxsite = 0 #負の傾向の中で最も多いヒット件数の印象語対の配列番号

		for i in range(0,2):
			if volt[i] > 0.0:
				pluscnt = pluscnt + 1
				hitnum = closeHit[i]
				if plusmax < hitnum:
					pluspre = plusmax
					plusmax = hitnum
					pluspresite = plusmaxsite
					plusmaxsite = i

				elif pluspre < hitnum:
					pluspre = hitnum
					pluspresite = i

			if volt[i] < 0.0:
				mainasucnt = mainasucnt + 1
				hitnum = uncloseHit[i]
				if mainasumax < hitnum:
					mainasupre = mainasumax
					mainasumax = hitnum
					mainasupresite = mainasumaxsite
					mainasumaxsite = i
				elif mainasupre < hitnum:
					mainasupre = hitnum
					mainasupresite = i

		if pluscnt > mainasucnt:
			self.voltage[3] = volt[plusmaxsite]
			if pluscnt > 1:
				self.voltage[3] = 0.5*volt[plusmaxsite] + 0.5*volt[pluspresite]

		if pluscnt < mainasucnt:
			self.voltage[3] = volt[mainasumaxsite]
			if mainasucnt > 1:
				self.voltage[3] = 0.5*volt[mainasumaxsite] + 0.5*volt[mainasupresite]

		if pluscnt == mainasucnt:
			self.voltage[3] = 0.0


		print ""
		print "----------------------------"
		print u"イメージ語 : " + self.inputAdj
		print u"活動性因子に対する印象値 = " + str(self.voltage[0])
		print u"品性因子に対する印象値 = " + str(self.voltage[1])
		print u"重量感因子に対する印象値 = " + str(self.voltage[2])
		print u"親密性因子に対する印象値 = " + str(self.voltage[3])
		print "----------------------------"




	def getVoltage(self,num):
		return self.voltage[num]


class Select(object):
	sample = numpy.zeros((545,4))  #サンプル座標格納用
	com = {}  #各サンプルとイメージ語の非類似度
	selectnum = []  #選出されたサンプル番号
	#candidate = [0,0,0,0,0,0,0,0,0,0]  #候補サンプル番号（１０個）
	#dessimiler = [100,100,100,100,100,100,100,100,100,100] #非類似度
	def __init__(self,volt1,volt2,volt3,volt4):
		self.volt1 = volt1
		self.volt2 = volt2
		self.volt3 = volt3
		self.volt4 = volt4
	#ファイルの読み込みと座標値の格納
	def readPoint(self,file):
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

	def sensyutu(self):  #辞書を使ってソートを行うことで候補を決める
		n = 10  #選出する候補数
		#非類似度の算出と辞書の作成
		for i in range(0,545):
			hirui = math.sqrt(math.pow(self.volt1-self.sample[i][0],2) + math.pow(self.volt2-self.sample[i][1],2) + math.pow(self.volt3-self.sample[i][2],2) + math.pow(self.volt4-self.sample[i][3],2))
			self.com[i+1] = hirui

		#非類似度が小さい順にソース(リスト型になる)
		comsort = sorted(self.com.items(), key=lambda x:x[1])
		for i in range(0,n):
			self.selectnum.append(comsort[i][0])
		print self.selectnum

	def getSyokinum(self):
		return self.selectnum











#テスト用
if __name__ == '__main__':
	#inputword = sys.argv
	#print inputword[1]
	#印象推定部
	estimate = ImpressionEstimate()
	estimate.preprocess(u'大人な')
	estimate.estimateFactorValue()
	voltAct = estimate.getVoltage(0)
	voltInteli = estimate.getVoltage(1)
	voltWeghit = estimate.getVoltage(2)
	voltClose = estimate.getVoltage(3)
	#選出部
	select = Select(voltAct,voltInteli,voltWeghit,voltClose)
	select.readPoint('zahyou2.csv')
	select.sensyutu()
	#初期出力表示
	f = out.Frame(select.selectnum)
	f.pack()
	f.mainloop()

	