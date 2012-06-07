
import gui.mainWindow
import gui.messageView
import ping.account.mailaccount
import ping.inbox
import ping.outbox


class Frequency(object):
    '''
    The main class invoked when starting up.
    '''

    def __init__(self):
        '''The constructor of Frequency.
		
		This is the main class, only really useful for concerting each of the other classes
		in Frequency.
        '''

        self.setupGui()
        #TODO: Make wizard for new account creation
        self.acctManager = ping.account.mailaccount.EmailAccountManager(self.gui)
        self.acctManager.new_account()
        self.outbox = ping.outbox.Outbox(self.acctManager.currentAccount)
        self.inbox = ping.inbox.Inbox.get_inbox(self.acctManager.currentAccount, self.gui)
        self.get_mailboxes()
        
    def setup_account_manager (self):
        """ sets up the Account management class. """
        self.acctManager = emailAccount.EmailAccountManager()

    def quit(self):
        self.gui.quit()

    def setupGui(self):
        self.gui = gui.mainWindow.MainWindow(self)
        self.gui.start()
	
if __name__ == "__main__":
    frq = Frequency()

