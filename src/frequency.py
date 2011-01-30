def main(toolkit):
	if toolkit == 'tk':
		import gui.tk.mainWindow as mainWin
	elif toolkit == 'wx':
		import gui.wxgui.mainWindow as mainWin
	elif toolkit == 'gtk':
		import gui.gtk.mainWindow as mainWin
	
	mainWin.start()
	
if __name__ == "__main__":
	main('wx')
