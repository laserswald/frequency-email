'''
Created on Jun 17, 2013

@author: Ben
'''
import ttk
import rfc822
import mailbox

class MessageList(ttk.Treeview):
    '''
     A Treelist
    '''


    def __init__(self, master, accounts, reciever):
        '''
        Constructor
        '''
        self.master = master
        self.accounts = accounts
        self.reciever = reciever
        self.messageColumns = ('Subject', 'From', 'Date')
        ttk.Treeview.__init__(self, self.master, columns = self.messageColumns, show = 'headings')
        
        for heading in self.messageColumns:
            self.heading(heading, text = heading)
        self.bind("<<TreeviewSelect>>", self.message_select);

    def show_mailbox(self, boxname):        
        print "showing mailbox"

        print "trying to get folder."
        if boxname == "INBOX":
            self.selectedBox = self.accounts.currentAccount.inbox
        else:
            self.selectedBox = self.accounts.currentAccount.inbox.selectFolder(boxname)
        print self.selectedBox
        print self.selectedBox.items()
        try:
            print "clearing the box list"
            self.set_children('')
        except:
            print 'no items'
        for key, message in self.selectedBox.iteritems():
            print "Adding message: ", key, message.keys();
            treevalues = (message['subject'],
                        message['From'],
                        message['Date'])
            self.insert('', 'end', values=treevalues, iid=key)
            
    def sortby(self, col, descending):
        """Sort tree contents when a column is clicked on."""
        # grab values to sort
        data = [(self.set(child, col), child) for child in self.get_children('')]
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
                self.move(item[1], '', indx)
        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        self.heading(col,
            command=lambda col=col: self.sortby(col, int(not descending)))
        
    def message_select(self, event):
        
        message = event.widget.selection()[0]
        self.reciever.show_message(message)