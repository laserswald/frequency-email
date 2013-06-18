from Tkinter import *
from ttk import *

class MailboxView(Treeview):
	"""
	Class Documentation
	"""
	
	def __init__(self, master, accounts, reciever):
		'''
		class initializer
		'''
		Treeview.__init__(self, master)
		self.accounts = accounts
		self.reciever = reciever
		self.bind("<<TreeviewSelect>>", self.box_selected)
		
	def add_account_tree(self, accountname, folders = None):
		'''
		Adds some default
		'''
		print "add_mailaccount called"
		
	def load_mailboxes(self, list):
		for box in list:
			hie = box.split('/')
			if len(hie) == 2:
				folder, mailbox = hie
			elif len(hie) == 1:
				folder = ''; mailbox = hie[0]
			self.insert(folder, 'end', mailbox, text=mailbox)

	# TODO: split this up into helper functions.
	def box_selected(self, event):

		boxname = event.widget.selection()[0]
		self.reciever.box_selection(boxname)

