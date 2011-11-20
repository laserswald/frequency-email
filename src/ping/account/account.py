#!/usr/bin/env python
# An account managing system.

import configparser


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
		
	def remove_item(self, key):
		self.data.remove(key)
	
	def get_item(self, key):
		return self.data[key]

