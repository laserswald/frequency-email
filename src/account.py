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
import pickle

class Account(object):
	""" An individual account for things. Not to be used by itself, please. """
	
	def __init__ (self):
		""" Class initialiser """
		self.save()
		
	def save(self):
		#save account for later loading
		pickle.dump(self, open(self.name, "wr"))
		
class AccountError(Exception):
	def __init__(self, error):
		self.value = error

class AccountManager(object):
	""" A manager for accounts. Can delete, add, set as default, load 
	from a configuration file, etc. """
	
	config = ConfigParser.SafeConfigParser()
	
	def __init__ (self, configfile = 'config.ini'):
		""" 
		Class initialiser.
		
		configfile - the name of the file that holds the configuration
			for the manager.
		 """
		self.currentAccount = None
		self.configFile = configfile
		self.read_configuration()

	def read_configuration (self):
		""" Reads the configuration file and performs filechecks. """
		try:
			self.config.read(self.configFile) #read that file, dammit.
		except IOError: #There's no file there!
			self.open_config_file() #Therefore, we should make one.			
		try:
			self.accountFile = self.config.get('Settings', 'Account')
		except: #The file is not set up correctly, so go choose the correct file.
			self.fix_config_file()
		
	def create_config_file (self):
		""" creates the configuration file based on the name given as 
		argument to AccountManager. """
		self.configFile = open(self.configFile, 'r')
		
	def fix_config_file (self):
		""" fixes the configuration file. Overload this."""
		raise AccountError("Fixing the config file hasn't been overloaded")
		
	def set_as_default (self):
		""" writes the account name to the config file as the default. """
		try:
			self.config.set('Settings','Account',self.currentAccount.name)
			
		except ConfigParser.NoSectionError:
			self.config.add_section('Settings')
			self.config.set('Settings','Account',self.currentAccount.name)
		
		self.config.write(self.configFile)
					
	
	def open_account_file (self, datafile):
		"""
		Loads the account and makes it the current account.
		
		datafile -- the path of the account file.
		"""
		try:
			self.currentAccount = pickle.load(open(datafile, "r"))
		except AttributeError:
			#That account does not work. Make a new one. 			
			self.new_account()
		
	def new_account (self, default = False):
		""" Creates a new accessable account. Overload, please. """
		self.currentAccount.save()
		self.currentAccount = Account()
		if default:
			self.set_as_default(self.currentAccount)
			


def test():
	manager = AccountManager()


if __name__ == '__main__':
	test()

