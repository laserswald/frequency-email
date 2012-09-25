'''
Created on Jul 12, 2011

@author: ben
'''

import inbox
import imaplib


class ImapBox(inbox.Inbox):
    folderlist = []

    def start(self, password):
        self.connect()
        self.login(password)
        

    def retrieve_mail(self, mailbox = 'INBOX', what = 'ALL'):
        typ, data = self.server.search(None, what)
        total = len(data[0].split())
        for num in data[0].split():
            self.getMessage(num)
        self.disconnect()
        return total      

    def getFolderList(self):
        '''
        Retrieves the email mailboxes.
        '''
        self.folderlist = []
        status, self.mailboxraw = self.server.list()
        for box in self.mailboxraw:
            boxstuff = box.split('" "')
            folderpath = boxstuff[1].strip('"')
            self.folderlist.append(folderpath)
            try:
                self.get_folder(folderpath)
            except mailbox.NoSuchMailboxError:
                self.add_folder(folderpath)


    def splitToTree(self, directory, spl="/"):
        directories = []
        for z in directory:
            directories.append(z.split(spl))
        tree = {}
        for x in directories:
            tree = self.folderToTree(x, tree)
        return tree
    
    
    def folderToTree(self, folder, tree = {}):
        """ Function doc """
        if folder == []:
            return {}
        
        start = folder.pop(0)
        
        if start in tree:
            tree[start] = self.folderToTree(folder, tree[start])
        else:
            newtree = {}
            tree[start] = self.folderToTree(folder, newtree)
        return tree

    def getFolderTree(self):
        return self.splitToTree(self.folderlist)    
  
    def disconnect(self):
        self.server.close()
    
    def selectFolder(self):
        self.currentBox = self.get_folder(mailbox)
        self.server.select(mailbox)
    
    def getMessage(self, msgnum):
        diag, data = self.server.fetch(num, '(RFC822)')
        self.currentBox.add(data[0][1])
        return diag
    
    def connect(self, ssl = False):
        if ssl:
            self.server = imaplib.IMAP4_SSL(self._account.data['in_server'], int(self._account.data['in_port']))
        else:
            self.server = imaplib.IMAP4(self._account.data['in_server'], int(self._account.data['in_port']))
    
    def login(self, password, email=None):
        if not email:
            email = self._account.data["email"]
        self.server.login(email, password)
        
