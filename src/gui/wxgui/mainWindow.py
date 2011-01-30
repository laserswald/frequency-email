#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 Ben Davenport-Ray <laserdude11@gmail.com>
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
import wx
from logic.mainLogic import MainWindowLogic as logic
class FrequencyMainWx(wx.Frame):
	""" The main window of Frequency using WxWidgets. """
	
	def __init__ (self):
		""" Class initialiser """
		wx.Frame.__init__(self, None, wx.ID_ANY, "Frequency")
		self.setupWidgets()
		
		
	def setupWidgets (self):
		"""
		Sets up the wxPython widgets.
		"""
		#This section creates the menu bar.
		sendIcon = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (24, 24))
		composeIcon = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (24, 24))
		
		self.fileMenu = wx.Menu()
		self.fileMenuAccount = self.fileMenu.Append(wx.ID_ANY, '&Account...', 'Edit accounts.')
		self.Bind(wx.EVT_MENU, logic.edit_account, self.fileMenuAccount)
		self.fileMenuExit = self.fileMenu.Append(wx.ID_EXIT, '&Exit', 'Quit Frequency.')
		self.Bind(wx.EVT_MENU, self.onExit, self.fileMenuExit)
		self.helpMenu = wx.Menu()
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.fileMenu, "&File")
		self.SetMenuBar(self.menuBar)
		
		#this section creates the Toolbar.
		self.toolbar = self.CreateToolBar()
		self.toolbar.AddLabelTool(-1, 'Send Mail', sendIcon)
		self.toolbar.AddLabelTool(-1, 'Compose', composeIcon)
		self.toolbar.Realize()

	def onExit(self, event):
		self.Close(True)
		

def start():
	app = wx.App(False)
	frame = FrequencyMainWx()
	frame.Show(True)
	app.MainLoop()
