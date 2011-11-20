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
import emailAccount

class Account(object):
	""" An individual account for things. Not to be used by itself, please. """
	data = {}
	def __init__ (self, manager):
		""" Class initialiser.
		
		manager - an Account Manager to accociate with.
		"""
		self.manager = manager

	
	def add_item (self, key, value):
		self.data[key] = value
		
		
class AccountError(Exception):
	def __init__(self, error):
		self.value = error

class AccountManager(object):
	""" A manager for accounts. Can delete, add, set as default, load 
	from a configuration file, etc. """
	
	config = ConfigParser.SafeConfigParser()
	
	def __init__ (self, configfile):
		""" 
		Class initialiser.
		
		configfile - the name of the file that holds the configuration
			for the manager.
		 """
		self.configFile = configfile
		self.currentAccount = None
		self.read_configuration()

	def read_configuration (self):
		""" Reads the configuration file and performs filechecks. """
		try:
			self.config.read(self.configFile) #read that file, dammit.
		except IOError:
			self.setup_config()
		try:  
			self.defaultSection = self.config.get('Global', 'Default')		
			if self.config.has_option(self.defaultSection, 'name'):
				self.load_account(self.defaultSection)
			else:
				raise Exception
		except:
			self.new_account(default = True)
			


			
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
		except ConfigParser.NoSectionError:
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
		print account.data
		for field in account.data:
			self.config.set(account.data['name'], field, str(account.data[field]))
		self.config.write(open(self.configFile, 'w'))
		
	def load_account(self, section):
		'''
		Loads the specified account from the file. 
		'''
		self.currentAccount = Account(self)
		for name, value in self.config.items(section):
			self.currentAccount.add_item(name, value)
		
	

	def __del__(self):
		self.save_account()

def test():
	manager = AccountManager('accountTest.cfg')
	manager.new_account()
	manager.currentAccount.add_item('Blarg', 'Honk')
	print manager.currentAccount.data['Blarg']
	manager.save_account()
	


if __name__ == '__main__':
	test()
