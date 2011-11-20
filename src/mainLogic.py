'''
Created on Jan 30, 2011

@author: ben
'''
import rfc822
import mail.emailAccount
import gui.mainWindow
import gui.dialogs
import gui.composer
import gui.messageView
import mail.outbox

class MainWindowLogic(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''

		self.setupGui()
		self.acctManager = mail.emailAccount.EmailAccountManager(self.gui)
		self.outbox = mail.outbox.Outbox(self.acctManager.currentAccount)
		self.inbox = mail.outbox.get_inbox(self.acctManager.currentAccount, self.gui)
		self.get_mailboxes()
		

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
		self.recieve

	def compose (self):
		""" Launches the composer. """
		compose = self.gui.dialogs.compose(self.acctManager.currentAccount)
		try:
			self.outbox.add(compose.returned)
			self.gui.update_status('Composition successful. Message now in outbox.')
		except AttributeError:
			self.gui.update_status('Message was not saved.')

	def setup_account_manager (self):
		""" sets up the Account management class. """
		self.acctManager = mail.emailAccount.EmailAccountManager()


	def receive(self):
		"""Gets the mail from the selected mailbox."""
		boxname = self.gui.mailboxTree.selection()[0]
		self.inbox.retrieve_mail(boxname)


	def get_mailboxes(self):
		self.boxlist = self.inbox.retrieve_folders()
		print self.boxlist
		for box in self.boxlist:
			hie = box.split('/')
			if len(hie) > 1:
				folder = hie[-2]
				print 'Folder: ' + folder
				mailbox = hie[-1]
				print 'Mailbox: ' + mailbox
			elif len(hie) == 1:
				folder = ''; mailbox = hie[0]
				
			try:
				self.gui.mailboxTree.insert(folder, 'end', mailbox, text=mailbox)
			except:
				pass

	def message_selected(self, event):
		itemkey = self.gui.messageList.selection()[0]
		displayedMessage = self.selectedBox.get_message(itemkey)
		self.mView = gui.messageView.MessageView(self.gui.master)
		self.mView.load_from_message(displayedMessage)



	def box_selected(self, what):
		print what
		boxname = self.gui.mailboxTree.selection()[0]
		print boxname
		while True:
			try:
				self.selectedBox = self.inbox.get_folder(boxname)
				break
			except:
				self.inbox.add_folder(boxname)
		self.gui.messageList.clear()
		for key in self.selectedBox.iterkeys():
			message = self.selectedBox.get_message(key)
			self.gui.messageList.add_message(message, key)
		self.gui.update_status('Messages for folder %s loaded.' % boxname)

	def new_account(self):
		print 'New Account called!'

	def rem_account(self):
		print 'Remove Account called!'

	def quit(self):
		self.gui.quit()

	def setupGui(self):
		self.gui = gui.mainWindow.MainWindow(self)
		self.gui.start()

	def options(self):
		'''
		Opens the options dialog.
		'''
		self.gui.dialogs.settings()

	def box_rightclick(self, event):
		'''
		Opens up a context menu for the item.
		'''
		print


