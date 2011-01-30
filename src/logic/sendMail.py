#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   sendMail.py
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

import smtplib
import poplib
import imaplib
import mailbox
import tkSimpleDialog
from ttk import Label, Progressbar
import tkMessageBox


	

class SubMailBox:
	pass

class Inbox(mailbox.Maildir):
	"""
	This class represents a maildir mailbox with convenience functions for getting mail.
	"""
	total = 0
	loaded = 0

	def __init__(self, account, master):
		"""
		Constructor.
		
		account -- An account to bind this mailbox to.
		"""
		self._account = account
		mailbox.Maildir.__init__(self, self._account.mboxDir, factory = mailbox.MaildirMessage)

	def retrieve_mailboxes(self):
		"""
		Retrieves mailboxes and returns a list of them.
		"""
		self.mailboxes = []
		if self._account.type == "POP":
			self.server = poplib.POP3(self._account.in_server, self._account.in_port)
			
		if self._account.type == "IMAP":
			self.server = imaplib.IMAP4_SSL(self._account.in_server, int(self._account.in_port))
			while True:
				password = tkSimpleDialog.askstring("Password?", "Please give your email's password.", show = '*')
				try:
					self.server.login(self._account.email, password)
					break
				except:
					tkMessageBox.showerror('Oh, poopy.', 'Apparently, you screwed up your password. Try again.')
			status, self.mailboxraw = self.server.list()
			for box in self.mailboxraw:				
				self.mailboxes.append(box.split('" "')[1].strip('"'))
		return self.mailboxes
	
	def retrieve_mail(self, mailbox = 'INBOX', what = 'ALL'):
		currentBox = self.get_folder(mailbox)
		
		self.server.select(mailbox)
		typ, data = self.server.search(None, what)

		self.total = len(data[0].split())
		self.progressbar.config(maximum = self.total)
		loaded = 0
		for num in data[0].split():
			typ, data = self.server.fetch(num, '(RFC822)')
			currentBox.add(data[0][1])
			loaded += 1
			self.progressbar.config(value = loaded)
			
			print 'Progress step'
		self.server.close()
		print self.list_folders()

		
class Outbox:
	""" A list of mail messages that can be periodically sent to their recipients. """
	
	def __init__ (self, account):
		""" 
		Constructor.
		
		account -- the account that will be used to send mail.
		"""
		self.queue = []
		self.account = account
	
	def add (self, message):
		""" Adds a message to the list. 
		
		message -- The message to add.
		"""
		self.queue.append(message)		
		
	def send_all (self, password):
		""" sends all the messages """
		print "Sendall called."
		for mNumber in self.queue:			
			self.send(self.queue.pop(), password)

	def send(self, message, password):
		print "Send called: Account" + self.account.out_server
		mailServer = smtplib.SMTP(self.account.out_server, self.account.out_port)
		print "Server created."
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(self.account.email, password)
		print "Server logged in."
		mailServer.sendmail(self.account.email, message['to'], message.as_string())
		print "Message Sent."
		# Should be mailServer.quit(), but that crashes...
		mailServer.close()
		print "Server closed."
