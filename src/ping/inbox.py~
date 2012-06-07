'''
Created on Jul 12, 2011

@author: ben
'''

import mailbox
import popbox
import imapbox

class Inbox(mailbox.Maildir):
    """
    This class represents a maildir mailbox with convenience functions for getting mail.
    """
    total = 0
    loaded = 0

    def __init__(self, account, gui):
        """
        Constructor.

        account -- An account to bind this mailbox to.
        """
        self._account = account
        mailbox.Maildir.__init__(self, self._account.data['mboxdir'], factory = mailbox.MaildirMessage)

        self.type = self._account.data['type']
        self.setup_server()


    def setup_server(self):
        print 'Overload this'
        
def get_inbox(account, gui):
    '''
    gets the correct inbox type when called.
    '''
    if account.data['type'] == 'POP':
        inbox = PopBox(account, gui)
    if account.data['type'] == 'IMAP':
        inbox = ImapBox(account, gui)
    return inbox
