# -*- coding: utf-8 -*-
#
#	   mainWindow.py
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
from ttk import *
import ttk
import sendMail
from composer import Composer
import tkSimpleDialog
import ConfigParser, tkFileDialog, pickle, emailAccount

class MainWindow(Frame):
	config = ConfigParser.SafeConfigParser()
	def __init__(self, master):
		"""
		Constructor.

		master -- the root Tk() instance.
		"""
		self.master = master
		self.setup_widgets()
		self.setup_account_sys()
		

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
		

		self.tbbuttons =[
							["Send", self.send_mail],
							['Get Mail', self.get_mail],
							['Write', self.compose]
						]
		self.toolbar = Toolbar(self.master, self.tbbuttons)
		self.toolbar.pack(side=TOP, fill=X)



		self.panes = ttk.PanedWindow(self.master, orient = HORIZONTAL)
		self.panes.pack(side=TOP, fill=BOTH, expand = 1)

		self.mailboxList = Listbox(self.panes)
		self.panes.add(self.mailboxList)
		self.mailboxList.insert(END, "Inbox")

		self.messagePanes = ttk.PanedWindow(self.panes, orient = VERTICAL)
		self.messageList = Listbox(self.messagePanes)
		self.messageView = Text(self.messagePanes)
		self.messagePanes.add(self.messageList)
		self.messagePanes.add(self.messageView)
		self.panes.add(self.messagePanes)
		
		self.status.pack(side=BOTTOM, fill=X)

		self.status.set("Welcome to Frequency!")

	def send_mail(self):
		"""
		Main mail driver.
		"""
		password = tkSimpleDialog.askstring("Password?", "Please give your email's password.", show = '*')
		try:
			self.outbox.send_all(password)
			self.status.set("All mail sent!")
		except:
			self.status.set("Mail sending failed.")


	def setup_account_sys(self):
		self.currentAccount = None
		self.config.read('config.ini')
		import pdb; pdb.set_trace()
		accountFile = None
		while accountFile == None:
			try:
				accountFile = self.config.get('Settings', 'Account')
			except:
				#fix the configuration file
				self.set_default_account()
		self.load_account(accountFile)
		self.status.set("Default account " + self.currentAccount.name + " loaded.")

	def compose (self):
		""" Launches the composer. """
		try:
			compose = Composer(self.currentAccount, self.master)
			self.outbox.add(compose.returned)
			self.status.set('Composition successful. Message now in outbox.')
		except:
			self.status.set('Composition failed.')


	def open_account(self):
		"""
		Asks for an account to load, then loads it.
		"""
		realfile = tkFileDialog.askopenfilename(title = "Open..")
		try:
			self.load_account(realfile)
		except IOError:
			emailAccount.new(self.master)
		self.status.set("Account loaded.")

	def load_account(self, datafile):
		"""
		Loads the account and makes it the current account.

		datafile -- the path of the account file.
		"""
		try:
			self.currentAccount = pickle.load(open(datafile, "r"))
			self.inbox = emailAccount.attach_inbox(self.currentAccount)
			
		except AttributeError:
			self.open_account()

	def set_default_account (self):
		""" Sets the default account for the session and future
		sessions, using the configuration file. """
		
		if self.currentAccount == None:
			self.open_account()
		try:
			self.config.set('Settings','Account',self.currentAccount.name)
		except ConfigParser.NoSectionError:
			self.config.add_section('Settings')
			self.config.set('Settings','Account',self.currentAccount.name)
		configfile = open("config.ini", 'w+')
		self.config.write(configfile)
		self.status.set("Current account set as default.")

	def get_mail (self):
		"""
		Gets the email, prints it out.
		"""
		self.inbox.retrieve_mail()
		for mailmessage in self.currentAccount.inbox:
			print mailmessage

if __name__ == '__main__':
	app = Tk()
	win = MainWindow(app)
	app.mainloop()
