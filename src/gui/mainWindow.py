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
import tkMessageBox
from PIL import Image, ImageTk
import os
import dialogs


class MainWindow(object):

	def __init__(self, logic):
		
		self.logic = logic


	def setup_widgets (self):
		"""
		Sets up all the user interface in the main window.
		"""
		
		self.master.title("Email")
		if os.name == "nt":
			self.master.iconbitmap("/icons/Frequency.ico")
		self.dialogs = dialogs.DialogManager(self.master)
		#self.setupIcons()
		
		self.master.grid_rowconfigure(1, weight = 1)
		self.master.grid_columnconfigure(0, weight = 1)
		self.filemenu = Menu()
		self.AccountMenu = Menu(self.filemenu)
		
		
		self.filemenu.add_command(label = "Send/Recieve",  compound = LEFT)		
		self.filemenu.add_cascade(label = "Account", menu = self.AccountMenu)
		self.filemenu.add_command(label = 'Options', compound = LEFT)
		self.filemenu.add_command(label = "Exit",  compound = LEFT)
		
		self.TopButton = Menubutton(text = 'Frequency',
									menu = self.filemenu, 
									
									compound = LEFT)
		self.TopButton.grid(row = 0, column = 0, sticky = W+N)
									
		self.panes = PanedWindow(self.master, orient = HORIZONTAL)

		self.mailboxTree = Treeview(self.panes,
									show = 'tree headings')

		#self.mailboxTree.bind("<<TreeviewSelect>>", self.box_selected)



		self.panes.add(self.mailboxTree)
		self.rightpanes = PanedWindow(self.master, orient = VERTICAL)



		self.messageColumns = ('Subject',
							'From',
							'To',
							'Date')
		self.messageList = Treeview(self.master,
									columns = self.messageColumns,
									show = 'headings')
		for heading in self.messageColumns:
			self.messageList.heading(heading, text = heading)
		self.messageList.bind("<<TreeviewSelect>>", self.message_selected)


		self.rightpanes.add(self.messageList)
		self.panes.add(self.rightpanes)
		#self.messageLis
		self.panes.grid(row = 1, column = 0, sticky = N+S+E+W)
		#self.status.set("Welcome to Frequency!")
		


	def message_selected(self, event):
		item = self.messageList.selection()
		index = int(item[0].strip('I'))-1
		key = self.messageKeys[index]
		displayedMessage = self.inboxes.get_message(key)
		self.mView = messageView.MessageView(self.master)
		self.mView.load_from_message(displayedMessage)

	def get_mailboxes(self):
		self.boxlist = self.inboxes.retrieve_mailboxes()
		for box in self.boxlist:
			hie = box.split('/')
			if len(hie) == 2:
				folder, mailbox = hie
			elif len(hie) == 1:
				folder = ''; mailbox = hie[0]
			self.mailboxTree.insert(folder, 'end', mailbox, text=mailbox)


	def box_selected(self, event):
		self.messageKeys = []
		boxname = event.widget.selection()[0]
		while True:
			try:
				self.selectedBox = self.inboxes.get_folder(boxname)
				break
			except:
				self.inboxes.add_folder(boxname)
		try:
			self.messageList.set_children('')
		except:
			print 'no items'
		for key, message in self.selectedBox.iteritems():
			treevalues = (message['Subject'],
						message['From'],
						message['Date'])
			self.messageList.insert('', 'end', values=treevalues)
			self.messageKeys.append(key)
		self.status.push(self.mailContext, 'Messages for folder %s loaded.' % boxname)

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
			
	def setupIcons(self):
		print os.getcwd()
		self.email_icon = ImageTk.PhotoImage(Image.open('src/icons/email.png'))
		self.email_add_icon = ImageTk.PhotoImage(Image.open('src/icons/email_add.png'))
		self.email_delete_icon = ImageTk.PhotoImage(Image.open('src/icons/email_delete.png'))
		self.email_attach_icon = ImageTk.PhotoImage(Image.open('src/icons/email_attach.png'))
		self.email_edit_icon = ImageTk.PhotoImage(Image.open('src/icons/email_edit.png'))
		self.door_in_icon =  ImageTk.PhotoImage(Image.open('src/icons/door_in.png'))
		self.user_icon = ImageTk.PhotoImage(Image.open('src/icons/user.png'))
		self.wrench_icon = ImageTk.PhotoImage(Image.open('src/icons/wrench.png'))


		
	def start(self):
		self.master = Tk()
		self.setup_widgets()
		self.master.mainloop()
		return self
		
if __name__ == "__main__":
	mw = MainWindow(None)
	mw.start()
