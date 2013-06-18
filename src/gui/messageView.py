'''
Created on Jan 17, 2011

@author: ben
'''
from Tkinter import *
from ttk import *
import widget.browser


class MessageView(Toplevel):
    '''
    An HTML viewer for a message.
    '''

    def __init__(self, master):
        '''
        Constructor
        '''
        Toplevel.__init__(self, master)
        self.view = widget.browser.Browser(self)
        self.view.pack(fill=BOTH, expand=1)
    
    def load_from_message(self, message):
        payloadText = ""
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_maintype() == 'text':
                payloadText += part.get_payload(decode = True)
        self.view.load_text(payloadText)
        self.title(message['Subject'])
