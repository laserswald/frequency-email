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
		self.gui.messageList.set_children('')		
		for key in self.selectedBox.iterkeys():
			message = self.selectedBox.get_message(key)

			self.gui.messageList.add_message(message)
			self.messageKeys.append(key)
		self.gui.update_status('Messages for folder %s loaded.' % boxname)
			
	def edit_account(self):
		print 'Edit Account called!'

	def load_account(self):
		print 'Load Account called!'

	def new_account(self):
		print 'New Account called!'
		
	def quit(self):
		self.gui.quit()

	def setupGui(self):
		self.gui = gui.main.MainWindow(self)
		
	def options(self):
		'''
		Opens the options dialog.
		'''
		self.gui.dialogs.settings()
		
	def box_rightclick(self, event):
		'''
		Opens up a context menu for the item.
		'''
		print "box.rightclick called"
	
	