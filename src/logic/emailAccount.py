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

class EmailAccountManager(account.AccountManager):
	def __init__(self, gui, configfile = 'AccountConfig.ini'):
		self.gui = gui
		account.AccountManager.__init__(self, configfile)
		

	def new_account (self, default = False, welcome = False):
		""" Creates a new email account. """
		if self.currentAccount:
			self.currentAccount.save()
		if welcome:
			self.gui.dialogs.welcome()
			
		popup = self.gui.dialogs.settings()
		accountDefs = {'email': popup.email, 'type': popup.type, 'in_server': popup.server, 'in_port': popup.port, 'out_server': popup.smtp_server, 'out_port': popup.smtp_port}
		#TODO : Fix this rubbish so that the account dialog returns a dict
		askname= self.gui.dialogs.askString("Account", "Please give a name to the account.")
		mboxdir =  os.path.splitext(askname)[0] + "Mail"
		self.currentAccount = account.Account(self)
		self.currentAccount.add_item('name', askname)
		self.currentAccount.add_item('mboxdir', mboxdir)
		for x in accountDefs:
			print x
			self.currentAccount.add_item(x, accountDefs[x])
		
		if default:
			self.set_as_default()
		
		self.save_account()

	def choose_account (self):
		""" asks for a file to load. If there is no file, it makes a new one. """
		self.gui.dialogs.warn(
			'Oh, no!',
			"""There seems to be a problem with the configuration file and I can't load the default account.\nDon't worry, though, just choose the correct account you want to be default.\nIf there is none, click cancel.""")
		self.accountFile = self.gui.dialogs.openfile(title = "Open account file...")
		self.open_account_file(self.accountFile)


if __name__ == "__main__":
	root = Tk()
	manager = EmailAccountManager(root)

