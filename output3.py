#! /usr/bin/env python
# coding: utf-8
     
import Tkinter as Tk
from PIL import Image, ImageTk
from ttk import *
import sys
import numpy


#これは修正に関するGUI

#GUIから引き抜く値について
#絶対評価：self.abhyouka_kakutei  BEST:self.sampimg[self.bestnum]   相対評価：self.rehyouka_kakutei[i]
#getterなどは準備していないので取り扱い注意


#１回目の修正ウィンドウ
class App(Tk.Frame):

	EXIST_OR_NOT = False  #ウィンドウの二重展開防止のための関数
	#bestok = False #bestが選ばれたかどうか

	#ウィンドウ全体の設定
	def __init__(self,smpimg,master=None):
		Tk.Frame.__init__(self, master)
		self.master.title(u'ヘアデザインシステム')
		self.master.geometry("1440x900")
		self.sampimg = smpimg

	def display(self):
		w1 = 288 #front画像表示サイズ
		h1 = 288 #front画像表示サイズ
		w2 = 144 #side,back画像表示サイズ
		h2 = 144 #side,back画像表示サイズ
		self.img_f = [0,0,0,0,0,0,0,0,0,0]  #前の画像番号
		self.img_s = [0,0,0,0,0,0,0,0,0,0]  #横の画像番号
		self.img_b = [0,0,0,0,0,0,0,0,0,0]  #後ろの画像番号
		fn = 0  #frame番号
		self.f = [0,0,0,0,0,0,0,0,0,0] #画像のラベルを乗っけるフレーム
		note = Notebook(self)
		self.tag1 = Tk.Frame(note)
		self.tag2 = Tk.Frame(note)
		note.add(self.tag1, text=u"ページ１")
		note.add(self.tag2, text=u"ページ２")

		#画像の表示部分
		for imgnum in self.sampimg:
			#画像の読み込みとサイズ変更
			imgname1 = "sample" + str(imgnum) + "_front.jpeg"
			imgname2 = "sample" + str(imgnum) + "_side.jpeg"
			imgname3 = "sample" + str(imgnum) + "_back.jpeg"
			image1 = Image.open(imgname1)
			image2 = Image.open(imgname2)
			image3 = Image.open(imgname3)
			image1 = image1.resize((w1,h1))
			image2 = image2.resize((w2,h2))
			image3 = image3.resize((w2,h2))

			#GUIに画像を貼り付ける
			if fn < 5:
				self.f[fn] = Tk.LabelFrame(self.tag1, text=u"候補"+str(fn+1))
				if fn < 3:
					self.f[fn].grid(row=0,column=fn, padx=5, pady=5)
				else:
					self.f[fn].grid(row=1,column=fn%3, padx=5, pady=5)
			else:
				self.f[fn] = Tk.LabelFrame(self.tag2, text=u"候補"+str(fn+1))
				if fn < 8:
					self.f[fn].grid(row=0,column=fn%5, padx=5, pady=5)
				else:
					self.f[fn].grid(row=1,column=fn%8, padx=5, pady=5)
			self.img_f[fn] = ImageTk.PhotoImage(image1)
			self.img_s[fn] = ImageTk.PhotoImage(image2)
			self.img_b[fn] = ImageTk.PhotoImage(image3)
			il1 = Tk.Label(self.f[fn], image=self.img_f[fn])
			il2 = Tk.Label(self.f[fn], image=self.img_s[fn])
			il3 = Tk.Label(self.f[fn], image=self.img_b[fn])
			il1.grid(row=0, column=0, rowspan=2)
			il2.grid(row=0, column=1)
			il3.grid(row=1, column=1)
			fn = fn + 1
		note.pack()

		
		#ベスト選択アンド評価部分
		bestevaluate = Tk.Frame(self) #bestの選択評価部分のフレーム
		bestbtn = Tk.Button(bestevaluate, text=u"最も良い候補を選択する", command=self.bestselect)
		bestbtn.pack(side=Tk.LEFT)
		bestevaluate.pack(side=Tk.LEFT)
		#選択した候補の印象反映評価
		bestevaluate2 = Tk.Frame(self)
		bestimpression = Tk.Label(bestevaluate2, text=u"最もいいと思った候補がどの程度印象を反映しているか評価してください")
		bestimpression.pack()
		self.abhyouka = Tk.IntVar()
		self.abhyouka.set(0)
		num = -2
		for i in ["self.abRadio1", "self.abRadio2", "self.abRadio3", "self.abRadio4", "self.abRadio5"]:
			i = Tk.Radiobutton(bestevaluate2, text=str(num), variable=self.abhyouka, value=num)
			i.pack(side=Tk.LEFT)
			num = num + 1
		bestevaluate2.pack()

		#決定ボタン
		decide = Tk.Button(self, text=u"修正実行", command=self.sendvalue)
		decide.pack(anchor=Tk.SE)



	def bestselect(self):
		listname = [u"候補１", u"候補２", u"候補３", u"候補４", u"候補５", u"候補６", u"候補７", u"候補８", u"候補９", u"候補１０"]
		if not self.EXIST_OR_NOT:
			self.bestslct = Tk.Toplevel()
			self.bestslct.title('best決定')
			bestlabel = Tk.Label(self.bestslct, text=u'最もあなたの考える印象を反映している候補を選んでください', bg='white')
			bestlabel.pack()
			self.listbx = Tk.Listbox(self.bestslct)
			self.listbx.insert(Tk.END, *listname)
			self.listbx.pack(pady=10)
			

			self.EXIST_OR_NOT = self.bestslct.winfo_exists() #サブウィンドウが開いていればtrueを返す

			#ベスト選択終了処理、値取得+ウィンドウ閉じなど
			bestdecide = Tk.Button(self.bestslct, text=u'決定', command=self.changeFlag)
			bestdecide.pack()
			self.bestslct.protocol('WM_DELETE_WINDOW', self.changeFlag)



		#ここでベストの候補の配列番号を返す
	def changeFlag(self):
		#リストの情報抽出
		self.bestnum = self.listbx.curselection() #タプル形式で帰ってくる
		self.bestnum = self.bestnum[0] #bestの候補番号（配列）
		#終了処理
		self.EXIST_OR_NOT = False
		self.bestslct.destroy()


	def sendvalue(self):
		self.abhyouka_kakutei = self.abhyouka.get() #bestの印象反映評価値
		print "bestの候補番号"
		print self.sampimg[self.bestnum]
		print "印象反映度"
		print self.abhyouka_kakutei
		self.master.destroy()






#２回目以降のウィンドウ
class App2(App):
	def __init__(self, sampimg, prebest, master=None):
		App.__init__(self, sampimg, master=None)
		self.prebest= prebest
		self.n = len(sampimg)

	def display2(self):
		#相対評価部分
		#self.rehyouka =  numpy.zeros(self.n) #相対評価の値の入ったオブジェクト用リスト
		self.rehyouka = []
		for i in range(self.n):
			self.rehyouka.insert(i, 0) 
		for i in range(self.n):
			self.rehyouka[i] = Tk.IntVar()
			self.rehyouka[i].set(i+1)
		num = -1
		for j in range(self.n):
			reRadioFrame = Tk.Frame(self.f[j])
			for i in ["self.reRadio"+str(j+1)+"_1", "self.reRadeo"+str(j+1)+"_2", "self.reRadio"+str(j+1)+"_3"]:
				i = Tk.Radiobutton(reRadioFrame, text=str(num), variable=self.rehyouka[j], value=num)
				i.pack(side=Tk.LEFT)
				num = num + 1
			reRadioFrame.grid(row=2,column=0,columnspan=2)
			num = -1

		#前回のベスト画像表示
		w1 = 288 #front画像表示サイズ
		h1 = 288 #front画像表示サイズ
		w2 = 144 #side,back画像表示サイズ
		h2 = 144 #side,back画像表示サイズ
		imgname1 = "sample" + str(self.prebest) + "_front.jpeg"
		imgname2 = "sample" + str(self.prebest) + "_side.jpeg"
		imgname3 = "sample" + str(self.prebest) + "_back.jpeg"
		image1 = Image.open(imgname1)
		image2 = Image.open(imgname2)
		image3 = Image.open(imgname3)
		image1 = image1.resize((w1,h1))
		image2 = image2.resize((w2,h2))
		image3 = image3.resize((w2,h2))
		preBestFrame1 = Tk.LabelFrame(self.tag1, text="前世代のBEST", fg="red")
		preBestFrame2 = Tk.LabelFrame(self.tag2, text="前世代のBEST", fg="red")
		preBestFrame1.grid(row=1, column=2)
		preBestFrame2.grid(row=1, column=2)
		self.imageF1 = ImageTk.PhotoImage(image1)
		self.imageS1 = ImageTk.PhotoImage(image2)
		self.imageB1 = ImageTk.PhotoImage(image3)
		il11 = Tk.Label(preBestFrame1, image=self.imageF1)
		il12 = Tk.Label(preBestFrame1, image=self.imageS1)
		il13 = Tk.Label(preBestFrame1, image=self.imageB1)
		il11.grid(row=0, column=0, rowspan=2)
		il12.grid(row=0, column=1)
		il13.grid(row=1, column=1)
		il21 = Tk.Label(preBestFrame2, image=self.imageF1)
		il22 = Tk.Label(preBestFrame2, image=self.imageS1)
		il23 = Tk.Label(preBestFrame2, image=self.imageB1)
		il21.grid(row=0, column=0, rowspan=2)
		il22.grid(row=0, column=1)
		il23.grid(row=1, column=1)

	#入力値を引き渡す
	def sendvalue(self):
		#現世代のベストに関する評価の引き渡し
		self.abhyouka_kakutei = self.abhyouka.get() #bestの印象反映評価値
		print "bestの候補番号"
		print self.sampimg[self.bestnum]
		print "印象反映度"
		print self.abhyouka_kakutei
		#相対評価の引き渡し
		self.rehyouka_kakutei = numpy.zeros((self.n,),dtype=numpy.int)
		for i in range(self.n):
			self.rehyouka_kakutei[i] = self.rehyouka[i].get()
			print "サンプル"+str(self.sampimg[i])+"のBESTに対する相対評価：" + str(self.rehyouka_kakutei[i]) 
		self.master.destroy()




		






if __name__ == '__main__':
	sample = [1,2,3,4,5,6,545]
	firstmd = App(sample)
	firstmd.display()
	firstmd.pack()
	firstmd.mainloop()

	best = firstmd.sampimg[firstmd.bestnum]
	app = App2(sample,best)
	app.display()
	app.display2()
	app.pack()
	app.mainloop()