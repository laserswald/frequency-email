'''
Created on Jul 12, 2011

@author: ben
'''

import mailbox

class Inbox(mailbox.Maildir):
    """
    This class represents a maildir mailbox with convenience functions for getting mail.
    """
    total = 0
    loaded = 0

    def __init__(self, account):
        """
        Constructor.

        account -- An account to bind this mailbox to.
        """
        self._account = account
        mailbox.Maildir.__init__(self, self._account.name, factory=mailbox.MaildirMessage)

        self.type = self._account.type
        self.setup_server()


    def setup_server(self):
        print 'Overload this'
        