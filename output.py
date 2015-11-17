#! /usr/bin/env python
# coding: utf-8
     
import Tkinter as Tk
from PIL import Image, ImageTk
from ttk import *
import sys


class App(Tk.Frame):

	EXIST_OR_NOT = False  #ウィンドウの二重展開防止のための関数
	#bestok = False #bestが選ばれたかどうか

	#ウィンドウ全体の設定
	def __init__(self,smpimg,master=None):
		Tk.Frame.__init__(self, master)
		self.master.title(u'ヘアデザインシステム')
		self.master.geometry("1440x900")
		self.sampimg = smpimg
		self.display()

	def display(self):
		w1 = 288 #front画像表示サイズ
		h1 = 288 #front画像表示サイズ
		w2 = 144 #side,back画像表示サイズ
		h2 = 144 #side,back画像表示サイズ
		self.img_f = [0,0,0,0,0,0,0,0,0,0]  #前の画像番号
		self.img_s = [0,0,0,0,0,0,0,0,0,0]  #横の画像番号
		self.img_b = [0,0,0,0,0,0,0,0,0,0]  #後ろの画像番号
		fn = 0  #frame番号
		f = [0,0,0,0,0,0,0,0,0,0] #画像のラベルを乗っけるフレーム
		note = Notebook(self)
		tag1 = Tk.Frame(note)
		tag2 = Tk.Frame(note)
		note.add(tag1, text=u"ページ１")
		note.add(tag2, text=u"ページ２")

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
				f[fn] = Tk.LabelFrame(tag1, text=u"候補"+str(fn+1))
				if fn < 3:
					f[fn].grid(row=0,column=fn, padx=5, pady=10)
				else:
					f[fn].grid(row=1,column=fn%3, padx=5, pady=10)
			else:
				f[fn] = Tk.LabelFrame(tag2, text=u"候補"+str(fn+1))
				if fn < 8:
					f[fn].grid(row=0,column=fn%5, padx=5, pady=10)
				else:
					f[fn].grid(row=1,column=fn%8, padx=5, pady=10)
			self.img_f[fn] = ImageTk.PhotoImage(image1)
			self.img_s[fn] = ImageTk.PhotoImage(image2)
			self.img_b[fn] = ImageTk.PhotoImage(image3)
			il1 = Tk.Label(f[fn], image=self.img_f[fn])
			il2 = Tk.Label(f[fn], image=self.img_s[fn])
			il3 = Tk.Label(f[fn], image=self.img_b[fn])
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
		abhyouka = Tk.IntVar()
		abhyouka.set(0)
		num = -3
		for i in ["abRadio1", "abRadio2", "abRadio3", "abRadio4", "abRadio5", "abRadio6", "abRadio7"]:
			i = Tk.Radiobutton(bestevaluate2, text=str(num), variable=abhyouka, value=num)
			i.pack(side=Tk.LEFT)
			num = num + 1
		bestevaluate2.pack()



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



if __name__ == '__main__':
	sample = [1,2,3,4,5,6,7,8,9,10]
	app = App(sample)
	app.pack()
	app.mainloop()