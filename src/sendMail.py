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
import mailbox
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import getpass
import os

class Inbox(mailbox.mbox):
	"""
	This class represents a maildir mailbox with convenience functions for getting mail.
	"""

	def __init__(self, account = None):
		"""
		Constructor.

		account -- An account to bind this mailbox to.
		"""
		self._account = account
		mailbox.mbox.__init__(self, self._account.mboxDir, create = True)
		self.retr_mail()
		

	def retr_mail(self):
		"""
		Retrieving of emails and placing them into the mailbox.
		"""
		if self._account.type == "POP":
			print self._account.in_server, self._account.in_port
			M = poplib.POP3_SSL(self._account.in_server, self._account.in_port)
			M.user = self._account.email
			M.pass_ = getpass.getpass()
			
		self.numMessages = len(M.list()[1])
		for i in range(self.numMessages):
			retrmess = M.retr(i+1)
			messgStr = string.join(retrmess[1], "\n")
			message = mailbox.mboxMessage(messgStr)
			self.add(message)
			
	def getheaders(self):
		""" Gets the headers for each email. """
		self.headers = []
		for value in self.values():
			self.headers.append.value['Subject']
		return self.headers
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

if __name__ == "__main__":
	import emailAccount
	acc = emailAccount.Account('laserdude11@gmail.com',
					'POP',
					'pop.gmail.com',
					'995',
					'smtp.gmail.com',
					'587'
					)
	inb = Inbox(acc)
	inb.getheaders()

