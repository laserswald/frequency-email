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
from Tkinter import *
import tkSimpleDialog
import tkFileDialog
import pickle
import os
import sendMail

class Account(object):
		
	def __init__(self, email, type, in_server, in_port, out_server, out_port):
		self.in_server = in_server
		self.in_port = in_port
		self.out_server = out_server
		self.out_port = out_port
		self.email = email
		self.type = type
		self.name = os.path.relpath(tkFileDialog.asksaveasfilename(title = "Save as.."))
		self.mboxDir = os.path.splitext(self.name)[0] + ".mail"	
		
		self.save()
	def save(self):
		#save account for later loading
		pickle.dump(self, open(self.name, "w"))


def attach_inbox (account):
        inbox = sendMail.Inbox(account)
        return inbox

class AccountError(Exception):
	def __init__(self, error):
		self.value = error


class NewAccountDialog(tkSimpleDialog.Dialog):
	
	def body(self, master):
		self.control = StringVar()
		Label(master, text="Email Address:").grid(row=0)
		self.em = Entry(master)
		self.em.grid(row = 0, column = 1)
		
		self.r1 = Radiobutton(master, text = 'POP Account', variable = self.control, value = "POP",)
		self.r2 = Radiobutton(master, text = 'IMAP Account', variable = self.control, value = "IMAP",)
		self.r1.grid(row=1, column=0)
		self.r2.grid(row=2, column=0)
		
		Label(master, text="Server:").grid(row=3)
		Label(master, text="Port:").grid(row=4)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e1.grid(row=3, column=1)
		self.e2.grid(row=4, column=1)
		
		Label(master, text="SMTP").grid(row=5)
		
		Label(master, text="Server:").grid(row=6)
		Label(master, text="Port:").grid(row=7)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e3.grid(row=6, column=1)
		self.e4.grid(row=7, column=1)
		

		return self.em # initial focus



	def apply(self):
		self.server = self.e1.get()
		self.port = self.e2.get()
		self.smtp_server = self.e3.get()
		self.smtp_port = self.e4.get()
		self.type = self.control.get()
		self.email = self.em.get()
		self.result = 1


def new(master):
	loadedAccount = None

	popup = NewAccountDialog(master, 'New Email Account')
	
	x = Account(popup.email, popup.type, popup.server, popup.port, popup.smtp_server, popup.smtp_port)
	return x

if __name__ == "__main__":
	
	root = Tk()
	new()
