import Tkinter
from Tkinter import *

class Toolbar(Frame):
	buttons = []
	def __init__(self, master, buttons = None):
		Frame.__init__(self, master, borderwidth=2, relief='raised')
		if buttons is not None:			
			self.buttons = buttons
		else:
			return 1
		self.pack_all()
		
	def append(self, deff):
		self.buttons.append(deff)
		self.clear_drawn()
		self.pack_all()
		
		
	def clear_drawn(self):
		"""deletes all the stuff in the toolbar and redraws."""
		for childname in self.winfo_children():
			widget = self.nametowidget(childname)
			widget.destroy()
			
	def pack_all(self):
		""" Function Documentation """			
		for item in self.buttons:
			tempButton = Button(self, text = item[0], command = item[1])
			tempButton.pack(side = LEFT, fill = X)
			
	def delete(self, buttonNumber):
		""" Function Documentation """
		self.buttons.delete
		
def defaultCallback():
	""" Function Documentation """
	this.clear_drawn()
	print "toolbar cleared"
	this.pack_all()
	print "toolbar redrawn"
	
# get button stuff
# then make the button stuff global
# refresh
if __name__ == "__main__":
	root = Tk()
	this = Toolbar(root, [["Testing", defaultCallback]])
	this.pack(side = TOP)
	#this.refresh()
	root.mainloop()
