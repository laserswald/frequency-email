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
from widget.ToolFrame import *
from widget import mailboxList 

class MainWindow(object):

    def __init__(self, accountmgr):
        self.accountmgr = accountmgr
        self.master = Tk()
        self.setup_widgets()
        self.dialogs = dialogs.DialogManager(self.master)
    
    def setup_widgets (self):
        """Sets up all the user interface in the main window.
        """
        
        self.master.title("Email")
        if os.name == "nt":
            self.master.iconbitmap("./icons/Frequency.ico")

        
        self.master.grid_rowconfigure(1, weight = 1)
        self.master.grid_columnconfigure(0, weight = 1)
        self.setup_icons()
        self.setup_menus()
        self.setup_tools()
        self.panes = PanedWindow(self.master, orient = HORIZONTAL)
        #TODO Finish the mailbox tree subclass of Treeview.
        self.mailboxview = mailboxList.MailBoxView(self.master);
        self.panes.add(self.mailboxview)
        self.rightpanes = PanedWindow(self.master, orient = VERTICAL)
        self.messageColumns = ('Subject',
                            'From',
                            'To',
                            'Date')
        self.messageList = Treeview(self.master,
                                    columns = self.messageColumns,
                                    show = 'headings')
        for heading in self.messageColumns:
            self.messageList.heading(heading, text = heading)
        self.messageList.bind("<<TreeviewSelect>>", self.message_selected)


        self.rightpanes.add(self.messageList)
        self.panes.add(self.rightpanes)
        #self.messageLis
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
        button = ToolImageButton(self.toolbar, label = "Send/Recieve", image = self.wrench_icon);
        self.toolbar.insert(button)
        self.toolbar.grid(row=0, column=0, sticky = N+S+E+W)
           
    def setup_icons(self):
        print os.getcwd()
        #self.email_icon = ImageTk.PhotoImage(Image.open('./icons/email.png'))
        #self.email_add_icon = ImageTk.PhotoImage(Image.open('./icons/email_add.png'))
        #self.email_delete_icon = ImageTk.PhotoImage(Image.open('./icons/email_delete.png'))
        #self.email_attach_icon = ImageTk.PhotoImage(Image.open('./icons/email_attach.png'))
        #self.email_edit_icon = ImageTk.PhotoImage(Image.open('./icons/email_edit.png'))
        #self.door_in_icon =  ImageTk.PhotoImage(Image.open('./icons/door_out.png'))
        #self.user_add_icon = ImageTk.PhotoImage(Image.open('./icons/user_add.png'))

        self.wrench_icon = ImageTk.PhotoImage(Image.open("./icons/wrench.png"))

    def quit(self):
        self.master.quit()
    
    def new_message(self):
        pass

    def message_selected(self):
        pass

    def populate(self):
        self.account

    def options(self):
        pass

    def start(self):
        self.master.mainloop()
        return self
        
if __name__ == "__main__":
    mw = MainWindow(None)
    mw.start()
