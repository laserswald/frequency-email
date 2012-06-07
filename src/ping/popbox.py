'''
Created on Jul 12, 2011

@author: ben
'''

import inbox
import poplib

class PopBox(inbox.Inbox):

    def retrieve_mail(self):
        '''
        Retrives email from POP.
        '''
        print "retrieve_mail called"

    def setup_server(self, isSSL = False):
        self.server = poplib.POP3(self._account.data['in_server'])
