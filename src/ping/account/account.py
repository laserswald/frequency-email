#!/usr/bin/env python
# An account managing system.

import ping.boxfactory
import ping.outbox

class EmailAccount(object):
	""" An individual email account. """


	def __init__ (self, name, username, email, _type, in_server, in_port, out_server, out_port):
		""" Class initialiser.
		"""
		self.name = name
		if (username == None): self.username = "none"
		else: self.username = username
		self.email = email
		self.type = _type
		self.in_server = in_server
		self.in_port = in_port
		self.out_server = out_server
		self.out_port = out_port

		print "Making inbox"
		self.inbox = ping.boxfactory.get_inbox(self)
		print "Making outbox"
		self.outbox = ping.outbox.Outbox(self)
