'''
Created on Jan 30, 2011

@author: ben
'''
import rfc822
import emailAccount
import gui.main
import gui.dialogs
import gui.composer
import gui.messageView
import mailtoss

class MainWindowLogic(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''

		self.setupGui()
		self.acctManager = emailAccount.EmailAccountManager(self.gui)		
		self.outbox = mailtoss.Outbox(self.acctManager.currentAccount)
		self.inboxes = mailtoss.Inbox(self.acctManager.currentAccount, self.gui)
		self.get_mailboxes()
		self.gui.start()
			
	def send(self):
		'''
		Sends email.
		'''
		password = self.gui.dialogs.askPassword()
		try:
			self.outbox.send_all(password)
			self.gui.update_status("All mail sent!")
		except:
			self.gui.update_status("Mail sending failed.")
	


	def send_receive(self):
		'''
		Sends and receives all email.
		'''
		self.send()
		self.get_mailboxes()

	def compose (self):
		""" Launches the composer. """
		compose = self.gui.Composer(self.acctManager.currentAccount)
		try:
			self.outbox.add(compose.returned)
			self.gui.update_status('Composition successful. Message now in outbox.')
		except AttributeError:
			self.gui.update_status('Message was not saved.')

	def setup_account_manager (self):
		""" sets up the Account management class. """
		self.acctManager = emailAccount.EmailAccountManager()


	def receive(self, boxname):
		"""Gets the mail from the selected mailbox."""
		self.inboxes.retrieve_mail(boxname)


	def get_mailboxes(self):
		self.boxlist = self.inboxes.retrieve_mailboxes()
		for box in self.boxlist:
			hie = box.split('/')
			if len(hie) == 2:
				folder, mailbox = hie
			elif len(hie) == 1:
				folder = ''; mailbox = hie[0]
			self.gui.mailboxTree.insert(folder, 'end', mailbox, text=mailbox)

	def message_selected(self, event):
		item = self.gui.messageList.selection()
		index = int(item[0].strip('I'), base=16) - 1
		key = self.messageKeys[index]
		displayedMessage = self.selectedBox.get_message(key)
		self.mView = gui.messageView.MessageView(self.gui.master)
		self.mView.load_from_message(displayedMessage)

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

	def box_selected(self, what):
		print what
		self.messageKeys = []
		boxname = self.gui.mailboxTree.selection()[0]
		
		while True:
			try:
				self.selectedBox = self.inboxes.get_folder(boxname)
				break
			except:
				self.inboxes.add_folder(boxname)
				self.receive(boxname)

		try:
			self.messageList.set_children('')
		except:
			print 'no items'
		for key in self.selectedBox.iterkeys():
			message = self.selectedBox.get_message(key)
			treevalues = (message['Subject'],
						  message['From'],
						  message['Date'])
			self.gui.messageList.insert('', 'end', values=treevalues)
			self.messageKeys.append(key)
		self.gui.update_status('Messages for folder %s loaded.' % boxname)
			
	def edit_account(self):
		print 'Edit Account called!'

	def load_account(self):
		print 'Load Account called!'

	def new_account(self):
		print 'New Account called!'
		
	def quit(self):
		pass

	def setupGui(self):
		self.gui = gui.main.MainWindow(self)
		
	def options(self):
		'''
		Opens the options dialog.
		'''
		self.gui.dialogs.settings()
	