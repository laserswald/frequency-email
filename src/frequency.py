#! /usr/bin/python2
from gui import mainWindow, messageView
from ping.account import mailaccount
from ping import boxfactory
from ping import outbox

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
        self.acctManager = mailaccount.EmailAccountManager(self.gui)
        self.acctManager.new_account()
        self.outbox = outbox.Outbox(self.acctManager.currentAccount)
        self.inbox = boxfactory.get_inbox(self.acctManager.currentAccount, self.gui)
        self.gui.start()

    def setup_account_manager (self):
        """ sets up the Account management class. """
        self.acctManager = mailAccount.EmailAccountManager()

    def quit(self):
        self.gui.quit()

    def setupGui(self):
        self.gui = mainWindow.MainWindow(self)
	
if __name__ == "__main__":
    frq = Frequency()

