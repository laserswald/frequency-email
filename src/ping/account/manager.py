#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       AccountManager.py
#		A system for managing accounts with pickle and a config file.
#
#       Copyright 2011 Ben Davenport-Ray <laserdude11@gmail.com>
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
import ConfigParser
from account import EmailAccount
import exception as ae

class AccountManager(object):
	""" A manager for accounts. Can delete, add, set as default, load
	from a configuration file, etc. """

	def __init__ (self, gui, configfile=".frequencyrc"):
		"""
		Class initialiser.
		"""

		self._configfile = configfile
		self.config = ConfigParser.SafeConfigParser()

		self.currentAccount = None
		self.gui = gui
		self.accounts = []
		self.read_configuration()
		
	def read_configuration (self):
		""" Reads the configuration file and performs filechecks. """
		print "debug - reading account config"
		try:
			self.config.read(self._configfile)
			self.defaccount = self.config.get("Global", "default")
		except ConfigParser.NoSectionError:
			print "No default found, going to set up new file."
			self.new_setup_config()
		self.load_account(self.defaccount)

	def new_setup_config (self):
		""" Function doc """
		print "Setting up new account file."
		self.config.add_section('Global')
		self.new_account(default = True)

	def choose_account (self):
		""" fixes the configuration file. Overload this."""
		raise ae.AccountError("Fixing the config file hasn't been overloaded")

	def set_as_default (self):
		""" writes the account name to the config file as the default. """
		try:
			self.config.set('Global', 'default', self.currentAccount.name)
		except ConfigParser.NoSectionError:
			self.setup_config()
			self.config.set('Global', 'default', self.currentAccount.name)
		self.config.write(open(self._configfile, 'w'))

	def new_account (self, default = False):
		""" Creates a new accessable account. """
		print "making new account"
		if self.currentAccount:
			self.save_account(self.currentAccount)
		self.currentAccount = self.gui.dialogs.settings()
		if default:
			self.set_as_default()
		self.save_account()

	def save_account(self, account = None):
		"""
		Saves an account to the file.
		"""
		if account == None:
			account = self.currentAccount
		self.config.add_section(account.name)
		self.config.set(account.name, "username", self.currentAccount.username)
		self.config.set(account.name, "email", self.currentAccount.email)
		self.config.set(account.name, "type", self.currentAccount.type)
		self.config.set(account.name, "in_server", self.currentAccount.in_server)
		self.config.set(account.name, "in_port", self.currentAccount.in_port)
		self.config.set(account.name, "out_server", self.currentAccount.out_server)
		self.config.set(account.name, "out_port", self.currentAccount.out_port)

		self.config.write(open(self._configfile, 'w'))

	def load_account(self, section):
		'''
		Loads the specified account from the file. 
		'''
		try: 
			username = self.config.get(section, "username")
			email = self.config.get(section, "email")
			_type = self.config.get(section, "type")
			in_server = self.config.get(section, "in_server")
			in_port = self.config.get(section, "in_port")
			out_server = self.config.get(section, "out_server")
			out_port = self.config.get(section, "out_port")
			self.currentAccount = EmailAccount(section, username, email, _type, in_server, in_port, out_server, out_port)
		except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
			self.new_account(default=True)
			
	def __del__(self):
		self.save_account()
		
	def getConfigFile(self): return self._configfile
	
	def loadConfigFile(self, newValue):
		self._configfile = newValue
		self.read_configuration()
