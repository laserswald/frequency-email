#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      untitled.py
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
import tkFont
from HTMLParser import HTMLParser
import logging
import tkSimpleDialog
import StringIO


class BlockParser(HTMLParser):
    """Translates HTML into a tree."""
    tag_stack = []
    data_stack = []
    blocks = []
    blockhasnothing = False

    def __init__(self, parent, document = None):
        self.parent = parent
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        logging.debug(tag)
        if tag in ['b', 'i', 'tt']: #only basic font formatting tags
            self.parent.add_font_tag(tag)
        elif tag in ['div', 'span', 'font', 'center']:
            self.division(tag, attrs)
        else:
            self.parent.add_tag(tag)

    def handle_endtag(self, tag):
        if tag in ['b', 'i', 'tt']: #only font formatting tags
            self.parent.remove_font_tag(tag)
        else:
            self.parent.remove_tag(tag)

    def handle_data(self, data):
        self.parent.write(data)

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.parent.newline()

    def division(self, tag, attrs):
        if tag == 'center':
            self.parent.realign('center')

class fontholder:
    pass

class Browser(Frame):
    """ A simple web renderer. Supports Bold, italic, and underline."""
    builtFonts = {}
    enabledfont = []
    formatTag = ''
    normalTags = []
    alignTag = ''
    def __init__ (self, root):
        """
        Constructor.
        """

        Frame.__init__(self, root)
        self.window = Text(self, font = ('Times New Roman', 11))
        self.window.pack(side=TOP, expand=1)

        self.configureTags()
        self.parser = BlockParser(self)

    def add_tag (self, tag):
        self.normalTags.append(tag)

    def add_font_tag(self, tag):
        print 'Add Font Tag:', tag
        self.enabledfont.append(tag)
        self.generateFont()

    def generateFont(self):
        fonttag = ''
        x = fontholder()
        x.family = 'times'
        x.size = 12
        x.slant = 'roman'
        x.weight = 'normal'

        if 'b' in self.enabledfont:
            fonttag+='b'
            x.weight = 'bold'
        if 'i' in self.enabledfont:
            fonttag+='i'
            x.slant = 'italic'
        if 'tt' in self.enabledfont:
            fonttag+='tt'
            x.family = 'courier'
##        import pdb; pdb.set_trace()

        if fonttag in self.builtFonts:
            self.formatTag = fonttag
        else:
            self.builtFonts[fonttag] = tkFont.Font(family = x.family,
                                                   size = x.size,
                                                   weight = x.weight,
                                                   slant = x.slant)


            self.window.tag_config(fonttag, font = self.builtFonts[fonttag])
            self.formatTag = fonttag


    def remove_tag (self, tag):
        self.normalTags.remove(tag)

    def remove_font_tag(self, tag):
        self.enabledfont.remove(tag)
        self.generateFont()

    def realign(self, alignment):
        self.newline()
        if alignment in ['justify','center','left','right','']:
            self.alignTag = alignment



    def write (self, text):
        logging.debug(self.normalTags)
        logging.debug(self.formatTag)
        alltags = tuple(self.normalTags)
        alltags += (self.formatTag,)
        alltags += (self.alignTag,)


        self.window.insert(INSERT, text, alltags)


    def load (self, documentName):
        htmlfile = open(documentName)
        filelist = []
        for line in htmlfile.readlines():
            line = line.rstrip()
            strl = line.strip('\t')
            filelist.append(strl)
        done = ''.join(filelist)
        logging.debug(done)
        self.parser.feed(done)

    def load_text(self, text):
    	filestring = StringIO.StringIO(text)
    	filelist = []
    	for line in filestring.readlines():
            line = line.rstrip()
            strl = line.strip('\t')
            filelist.append(strl)
        done = ''.join(filelist)
        self.parser.feed(done)

    def configureTags (self):
        """ configures the tags for Browser. """
        self.window.tag_config("a", foreground = "blue", underline=1)
##        self.window.tag_bind('a', '<Button-1>')
        self.window.tag_config('u', underline=1)
        self.window.tag_config('center', justify = CENTER)
        self.window.tag_config('right', justify = RIGHT)

    def newline (self):
        self.window.insert(INSERT, '\n')

class MainApp(Frame):
    """ test application """

    def __init__ (self, root):
        """ Class initialiser """
        Frame.__init__(self, root)
        self.browser = Browser(root)
        self.browser.pack(fill=X, expand=1)
        testText = '''<html>
<head>
<title></title>
</head>
<body>
<!-- Put the body of your page below this line -->
<b>blarg</b> honk
flask
<!-- Put the body of your page above this line -->
</body>
</html>

'''
        self.browser.load_text(testText)


if __name__ == '__main__':
    app = Tk()
    main = MainApp(app)
    app.mainloop()
