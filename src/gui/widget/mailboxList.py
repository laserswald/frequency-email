from Tkinter import *
from ttk import *

class MailBoxView(Treeview):
    """
    Class Documentation
    """
    
    def __init__(self, master):
        '''
        class initializer
        '''
        Treeview.__init__(self, master)
        
    def add_account_tree(self, accountname, folders = None):
        '''
        Adds some default
        '''
        self.insert()
        
    def load_mailboxes(self, folder, list):
        if folder == None:
            folder = ''

        if list == "" or list == None:
            return

        for box in list.iterkeys():
            self.insert(folder, 'end', box, text=box)
            self.load_mailboxes(box, list[box])

    
    def box_selected(self, event):
        self.messageKeys = []
        boxname = event.widget.selection()[0]
        while True:
            try:
                self.selectedBox = self.inboxes.get_folder(boxname)
                break
            except:
                self.inboxes.add_folder(boxname)
        try:
            self.set_children('')
        except:
            print 'no items'
        for key, message in self.selectedBox.iteritems():
            treevalues = (message['Subject'],
                        message['From'],
                        message['Date'])
            self.insert('', 'end', values=treevalues)
            self.messageKeys.append(key)

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

if __name__ == "__main__":
    app = Tk()
    mailboxlist = MailBoxView(app)
    mailboxlist.pack()
    boxen = {"blarg": {"derp": ""}}
    print boxen

    mailboxlist.load_mailboxes("", boxen)
    app.mainloop()


