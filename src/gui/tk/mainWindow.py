# -*- coding: utf-8 -*-
#
#	  mainWindow.py
#	   
#	   Copyright 2010 Ben Davenport-Ray <ben@benslaptop>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.
from Tkinter import * 
from toolbar import *
from statusbar import *
from logic import sendMail, emailAccount
from logic.mainLogic import MainWindowLogic as mainLogic
from composer import Composer
import tkSimpleDialog
import ConfigParser, tkFileDialog, pickle

class MainWindow(Frame):
	
	def __init__(self, master):
		self.master = master
		self.setup_widgets()
		self.setup_account_manager()
		self.outbox = sendMail.Outbox(self.acctManager.currentAccount)
		self.inboxes = sendMail.Inbox(self.acctManager.currentAccount)
	
	def setup_widgets (self):
		""" 
		Sets up all the user interface in the main window.
		"""
		
		self.master.title("Email")


		self.menubar = Menu(self.master)
		self.filemenu = Menu(self.menubar)
		self.filemenu.add_command(label = "Account...")
		self.filemenu.add_command(label = "Exit", command = self.master.quit)
		self.menubar.add_cascade(label = "File", menu = self.filemenu)
		self.master.config(menu = self.menubar)
		
		self.status = StatusBar(self.master)
		self.status.pack(side = BOTTOM, fill = X)

		self.tbbuttons =[
							["Send", mainLogic.send],
							['Write', mainLogic.compose],
						]
		self.toolbar = Toolbar(self.master, self.tbbuttons)
		self.toolbar.pack(side=TOP, fill=X)
		
		self.mailboxList = Listbox(self.master)
		
		self.panes = PanedWindow(self.master, orient = HORIZONTAL)
		self.panes.add(self.mailboxList)
		self.rightpanes = PanedWindow(self.master, orient = VERTICAL)
		self.messageList = Listbox(self.master)
		self.messageView = Text(self.master)
		self.rightpanes.add(self.messageList)
		self.rightpanes.add(self.messageView)
		self.panes.add(self.rightpanes)
		#self.messageLis
		self.panes.pack(side=TOP, fill=BOTH, expand=1)
		self.status.set("Welcome to Frequency!")
		
	def getmail(self):
		boxname = self.mailboxTree.selection()[0]
	
	
	def compose (self):
		""" Launches the composer. """
		try:
			compose = Composer(self.acctManager.currentAccount, self.master)
			self.outbox.add(compose.returned)
			self.status.set('Composition successful. Message now in outbox.')
		except:
			self.status.set('Composition failed.')

	def setup_account_manager (self):
		""" sets up the Account management class. """
		self.acctManager = emailAccount.EmailAccountManager(self.master)
		
def start():	
	app = Tk()
	win = MainWindow(app)
	app.mainloop()		


