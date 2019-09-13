import ac

class deflabel:
	def __init__(self, parent, text, size, posx, posy, font, align):
		self.lbl = ac.addLabel(parent, str(text))
		ac.setPosition(self.lbl, posx, posy)
		if size:
			ac.setFontSize(self.lbl, size)
		if font:
			ac.setCustomFont(self.lbl, font, 0, 0)
		if align:
			ac.setFontAlignment(self.lbl, align)

class defbutton:
	def __init__(self, parent, text, sizex, sizey, posx, posy):
		self.btn = ac.addButton(parent, text)
		ac.setSize(self.btn, sizex, sizey)
		ac.setPosition(self.btn, posx, posy)

class deftowerbox:
	def __init__(self, parent, number):
		self.back = defbutton(parent, "", 320, 34, 0, number*34)
		ac.drawBorder(self.back.btn, 0)
		ac.setBackgroundTexture(self.back.btn, "apps/python/HoschTV/img/tower-back.png")
		ac.drawBorder(self.back.btn, 0)
		ac.setBackgroundOpacity(self.back.btn, 0)
		self.pos = deflabel(parent, str(number +1), 32, 17, 2+number*34, "voxbox", "center")
		ac.setFontColor(self.pos.lbl, 0, 0, 0, 1)
		if number>18:
			ac.setFontSize(self.pos.lbl, 19)
			ac.setPosition(self.pos.lbl, 17, 8+number*34)
		elif number>8:
			ac.setFontSize(self.pos.lbl, 26)
			ac.setPosition(self.pos.lbl, 17, 5+number*34)
		
		
		# ac.addOnClickedListener(self.back, focus(i))
		# ac.addOnClickedListener(self.back, focus(p[i+1]))
		# ac.addOnClickedListener(id, func)
		"""
		self.pos = ac.addLabel(ACtower, str(i+1))
		ac.setPosition(self.pos, 19, (40*i)+6)
		ac.setFontSize(self.pos, 25)
		ac.setCustomFont(self.pos, "Arial", 0, 0)
		ac.setFontAlignment(self.pos, "center")
		ac.setFontColor(self.pos, 0, 0, 0, 1)
		
		self.name = ac.addLabel(ACtower, "BSP")
		ac.setPosition(self.name, 40, (40*i)+4)
		ac.setFontSize(self.name, 29)
		ac.setCustomFont(self.name, "Arial", 0, 0)
		
		self.info = ac.addLabel(ACtower, "0:00.000")
		ac.setPosition(self.info, 116, (40*i)+6)
		ac.setFontSize(self.info, 25)
		ac.setCustomFont(self.info, "Arial", 0, 0)
		"""
		