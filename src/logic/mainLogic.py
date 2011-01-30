'''
Created on Jan 30, 2011

@author: ben
'''
import rfc822
import emailAccount

class MainWindowLogic(object):
    '''
    classdocs
    '''


    def __init__(self, guikit):
        '''
        Constructor
        '''
        self.toolkit = guikit

    
    def send(self, event): #Main mail driver.
        
        password = gui.Dialogs.askPassword()
        try:
            self.outbox.send_all(password)
            self.status.push(self.mailContext, "All mail sent!")
        except:
            self.status.push(self.mailContext, "Mail sending failed.")    
                        
    def send_receive(self, event):
        pass
    
    def compose (self, event):
        """ Launches the composer. """
        compose = gui.Composer(self.acctManager.currentAccount, self.master)
        try:
            self.outbox.add(compose.returned)
            gui.main.updateStatus('Composition successful. Message now in outbox.')
        except AttributeError:
            gui.main.updateStatus(self.mailContext, 'Message was not saved.')            

    def setup_account_manager (self):
        """ sets up the Account management class. """
        self.acctManager = emailAccount.EmailAccountManager(self.toolkit)
        
        
    def get_mail(self, boxname): 
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
            self.mailboxTree.insert(folder, 'end', mailbox, text=mailbox)
            self.master.update
        
        
    def message_selected(self, event):
        item = self.messageList.selection()
        index = int(item[0].strip('I'), base=16) - 1
        key = self.messageKeys[index]
        displayedMessage = self.selectedBox.get_message(key)
        self.mView = gui.MessageView(self.master)
        self.mView.load_from_message(displayedMessage)
        
    def sortby(self, tree, col, descending):
        """Sort tree contents when a column is clicked on."""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        if col == 'Date':
            newData = []
            for index, item in enumerate(data):
                date = item[0]
                dataitem = (rfc822.parsedate(date), index, item)
                newData.append(dataitem)    
        
            newData.sort(reverse=descending)
            for set in enumerate(newData):
                print set
                parsedate, indx, item = set
                tree.move(item[1], '', indx)
        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)
    
        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
            command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def edit_account(self, event):
        print 'Edit Account called!'
    
    def load_account(self, event):
        print 'Load Account called!'
    
    def new_account(self, event):
        print 'New Account called!'
        
    def choose_toolkit(self, toolkit):
        if toolkit == 'tk':
            import gui.tk as gui
        elif toolkit == 'gtk':
            import gui.gtk as gui
        elif toolkit == 'wx':
            import gui.wxgui as gui
    