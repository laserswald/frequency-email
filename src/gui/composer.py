#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       composer.py
#
#       Copyright 2010 Ben Davenport-Ray <laserdude11@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from Tkinter import *
from ttk import *
from Tkconstants import *
from toolbar import *
import tkFileDialog, ScrolledText, tkSimpleDialog
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders, message_from_file

import pickle

QUEUE = None



class Composer(Toplevel):
	def __init__(self, account, master = None):
		""" This starts up the main frame and widgets."""
		Toplevel.__init__(self)
		self.transient(master)
		self.account = account
		self.setupWidgets()
		self.grab_set()
		self.wait_window(self)


	def setupWidgets(self):
		self.title("Compose Mail")
		self.maintext = ScrolledText.ScrolledText(self, state=NORMAL)

		self.tbbuttons =[
							['Send!', self.send],
							["Open", self.open_mail],
							["Save", self.save_mail],
							["Add Address", self.new_button_cb]
						]


		self.toolbar = Toolbar(self, self.tbbuttons)
		self.toolbar.pack(side=TOP, fill=X)

		self.addressBox = Listbox(self)
		self.addressBox.pack(side=TOP, fill=X)


		self.subjectBox = Entry(self)
		self.subjectBox.pack(side=TOP, fill=X)

		self.maintext.pack(side=TOP, fill=BOTH,expand = 1)
		self.menubar = Menu(self)

		self.filemenu = Menu(self.menubar)
		self.filemenu.add_command(label = "Save", command = self.save_mail)

		self.menubar.add_cascade(label = "File", menu = self.filemenu)
		self.config(menu = self.menubar)

	def send (self):
		""" closes the window and places the mail in the queue. """
		self.returned = self.convert_to_message()
		self.destroy()

	def convert_to_message (self, flatten = False):
		""" converts all the stuff into a message for sending/saving/whatever """
		m = MIMEMultipart()
		m['To'] = ", ".join(self.addressBox.get(0, END))
		m['Subject'] = self.subjectBox.get()
		m['From'] = self.account.email
		m.attach(MIMEText(self.maintext.get(1.0, END)))
		if flatten == True:
			flatm = m.as_string(True)
			return flatm
		else:
			return m
		
	def save_mail(self): #Save mail as a text file.
		text = self.convert_to_message(flatten = True)
		self.savefile = tkFileDialog.asksaveasfilename(title = "Save as..")
		if self.savefile != "":
			self.newmessage = open(self.savefile, "w+")
			self.newmessage.write(text)
			self.newmessage.close()

	def open_mail(self):
		self.openfile = tkFileDialog.askopenfilename(title = "Open Mail..", )
		if self.openfile != "":
			openmessage = open(self.openfile, "r+")
			parsedFile = message_from_file(openmessage)

			#Load the addresses
			self.addressBox.delete(0, END)
			addresses = parsedFile['to'].split(', ')
			for addr in addresses:
				self.addressBox.insert(END, addr)

			#set the subject field to the parsed email's subject.
			self.subjectBox.delete(0, END)
			self.subjectBox.insert(END, parsedFile['Subject'])

			#set the main text field to the text portion of the file. it is assumed to be first.
			#
			self.maintext.delete("1.0", END)
			payloadText = ''
			for part in parsedFile.walk():
				if part.get_content_maintype() == 'multipart':
					continue
				if part.get_content_type() == 'text/plain':
					payloadText += part.get_payload(decode = True)
			self.maintext.insert(END, payloadText)

	def new_button_cb(self):
		buttonname = tkSimpleDialog.askstring("Email", "What should the email be?")
		if buttonname is not None:
			self.addressBox.insert(END, buttonname)

	def to_addr_button_cb(self):
		""" Deletes the address from the address bar. """
		pass



if __name__ == '__main__':
	root = Tk()
	app = Composer(root)
	root.mainloop()

