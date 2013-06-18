'''
Created on Jul 12, 2011

@author: ben
'''
import inbox
import mailbox
import imaplib

class ImapBox(inbox.Inbox):
    folderlist = []

    def retrieve_mail(self, mailbox = 'INBOX', what = 'ALL'):
        # TODO: make this multithreaded
        # TODO: add a notification system for the status bar
        print "retrieving mail from ", mailbox
        typ, data = self.server.search(None, what)
        total = len(data[0].split())
        if total > 10: total = 10
        for num in data[0].split():
            if int(num) > total: break
            self.getMessage(num)
            print "got message ", num, " of ", total
        return total      

    def get_folders(self):
        self.retrieve_folders()
        tree = self.get_folders_as_tree()
        return tree

    def retrieve_folders(self):
        '''
        Retrieves the email mailboxes.
        '''
        self.folderlist = []
        status, self.mailboxraw = self.server.list()
        for box in self.mailboxraw:
            boxstuff = box.split('" "')
            print "Box stuff:", boxstuff
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

    def get_folders_as_tree(self):
        return self.splitToTree(self.folderlist)    
  
    def disconnect(self):
        self.server.close()
    
    def selectFolder(self, mailbox):
        folder = self.get_folder(mailbox)
        self.server.select(mailbox)
        return folder
    
    def getMessage(self, msgnum):
        diag, data = self.server.fetch(msgnum, '(RFC822)')
        self.currentBox.add(data[0][1])
    
    def connect(self, ssl = False):
        if ssl:
            self.server = imaplib.IMAP4_SSL(self._account.in_server, int(self._account.in_port))
        else:
            self.server = imaplib.IMAP4(self._account.in_server, int(self._account.in_port))
    
    def login(self, password):
        email = self._account.email
        try:
            self.server.login(email, password)
        except imaplib.IMAP4.error:
            raise Exception
        finally:
            self.server.select();
            self.currentBox = self

    def setup_server(self):
        self.connect(ssl = True)
