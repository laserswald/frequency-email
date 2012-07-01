import Tkinter
from Tkinter import *
from ttk import *

class Toolbar(Frame):
    buttons = []
    def __init__(self, master, vertical=False, buttons = None):
        Frame.__init__(self, master, borderwidth=2, relief='raised')
        self.vert = vertical
        if buttons is not None:            
            self.items = buttons
        else:
            self.items = None
        self.pack_all()
        
    def insert(self, deff):
        self.items.append(deff)
        self.clear_drawn()
        self.pack_all()
        
        
    def clear_drawn(self):
        """deletes all the stuff in the toolbar and redraws."""
        for childname in self.winfo_children():
            widget = self.nametowidget(childname)
            widget.destroy()
            
    def pack_all(self):
        """ packs the items in the toolbar. """    
        if self.items:        
            for item in self.items:
                if item[2] == 'Button' or None:
                    temp = Button(self, text = item[0], command = item[1])
                elif item[2] == 'Entry':
                    temp = Entry(self, label = item[0])                
                elif item[2] == 'MenuButton':
                    temp = Menubutton(self, text = item[0], menu = item[1])
                if self.vert:
                	temp.pack(side = TOP, fill = Y)
                else:
                	temp.pack(side = LEFT, fill = X)
        else:
            pass

    def delete(self, buttonNumber):
        """ Function Documentation """
        self.buttons.delete
        
def defaultCallback():
    """ Function Documentation """
    this.clear_drawn()
    print "toolbar cleared"
    this.pack_all()
    print "toolbar redrawn"
    
# get button stuff
# then make the button stuff global
# refresh
if __name__ == "__main__":
    root = Tk()
    this = Toolbar(root, [["Testing", defaultCallback]])
    this.pack(side = TOP)
    #this.refresh()
    root.mainloop()
