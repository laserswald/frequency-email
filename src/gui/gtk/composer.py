#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   composer.py
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

from email import message_from_file
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pygtk
pygtk.require('2.0')
import gtk


QUEUE = None


class Composer(gtk.Window):
	def __init__(self, account):
		""" This starts up the main frame and widgets."""
		self.account = account
		super(Composer, self).__init__()
		self.setupWidgets()



	def setupWidgets(self):

		self.set_title('Compose Mail')
#		self.maintext = ScrolledText.ScrolledText(self, state=NORMAL)
		self.mainText = gtk.TextView(buffer = None)
#		self.tbbuttons = [
#							['Send!', self.send, 'Button'],
#							["Open", self.open_mail, 'Button'],
#							["Save", self.save_mail, 'Button']
#						]
		self.uiManager = gtk.UIManager()
		self.mainAccelGroup = self.uiManager.get_accel_group()
		self.add_accel_group(self.mainAccelGroup)
		
		
		
#
#		self.toolbar = Toolbar(self, False, self.tbbuttons)
#		self.toolbar.pack(side=TOP, fill=X)
#
#		self.addressBox = Toolbar(self, False, [["Add Address", self.new_button_cb, 'Button']])
#		self.addressBox.pack(side = TOP, fill = X)
#		
#		self.subjectBox = Entry(self)
#		self.subjectBox.pack(side=TOP, fill=X)
#
#		self.maintext.pack(side=TOP, fill=BOTH, expand=1)
#		self.menubar = Menu(self)
#
#		self.filemenu = Menu(self.menubar)
#		self.filemenu.add_command(label="Save", command=self.save_mail)
#
#		self.menubar.add_cascade(label="File", menu=self.filemenu)
#		self.config(menu=self.menubar)

	def send (self):
		""" closes the window and places the mail in the queue. """
		self.returned = self.convert_to_message()
		self.destroy()
		
	def convert_to_message (self, flatten=False):
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
		text = self.convert_to_message(flatten=True)
		self.savefile = tkFileDialog.asksaveasfilename(title="Save as..")
		if self.savefile != "":
			self.newmessage = open(self.savefile, "w+")
			self.newmessage.write(text)
			self.newmessage.close()

	def open_mail(self):
		self.openfile = tkFileDialog.askopenfilename(title="Open Mail..",)
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
				if part.get_content_maintype() == 'text':
					payloadText += part.get_payload(decode=True)
			self.maintext.insert(END, payloadText)
			



			

	def new_button_cb(self):
		buttonname = tkSimpleDialog.askstring("Email", "What should the email be?")
		addressMenu = Menu()
		addressMenu.add_command(label = 'Remove Address', command = self.to_addr_button_cb)
		addressMenu.add_checkbutton(label = 'Save in Addressbook', command = self.add_to_address_book)
		
		if buttonname is not None:
			buttonTotal = [buttonname, addressMenu, 'MenuButton']
			self.addressBox.insert(buttonTotal)

	def to_addr_button_cb(self):
		""" Deletes the address from the address bar. """
		pass
	
	def add_to_address_book(self, event):
		pass
	



if __name__ == '__main__':
	root = Tk()
	app = Composer(root)
	root.mainloop()
