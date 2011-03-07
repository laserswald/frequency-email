import Tkinter
from Tkinter import *
from ttk import *
from PIL import Image, ImageTk

class ToolFrame(Frame):
	itemdefs = []
	items = []
	def __init__(self, master, vertical=False, buttons = None):
		Frame.__init__(self, master, borderwidth=2, relief='raised')
		self.vert = vertical
		if buttons is not None:
			self.items = buttons
		else:
			self.items = []
		self.pack_all()

	def insert(self, label = '', action = None, type = None, image = None):
		self.items.append([label, action, type, image])
		self.clear_drawn()
		self.pack_all()


	def clear_drawn(self):
		"""deletes all the stuff in the toolbar and redraws."""
		for childname in self.winfo_children():
			widget = self.nametowidget(childname)
			widget.destroy()

	def pack_all(self):
		""" packs the items in the toolbar. """
		if self.items:
			for defin in self.items:
				temp = self.parse_definition(defin)
				if self.vert:
					temp.pack(side = TOP, fill = Y)
				else:
					temp.pack(side = LEFT, fill = X)
		else:
			pass
			
	def map_items(self, defs):
		'''
		adds items in defs to the items in the toolframe.
		'''
		for item in self.itemdefs:
			self.items.append(temp)
	
	def parse_definition(self, defin):
		'''
		Returns a control when given a Toolframe definition.
		'''
		if defin[2] == 'Button' or defin[2] == None:
			temp = Button(self, text = defin[0], command = defin[1])
		elif defin[2] == 'Entry':
			temp = Entry(self, label = defin[0])
		elif defin[2] == 'MenuButton':
			temp = Menubutton(self, text = defin[0], menu = defin[1])			
		if defin[3]:
			img = defin[3]
			temp.config(image = img, compound = 'left')
		return temp
	
	
	def delete(self, buttonNumber):
		""" Function Documentation """
		self.buttons.delete


class ToolButton(Button):
	""" A toolbutton with the default stuff. """

	def __init__ (self, label = 'ToolButton', command = None):
		""" Class initialiser """
		Button.__init__(self, text = text, command = command)

# get button stuff
# then make the button stuff global
# refresh
if __name__ == "__main__":
	root = Tk()
	this = ToolFrame(root, buttons = [["Testing", None, 'Button', None]])
	this.pack(side = TOP)
	#this.refresh()
	root.mainloop()
