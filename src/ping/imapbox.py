'''
Created on Jul 12, 2011

@author: ben
'''

import inbox



class ImapBox(inbox.Inbox):
    folderlist = []

    def retrieve_mail(self, mailbox = 'INBOX', what = 'ALL'):
        typ, data = self.server.search(None, what)
        total = len(data[0].split())
        for num in data[0].split():
            typ, data = self.server.fetch(num, '(RFC822)')
            self.currentBox.add(data[0][1])
        self.server.close()
	return total



    def setupServer(self, username, password, ssl = False):
        self.server = imaplib.IMAP4_SSL(self._account.data['in_server'], int(self._account.data['in_port']))
        
       

    def refreshMailboxes(self):
        '''
        Retrieves the email mailboxes.
        '''
        self.folderlist = []
        status, self.mailboxraw = self.server.list()
        self.gui.update_status('Creating subfolder structure...')
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

    def retrieve_folders(self):
        return self.splitToTree(self.folderlist)



    def __del__(self):
        '''
        Deletion.
        '''
        self.server.close()
    
  
    def teardownServer(self):
        pass
    
    def recieveFolders(self):
        pass
    
    def getFolders(self):
        pass
    
    def selectFolder(self):
        self.currentBox = self.get_folder(mailbox)
        self.server.select(mailbox)
    
    def getMail(self):

    
    def switchMailbox(self, mailbox, readOnly = False):
        pass

def open_connection(self, ssl = False):
	
    def login(self, email=None, password):
	if not email:
            email = 
	 self.server.login(email, )
if __name__ == "__main__":
	import Account
	acct = Account.Account(None)
	acct.add_item("email"
	imap = ImapBox(
        
