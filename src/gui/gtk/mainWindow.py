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
import pygtk
from composer import Composer
import emailAccount
import messageView
import sendMail
import tkSimpleDialog
import rfc822

import pygtk
pygtk.require('2.0')
import gtk

class MainWindow(object):

	
	def __init__(self):
		self.create_widgets()
#		self.setup_account_manager()
#		self.outbox = sendMail.Outbox(self.acctManager.currentAccount)
#		self.inboxes = sendMail.Inbox(self.acctManager.currentAccount, self.master, self.progress)
#		self.get_mailboxes()
		
	def create_widgets(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('frequencyui.xml')
		self.window = self.builder.get_object('BoxWindow')
		self.builder.connect_signals(self)
		self.window.show_all()
	
	def main(self):
		gtk.main()
		

	def quit_cb(self, event):
		gtk.main_quit()
	
if __name__ == '__main__':
	main = MainWindow()
	main.main()
