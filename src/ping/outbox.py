
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      sendMail.py
#
#      Copyright 2010 Ben Davenport-Ray <ben@benslaptop>
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

import smtplib


class Outbox:
    """ A list of mail messages that can be periodically sent to their recipients. """
    server = None;

    def __init__ (self, account):
        """
        Constructor.

        account -- the account that will be used to send mail.
        """
        self.queue = []
        self.account = account

    def add (self, message):
        """ Adds a message to the list.

        message -- The message to add.
        """
        self.queue.append(message)

    def send (self, password):
        """ sends all the messages """
        self.connect(secure = True)
        self.login(password)
        for mNumber in self.queue: #@UnusedVariable
            self.send_msg(self.queue.pop())
        self.close()
        

    def send_msg(self, message):
        self.server.sendmail(self.account.email, message['to'], message.as_string())
        
    def login(self, password):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.account.email, password)
        
    def connect(self, secure = False):
        if secure: 
            self.server = smtplib.SMTP_SSL(self.account.out_server, self.account.out_port)
        else:
            self.server = smtplib.SMTP_SSL(self.account.out_server, self.account.out_port)
            
    def disconnect(self):
        self.server.close()
