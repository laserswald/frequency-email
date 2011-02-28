#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       TkinterRibbon.py
#
#       Copyright 2011 Ben Davenport-Ray <>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
from ToolFrame import ToolFrame

#
#  name: unknown
#  @param
#  @return
class TabbedToolbar(Notebook):
	""" A tabbed toolbar in the style of the Windows Ribbon. Don't rape
	me with your lawyers, please, Microsoft. """

	def __init__ (self, parent):
		""" Class initialiser """
		Notebook.__init__(self, parent)

	def add_toolframe(self, page):
		'''
		Adds a new toolframe onto the page given by page.
		'''
		toolframe = ToolFrame(page)
		toolframe.pack(fill = Y, expand = 1)
		return toolframe

	def add_page(self, title):
		'''
		Adds a new page to the tabbed toolbar.
		'''
		page = Frame(self)
		self.add(page, text = title)
		return page

class MainButton(Menubutton):
	""" the main button in the top left of the window. """

	def __init__ (self, parent, text=None, icon=None, compound=LEFT):
		""" Class initialiser """
		
		Menubutton.__init__(self, parent)
		self.menu = Menu(self)
		self.config(menu = self.menu)
		
		self.text = text
		if icon is not None:
			self.icon = ImageTk.PhotoImage(Image.open(icon))
		else:
			self.icon = None
		self.compound = compound

		self.reconfigure()

	def set_icon(self, image):
		self.icon = ImageTk.PhotoImage(Image.open(image))
		self.reconfigure()

	def set_text(self, text):
		'''
		Sets the text for the MainButton.
		'''
		self.icon = image
		self.reconfigure()
		
	def set_compound(self, compound):
		'''
		Sets the compoundness of the MainButton
		'''
		self.compound = compound
		self.reconfigure()	

	def reconfigure(self):
		self.config(text = self.text, image = self.icon, compound = self.compound)
		
	def addCommand(self, label, command, icon=None, compound=LEFT):
		'''
		Adds a new menu command to the menu.
		'''
		self.menu.add_command(label = label, image = icon, command = command, compound = compound)
	

class Ribbon(Frame):
	""" Class doc """

	def __init__ (self, parent):
		""" Class initialiser """
		Frame.__init__(self, parent, borderwidth=2, relief='raised')
		self.columnconfigure(1, weight = 1)
		self.menu = MainButton(self, parent)
		self.toolbar = TabbedToolbar(self)
		self.menu.grid(sticky = N+S+E+W)
		self.toolbar.grid(column = 1, sticky = E+W)
			
	def set_main_icon(self, icon):
		'''
		Sets the icon for the MainButton.
		'''
		self.menu.set_icon(icon)
		
	def set_main_text(self, text):
		'''
		Sets the text for the MainButton.
		'''
		self.menu.set_text(text)
		
	def set_main_compound(self, compound):
		'''
		Sets the compound for the MainButton.
		'''
		self.menu.set_compound(compound)
	


if __name__ == '__main__':
	app = Tk()
	rib = Ribbon(app)
	testingpage = rib.ttb.add_page('Testing')
	toolbar = rib.ttb.add_toolbar(testingpage)
	toolbar.insert('Test button', None, None)
	rib.pack(expand = 1, fill = X)
	textbox = Text(app)
	textbox.pack(expand = 1, fill = BOTH)
	app.mainloop()

