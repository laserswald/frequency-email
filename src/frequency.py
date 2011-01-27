

#TODO: make loading file, and finish prompts for version 0.1
#TODO: turn current frame work to the compsition frame. Use Toplevel.
from Tkinter import *
from ttk import *
import mainWindow

class Frequency:
	def __init__(self, master):
		s = Style()
		print s.theme_names()
		s.theme_use('xpnative')
		start = mainWindow.MainWindow(master)
		



if __name__ == "__main__":
	root = Tk()
	frequency = Frequency(root)
	root.mainloop()
