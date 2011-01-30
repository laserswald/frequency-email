#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   emailAccount.py
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
#


import account
import os
import mainLogic

class EmailAccount(account.Account):
		
	def __init__(self, email, type, in_server, in_port, out_server, out_port):
		self.in_server = in_server
		self.in_port = in_port
		self.out_server = out_server
		self.out_port = out_port
		self.email = email
		self.type = type
		self.name = os.path.relpath(tkFileDialog.asksaveasfilename(title = "Save as.."))
		self.mboxDir = os.path.splitext(self.name)[0] + "Mail"	
		
		self.save()
	

class EmailAccountManager(account.AccountManager):
	def __init__(self, toolkit, configfile = 'AccountConfig.ini'):
		self.toolkit = toolkit
		mainLogic.MainWindowLogic.choose_toolkit(self, toolkit)
		account.AccountManager.__init__(self, configfile)
		
	def new_account (self, default = False):
		""" Creates a new email account. """
		if self.currentAccount:
			self.currentAccount.save()
		popup = gui.dialogs.EmailAccountDialog(self.master, 'New Email Account')		
		self.currentAccount = EmailAccount(popup.email, popup.type, popup.server, popup.port, popup.smtp_server, popup.smtp_port)
		if default:
			self.set_as_default()
				
	def choose_account (self):
		""" asks for a file to load. If there is no file, it makes a new one. """
		tkMessageBox.showwarning(
			'Oh, no!', 
			"""There seems to be a problem with the configuration file and I can't load the default account.\nDon't worry, though, just choose the correct account you want to be default.\nIf there is none, click cancel.""")
		self.accountFile = tkFileDialog.askopenfilename(title = "Open account file...")
		self.open_account_file(self.accountFile)
        
        
if __name__ == "__main__":	
	root = Tk()
	manager = EmailAccountManager(root)
