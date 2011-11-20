
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      sendMail.py
#
#      Copyright 2010 Ben Davenport-Ray <ben@benslaptop>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#      MA 02110-1301, USA.

import smtplib
import poplib
import imaplib
import mailbox





class Inbox(mailbox.Maildir):
	"""
	This class represents a maildir mailbox with convenience functions for getting mail.
	"""
	total = 0
	loaded = 0

	def __init__(self, account, gui):
		"""
		Constructor.

		account -- An account to bind this mailbox to.
		"""
		self._account = account
		self.gui = gui
		mailbox.Maildir.__init__(self, self._account.data['mboxdir'], factory = mailbox.MaildirMessage)

		self.type = self._account.data['type']
		self.setup_server()


	def setup_server(self):
		print 'Overload this'

class PopBox(Inbox):

	def retrieve_mail(self):
		'''
		Retrives email from POP.
		'''
		print "retrieve_mail called"

	def setup_server(self, isSSL = False):
		self.server = poplib.POP3(self._account.data['in_server'])


class ImapBox(Inbox):
	folderlist = []

	def retrieve_mail(self, mailbox = 'INBOX', what = 'ALL'):
		currentBox = self.get_folder(mailbox)
		self.server.select(mailbox)
		typ, data = self.server.search(None, what)

		self.total = len(data[0].split())
		self.gui.update_status('0 Messages out of %i loaded.' % self.total)
		loaded = 0
		for num in data[0].split():
			typ, data = self.server.fetch(num, '(RFC822)')
			currentBox.add(data[0][1])
			loaded += 1
			print loaded
			self.gui.update_status('%i Messages out of %i loaded.' % (loaded, self.total))
		self.server.close()



	def setup_server(self):
		self.server = imaplib.IMAP4_SSL(self._account.data['in_server'], int(self._account.data['in_port']))
		while True:
			password = self.gui.dialogs.askPassword()
			try:
				self.server.login(self._account.data['email'], password)
				break
			except self.server.error:
				self.gui.dialogs.error('Oh, poopy.', 'Apparently, you screwed up your password. Try again.')
		self.refresh_mailboxes()

	def refresh_mailboxes(self):
		'''
		Retrieves the email mailboxes.
		'''
		self.folderlist = []
		status, self.mailboxraw = self.server.list()
		self.gui.update_status('Creating subfolder structure...')
		for box in self.mailboxraw:
			boxstuff = box.split('" "')
			folderpath = boxstuff[1].strip('"')

			self.folderlist.append(folderpath)
			try:
				self.get_folder(folderpath)
			except mailbox.NoSuchMailboxError:
				self.add_folder(folderpath)

		self.gui.update_status('Folder structure update complete!')


	def retrieve_folders(self):

		return self.folderlist



	def __del__(self):
		'''
		Deletion.
		'''
		self.server.close()


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


def get_inbox(account, gui):
	'''
	gets the correct inbox type when called.
	'''
	if account.data['type'] == 'POP':
		inbox = PopBox(account, gui)
	if account.data['type'] == 'IMAP':
		inbox = ImapBox(account, gui)
	return inbox
