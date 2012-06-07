from Tkinter import *
from ttk import *

class MailBoxView(Treeview):
	"""
	Class Documentation
	"""
	
	def __init__(self):
		'''
		class initializer
		'''
		pass
		
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

	
	def box_selected(self, event):
		self.messageKeys = []
		boxname = event.widget.selection()[0]
		while True:
			try:
				self.selectedBox = self.inboxes.get_folder(boxname)
				break
			except:
				self.inboxes.add_folder(boxname)
		try:
			self.set_children('')
		except:
			print 'no items'
		for key, message in self.selectedBox.iteritems():
			treevalues = (message['Subject'],
						message['From'],
						message['Date'])
			self.insert('', 'end', values=treevalues)
			self.messageKeys.append(key)

	def sortby(self, tree, col, descending):
		"""Sort tree contents when a column is clicked on."""
		# grab values to sort
		data = [(tree.set(child, col), child) for child in tree.get_children('')]
		if col == 'Date':
			newData = []
			for index, item in enumerate(data):
				date = item[0]
				dataitem = (rfc822.parsedate(date), index, item)
				newData.append(dataitem)

			newData.sort(reverse=descending)
			for set in enumerate(newData):
				print set
				parsedate, indx, item = set
				tree.move(item[1], '', indx)
		# reorder data
		data.sort(reverse=descending)
		for indx, item in enumerate(data):
			tree.move(item[1], '', indx)

		# switch the heading so that it will sort in the opposite direction
		tree.heading(col,
			command=lambda col=col: self.sortby(tree, col, int(not descending)))