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
import configparser
from account import Account
import exception as ae

class AccountManager(object):
	""" A manager for accounts. Can delete, add, set as default, load
	from a configuration file, etc. """

	def __init__ (self):
		"""
		Class initialiser.
		"""
		self.config = configparser.SafeConfigParser()
		self.currentAccount = None
		
	def read_configuration (self):
		""" Reads the configuration file and performs filechecks. """
		self.config.read(self._configfile)

	def setup_config (self):
		""" Function doc """
		self.config.add_section('Global')
		self.config.set('Global', 'Default', '')

	def choose_account (self):
		""" fixes the configuration file. Overload this."""
		raise AccountError("Fixing the config file hasn't been overloaded")

	def set_as_default (self):
		""" writes the account name to the config file as the default. """
		try:
			self.config.set('Global', 'Default', self.currentAccount.data['name'])
		except configparser.NoSectionError:
			self.setup_config()
			self.config.set('Global', 'Default', self.currentAccount.data['name'])
		self.config.write(open(self.configFile, 'w'))

	def new_account (self, name = 'Account', default = False, welcome = False):
		""" Creates a new accessable account. Overload, please. """
		if self.currentAccount:
			self.save_account(self.currentAccount)
		self.currentAccount = Account(self, name)
		if default:
			self.set_as_default(self.currentAccount)

	def save_account(self, account = None):
		"""
		Saves an account to the file.
		"""
		if account == None:
			account = self.currentAccount
		self.config.add_section(account.data['name'])
		for field in account.data:
			self.config.set(account.data['name'], field, str(account.data[field]))
		self.config.write(open(self.configFile, 'w'))

	def load_account(self, section):
		'''
		Loads the specified account from the file. 
		'''
		self.createNewAccount
		for name, value in self.config.items(section):
			self.currentAccount.add_item(name, value)
		
	def __del__(self):
		self.save_account()
		
	def getConfigFile(self): return self._configfile
	def loadConfigFile(self, newValue):
		self._configfile = newValue
		self.read_configuration()
		
