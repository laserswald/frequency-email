
from Tkinter import *
from ttk import *
from PIL import Image, ImageTk

class ToolFrame(Frame):
	itemdefs = []
	items = []
	def __init__(self, master, vertical=False, buttons = None):
		Frame.__init__(self, master, borderwidth=1)
		
		
		
		self.vert = vertical
		if buttons is not None:
			self.items = buttons
		else:
			self.items = []
		self.pack_all()

	def insert(self, item):
		self.items.append(item)
		self.pack_all()


	def clear(self):
		"""deletes all the stuff in the toolbar and redraws."""
		for childname in self.winfo_children():
			widget = self.nametowidget(childname)
			widget.destroy()

	def pack_all(self):
		""" packs the items in the toolbar. """
		if self.items:
			for item in self.items:
				if self.vert:
					item.pack(side = TOP, fill = Y)
				else:
					item.pack(side = LEFT, fill = X)
		else:
			pass
			
	def map_items(self, defs):
		'''
		adds items in defs to the items in the toolframe.
		'''
		for item in defs:
			self.items.append(item)	
	
	def delete(self, buttonNumber):
		""" Function Documentation """
		self.buttons.delete

	def minimize(self):
		pass
	
	def pop_out(self):
		pass
		
	def pop_in(self):
		pass

class ToolItem(Widget):
	pass
		
class ToolButton(Button):
	""" A toolbutton with the default stuff. """
	def __init__ (self, toolbar, label = 'ToolButton', command = None):
		""" Class initialiser """
		Button.__init__(self, master = toolbar, text = label, command = command)
		
class ToolImageButton(Button):
	def __init__(self, toolbar, label = "ToolMenuButton", command = None, image = None):
		Button.__init__(self, master = toolbar, text = label, command = command)
		self.config(image = image)

class ToolMenu(Menubutton):
	def __init__ (self, toolbar, label = 'ToolMenu', command = None):
		Menubutton.__init__(self,  master = toolbar, text = label, command = command)


# get button stuff
# then make the button stuff global
# refresh
if __name__ == "__main__":
	root = Tk()
	this = ToolFrame(root)
	print this
	button = ToolButton(this, label = "Send/Recieve")	
	this.pack(side = TOP, expand = 0)
	this.insert(button)
	root.mainloop()
