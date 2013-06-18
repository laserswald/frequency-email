from Tkinter import *
from ttk import *

class ButtonBoxType(object):
    OK_CANCEL = 1
    OK = 2
    
class WizardPage(object):
    """A page in a wizard helper dialog class."""

    def __init__(self, wizard, title="Title"):
        self.master = wizard.pageframe
        self.frame = Frame(self.master)
        self.buttontype = ButtonBoxType.OK
        self.title = title

    def setup_widgets(self):
        """Sets up a title widget and the weights for the first column."""
        self.columnconfigure(0, weight=1)
        self.titlewidget = Label(self, text=self.title)
        self.titlewidget.config(font = "Helvetica 14 bold")
        self.titlewidget.grid(row=0, column=0, sticky="ew")

class InputPage(WizardPage):
    """docstring for InputPage"""
    def __init__(self, arg):
        super(InputPage, self).__init__()
        self.arg = arg

    def get_data(self, data):
        """Gets the data from a wizard's page. This is only for input pages."""
        pass
        
class DescriptionPage(WizardPage):
    """A wizard page that has textual information for the user to read."""
    def __init__(self, wizard, text="Text"):
        self.text = text
        super(DescriptionPage, self).__init__(wizard);
        
        self.setup_widgets()
    
    def setup_widgets(self):
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.textwidget = Message(self.frame, text=self.text)
        self.textwidget.config(borderwidth=1, relief="solid", anchor="nw", width=50)
        self.textwidget.grid(row=1, column=0, sticky="nsew")

        # This particular binding makes sure that the text widget "fits" the place alloted.
        self.textwidget.bind("<Configure>", lambda e: self.textwidget.configure(width=e.width-10))
        
class TextInputPage(InputPage):

    def __init__(self, labeltext="derp"):
        super(TextInputPage, self).__init__()

    def get_data(self, data, name):
        data.add(name, self.text)

    def setup_widgets(self):
        self.inputframe = Frame(self.master)
        self.entrylabel = Label(self.inputframe)
        self.entrywidget = Entry(self.entrylabel)
    
        self.entrylabel.grid(row=0, column=0, sticky="e")
        self.entrywidget.grid(row=0, column=1, sticky="w")

        self.inputframe.grid(row=1, column=0, sticky="nsew")

class AccountPage(InputPage):
    """docstring for AccountPage"""
    def __init__(self, arg):
        super(AccountPage, self).__init__()
        self.arg = arg
        

class ButtonBoxFactory(object):
    def __init__(self):
        pass
    
    def _make_button(self, master, name):
        return Button(master, text=name)

    def make_buttons(self, master, type, callbacks):
        frame = Frame(master)
        if type == ButtonBoxType.OK:
            button = self._make_button(master, "Ok")
            button.pack(side=LEFT)
        return frame

class Wizard(object):
    def __init__(self, master, title):
        self.master = master
        self.frame = Toplevel(master)
        self.frame.minsize(300, 400)
        self.frame.title(title)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.pageframe = Frame(self.frame)
        self.pageframe.config(borderwidth=3, relief="ridge")
        self.pageframe.grid(row = 0, column = 0, sticky="nsew")
        self.pageframe.columnconfigure(0, weight=1)
        self.pageframe.rowconfigure(0, weight=1)
        
        self.buttons = Frame(self.frame)        
        self.forward_button = Button(self.buttons, text = "Next", command = self.next_page)
        self.forward_button.grid(row = 0, column = 0)       
        self.cancel_button = Button(self.buttons, text = "Cancel", command = self.cancel)
        self.cancel_button.grid(row = 0, column = 1)
        self.back_button = Button(self.buttons, text = "Back", command = self.previous_page)
        self.back_button.grid(row = 0, column = 2)      
        self.buttons.grid(row = 1, column = 0, sticky = "se")
        
        self.pages = []
        self.currentpage = 0
        
        self.data = {}
        
    def add_page(self, page):
        self.pages.append(page)
    
    def display_page(self, page, prev):
        self.clear_page(prev)
        self.draw_page(self.pages[page])
        
    def draw_page(self, page):
        page.frame.grid(row=0, column=0, sticky="nsew")
    
    def begin(self):
        self.draw_page(self.pages[self.currentpage])
    
    def cancel(self):
        self.output = {}
        self.frame.quit()       
    
    def clear_page(self, page):
        print self.pageframe.winfo_children()
        self.pageframe.winfo_children()[page].grid_remove()
        
    def next_page(self):
        print self.currentpage
        self.pages[self.currentpage].get_data(self.data)
        if len(self.pages)-1 != self.currentpage:
            self.currentpage += 1
            self.display_page(self.currentpage, self.currentpage-1)

    def previous_page(self):
        self.pages[self.currentpage].get_data(self.data)
        if 0 != self.currentpage:
            self.currentpage -= 1
            self.display_page(self.currentpage, self.currentpage+1)

if __name__ == "__main__":
    root = Tk()
    wiz = Wizard(root, "Wizard")
    page1 = DescriptionPage(wiz, "Page 1")
    page2 = DescriptionPage(wiz, "This is going on page 2.")
    wiz.add_page(page1)
    wiz.add_page(page2)
    wiz.begin()
    root.mainloop()
