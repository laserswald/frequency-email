# -*- coding: utf-8 -*-
#
#	  mainWindow.py
#
#	   Copyright 2010 Ben Davenport-Ray <laserdude11@gmail.com>
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
from ttk import *
from TabbedToolbar import Ribbon
from statusbar import StatusBar
from msglist import MessageList
from PIL import Image, ImageTk
import dialogs
import os

class MainWindow(object):

	def __init__(self, logic):
		self.master = Tk()
		self.logic = logic
		self.dialogs = dialogs.DialogManager(self.master)
		self.setup_widgets()
		

		
	def setup_widgets (self):
		"""
		Sets up all the user interface in the main window.
		"""
		
		#Sets up most of the main frame stuff.
		self.master.title("Frequency")
		self.master.iconbitmap("icons/Frequency.ico")
		self.master.columnconfigure(0, weight = 1)
		self.master.rowconfigure(1, weight = 1)
		self.setup_icons()
		
		
		self.ribbon = Ribbon(self.master)		
		self.AccountMenu = Menu()
		self.AccountMenu.add_command(label = "Add...", command = self.logic.new_account)
		self.AccountMenu.add_command(label = "Remove...", command = self.logic.rem_account)		
		self.ribbon.menu.add_command("Send/Recieve", self.logic.send_receive, icon = self.email_icon)		
		self.ribbon.menu.add_cascade(label = "Account", menu = self.AccountMenu)
		self.ribbon.menu.add_command('Options', self.logic.options, icon = self.wrench_icon)
		self.ribbon.menu.add_command("Exit", self.logic.quit, icon = self.door_in_icon)
		std = self.ribbon.toolbar.add_page('Standard')
		mailTools = self.ribbon.toolbar.add_toolframe(std)
		mailTools.insert('Compose', self.logic.compose, 'Button', self.email_edit_icon)
		mailTools.insert('Get Mail', self.logic.receive, 'Button', self.connect_icon)
		self.ribbon.set_main_icon('icons/table.png')
		self.ribbon.grid(columnspan = 2, sticky = N+S+E+W)		
		
		#Sets up the main frames for stuff.
		self.panes = PanedWindow(self.master, orient = HORIZONTAL)
		self.mailboxTree = Treeview(self.panes,
									show = 'tree headings')
		self.mailboxTree.bind(('<3>'), self.logic.box_rightclick)
		self.mailboxTree.bind("<<TreeviewSelect>>", self.logic.box_selected)
		self.panes.add(self.mailboxTree)
		
		
		self.rightpanes = PanedWindow(self.master, orient = VERTICAL)
		self.messageList = MessageList(self.rightpanes)
		self.messageList.bind("<<TreeviewSelect>>", self.logic.message_selected)
		self.rightpanes.add(self.messageList)
		self.panes.add(self.rightpanes)
		self.progressBar = Progressbar(self.master, mode='determinate')
		self.progressBar.grid(row = 2, column = 1, sticky = 'ew')
		self.status = StatusBar(self.master)
		self.status.grid(row = 2, sticky = E+W)
		self.panes.grid(row = 1, column = 0, columnspan = 2, sticky = N+S+E+W)
		self.update_status("Welcome to Frequency!")

	def sortby(self, tree, col, descending):
		"""Sort tree contents when a column is clicked on."""
		# grab values to sort
		data = [(tree.set(child, col), child) for child in tree.get_children('')]
		if col == 'Date':
			newData = []
			for index, item in enumerate(data):
				date = item[0]
				dataitem = (rfc822.parsedate(date), index, item)
				newData.append(dataitem)

			newData.sort(reverse=descending)
			for set in enumerate(newData):
				print set
				parsedate, indx, item = set
				tree.move(item[1], '', indx)
		# reorder data
		data.sort(reverse=descending)
		for indx, item in enumerate(data):
			tree.move(item[1], '', indx)

		# switch the heading so that it will sort in the opposite direction
		tree.heading(col,
			command=lambda col=col: self.sortby(tree, col, int(not descending)))
			
	def setup_icons(self):		
		self.email_icon = ImageTk.PhotoImage(Image.open('icons/email.png'))
		self.email_add_icon = ImageTk.PhotoImage(Image.open('icons/email_add.png'))
		self.email_delete_icon = ImageTk.PhotoImage(Image.open('icons/email_delete.png'))
		self.email_attach_icon = ImageTk.PhotoImage(Image.open('icons/email_attach.png'))
		self.email_edit_icon = ImageTk.PhotoImage(Image.open('icons/email_edit.png'))
		self.door_in_icon =  ImageTk.PhotoImage(Image.open('icons/door_in.png'))
		self.user_icon = ImageTk.PhotoImage(Image.open('icons/user.png'))
		self.wrench_icon = ImageTk.PhotoImage(Image.open('icons/wrench.png'))
		self.connect_icon = ImageTk.PhotoImage(Image.open('icons/connect.png'))
		
	def update_status(self, status):
		'''
		proxy for Statusbar.set
		'''
		self.status.set(status)
		
	def set_progress(self, maximum):
		self.progressBar.config(maximum = maximum)
		
	def	progress_step(self, stepa = None):
		if stepa is not None:
			self.progressBar.step(stepa)
		else:
			self.progressBar.step()
	
	def quit(self):
		self.master.destroy()
				
	def start(self):
		self.master.mainloop()
		return self
		
if __name__ == "__main__":
	mw = MainWindow(None)
	mw.start()