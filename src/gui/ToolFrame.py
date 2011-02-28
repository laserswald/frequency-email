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
			self.itemdefs = buttons
		else:
			self.itemdefs = []
		self.pack_all()

	def insert(self, label = '', action = None, type = None, image = None):
		self.items.append(self.parse_definition([label, action, type, image]))
		self.clear_drawn()
		self.pack_all()


	def clear_drawn(self):
		"""deletes all the stuff in the toolbar and redraws."""
		for childname in self.winfo_children():
			widget = self.nametowidget(childname)
			widget.destroy()

	def pack_all(self):
		""" packs the items in the toolbar. """
		if self.itemdefs:
			

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
		if defin[2] == 'Button' or item[2] == None:
			temp = Button(self, text = item[0], command = item[1])
		elif defin[2] == 'Entry':
			temp = Entry(self, label = item[0])
		elif defin[2] == 'MenuButton':
			temp = Menubutton(self, text = item[0], menu = item[1])			
		if defin[3]:
			img = ImageTk.PhotoImage(Image.open(defin[3]))
			temp.config(image = img)
	
	
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
	this = ToolFrame(root, buttons = [["Testing", None, 'Button']])
	this.pack(side = TOP)
	#this.refresh()
	root.mainloop()
