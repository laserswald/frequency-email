# -*- coding: utf-8 -*-
#
#     mainWindow.py
#
#      Copyright 2010 Ben Davenport-Ray <laserdude11@gmail.com>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#      MA 02110-1301, USA.
from Tkinter import *
from ttk import *
import tkMessageBox
from PIL import Image, ImageTk
import os
import dialogs
import widget.mailboxList
import widget.messagelist
import messageView
from widget.ToolFrame import *
import ping.account.manager

class MainWindow(object):

    def __init__(self):
        self.master = Tk()
        self.dialogs = dialogs.DialogManager(self.master)
        self.accounts = ping.account.manager.AccountManager(self)
        self.setup_widgets()
        
        
    def start(self):
        password = self.dialogs.askPassword()
        self.accounts.currentAccount.inbox.login(password)
        self.update_folders()
        self.get_mail()
        self.master.mainloop()

    def setup_widgets (self):
        """Sets up all the user interface in the main window.
        """
        
        self.master.title("Frequency")
        if os.name == "nt":
           self.master.iconbitmap("icons/Frequency.ico")
        self.dialogs = dialogs.DialogManager(self.master)
        self.master.grid_rowconfigure(1, weight = 1)
        self.master.grid_columnconfigure(0, weight = 1)
        self.setup_icons()
        self.setup_menus()
        self.setup_tools()
        self.panes = PanedWindow(self.master, orient = HORIZONTAL)

        #TODO Finish the mailbox tree subclass of Treeview.
        self.mailboxTree = widget.mailboxList.MailboxView(self.master, self.accounts, self)
        self.panes.add(self.mailboxTree)

        self.rightpanes = PanedWindow(self.master, orient = VERTICAL)
        

        self.messageList = widget.messagelist.MessageList(self.master, self.accounts, self)
        
        
        self.rightpanes.add(self.messageList)
        self.panes.add(self.rightpanes)
        self.panes.grid(row = 1, column = 0, sticky = N+S+E+W)
        #self.status.set("Welcome to Frequency!")
        
    def setup_menus(self):
        self.mainMenu = Menu(self.master)
        
        self.fileMenu = Menu(self.mainMenu)
        
        self.newMenu = Menu(self.fileMenu)
        self.newMenu.add_command(label = "Message", command = self.new_message)
        self.fileMenu.add_cascade(label = "New", menu = self.newMenu)
        self.fileMenu.add_command(label = "Send/Recieve",  compound = LEFT)
        self.fileMenu.add_command(label = 'Options', command = self.options)
        self.fileMenu.add_command(label = "Exit", command = self.quit)
        
        self.mainMenu.add_cascade(label = "File", menu = self.fileMenu)

        self.master.config(menu = self.mainMenu)
        
    def setup_tools(self):
        self.toolbar = ToolFrame(self.master)
        button = ToolImageButton(self.toolbar, label = "Send/Recieve", image = self.email_icon);
        self.toolbar.insert(button)
        self.toolbar.grid(row=0, column=0, sticky = N+S+E+W)
    def setup_icons(self):
        self.email_icon = ImageTk.PhotoImage(Image.open('icons/email.png'))
        #self.email_add_icon = ImageTk.PhotoImage(Image.open('./icons/email_add.png'))
        #self.email_delete_icon = ImageTk.PhotoImage(Image.open('./icons/email_delete.png'))
        #self.email_attach_icon = ImageTk.PhotoImage(Image.open('./icons/email_attach.png'))
        #self.email_edit_icon = ImageTk.PhotoImage(Image.open('./icons/email_edit.png'))
        #self.door_in_icon =  ImageTk.PhotoImage(Image.open('./icons/door_out.png'))
        #self.user_add_icon = ImageTk.PhotoImage(Image.open('./icons/user_add.png'))
        self.wrench_icon = ImageTk.PhotoImage(Image.open("icons/wrench.png"))

    def quit(self):
        self.master.quit()
            
    def options(self):
        pass

    def new_message(self):
        pass

    def switch_accounts(self, thingy):
        pass
    
    def show_message(self, messagekey):
        view = messageView.MessageView(self.master)
        view.load_from_message(self.accounts.currentAccount.inbox.get_message(messagekey))

    def get_mail(self):
        # make this get all mail
        self.accounts.currentAccount.inbox.retrieve_mail()
       
    def box_selection(self, mailbox):
        self.messageList.show_mailbox(mailbox)

    def update_folders(self):
        folders = self.accounts.currentAccount.inbox.get_folders()
        self.mailboxTree.load_mailboxes(folders)

if __name__ == "__main__":
    mw = MainWindow(None)
    mw.start()
