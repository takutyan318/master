#! /usr/bin/env python
# coding: utf-8

#システムのプログラムと関係ない
#サンプル画像をトリミングする

from PIL import Image

def trimming():
	width = 640
	height = 480
	for num in range(1,546):
		for part in ["front", "side", "back"]:
			try:
				img = Image.open("../experiment/sample" + str(num) + "_" + part + ".jpeg")
				img = img.crop((width/4, height/6, width*3/4, height*5/6))
				img.save("sample" + str(num) + "_" + part + ".jpeg", "JPEG")

				if num == 100:
					print "20%完了"
				elif num == 200:
					print "40%完了"
				elif num == 300:
					print "60%完了"
				elif num == 400:
					print "80%完了"
				elif num == 500:
					print "もうすぐで終わります"

			except IOError:
				print "Error"


if __name__ == '__main__':
	width = 640
	height = 480
	try:
		img = Image.open('/Users/takuya/Desktop/sample_back/sample545_back.jpg')
		img = img.crop((width/4, height/6, width*3/4, height*5/6))
		img.save("/Users/takuya/ihairsystem/imageAfterTriming/sample545_back.jpeg", "JPEG")
	except IOError:
		print "Error"