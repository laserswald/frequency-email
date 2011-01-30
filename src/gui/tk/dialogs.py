'''
Created on Jan 30, 2011

@author: ben
'''
from Tkinter import *
import tkSimpleDialog
class EmailAccountDialog(tkSimpleDialog.Dialog):
    
    def body(self, master):
        self.control = StringVar()
        Label(master, text="Email Address:").grid(row=0)
        self.em = Entry(master)
        self.em.grid(row = 0, column = 1)
        
        self.r1 = Radiobutton(master, text = 'POP Account', variable = self.control, value = "POP",)
        self.r2 = Radiobutton(master, text = 'IMAP Account', variable = self.control, value = "IMAP",)
        self.r1.grid(row=1, column=0)
        self.r2.grid(row=2, column=0)
        
        Label(master, text="Server:").grid(row=3)
        Label(master, text="Port:").grid(row=4)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e1.grid(row=3, column=1)
        self.e2.grid(row=4, column=1)
        
        Label(master, text="SMTP").grid(row=5)
        
        Label(master, text="Server:").grid(row=6)
        Label(master, text="Port:").grid(row=7)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e3.grid(row=6, column=1)
        self.e4.grid(row=7, column=1)
        

        return self.em # initial focus



    def apply(self):
        self.server = self.e1.get()
        self.port = self.e2.get()
        self.smtp_server = self.e3.get()
        self.smtp_port = self.e4.get()
        self.type = self.control.get()
        self.email = self.em.get()
        self.result = 1
