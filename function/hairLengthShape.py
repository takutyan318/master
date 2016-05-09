#! /usr/bin/env python
# coding: utf-8

#ヘアデザイン部で矛盾のあるパラメータを見つけ出すための関数を集めたもの


#パラメータ「長さ」について調べる
#どの部位（二箇所）でありえないヘアスタイルの長さになっているのかが欲しい
#引数は辞書型で！！
def length(hl):
	max_value = max(hl[x] for x in hl)  #最も長い部位の長さ
	min_value = min(hl[x] for x in hl)  #最も短い部位の長さ
	sabun = max_value - min_value  

	max_name = max(hl, key=(lambda x: hl[x]))  #最も長い部位
	min_name = min(hl, key=(lambda x: hl[x]))  #最も短い部位

	if sabun >= 3:
		return True, max_name, min_name
	else:
		return False



