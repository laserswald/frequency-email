from Tkinter import *
from ttk import *

class MessageList(Treeview):
	'''
	the main message display gui. 
	
	'''
	keys = []
	numofItems = 0
	fonts = {}
	
	def __init__(self, master):
		'''
		class initializer
		'''
		self.columns = ['Subject', 'From', 'Date']
		Treeview.__init__(self, master, columns = self.columns, show='headings')
		for head in self.columns:
			self.heading(head, text = head)
		self.setup_fonts()

		
	def add_message(self, message):
		'''
		Adds a message to the list.
		'''
		treevalues = (message['Subject'], message['From'], message['Date'])
		flags = message.get_flags().split()
		self.insert('', 'end', values=treevalues)
	
	def remove_message(self, index):
		'''
		Removes the message at index.
		'''
		print "remove_message called"
	
	def map_messages(self, msgmap):
		'''
		Maps many messages and adds them.
		'''
		print "map_messages called"
	
	def clear(self):
		'''
		Removes all messages.
		'''
		print "clear called"
		
	def setup_fonts(self):
		'''
		Sets up the fonts for the messages.
		'''

		
	def sortby(self, col, descending):
		"""Sort self contents when a column is clicked on."""
		# grab values to sort
		data = [(self.set(child, col), child) for child in self.get_children('')]
		if col == 'Date':
			newData = []
			for index, item in enumerate(data):
				date = item[0]
				dataitem = (rfc822.parsedate(date), index, item)
				newData.append(dataitem)

			newData.sort(reverse=descending)
			for set in enumerate(newData):
				print set
				parsedate, indx, item = set
				self.move(item[1], '', indx)
		# reorder data
		data.sort(reverse=descending)
		for indx, item in enumerate(data):
			self.move(item[1], '', indx)

		# switch the heading so that it will sort in the opposite direction
		self.heading(col,
			command=lambda col=col: self.sortby(self, col, int(not descending)))
				

if __name__ == '__main__':
	app = Tk()
	app.columnconfigure(0, weight = 1)
	msglist = MessageList(app)
	msglist.grid()
	msglist.create_item('Title', 'Lorem ipsum, dolor sit amet')	
	msglist.create_item('Title', 'Lorem ipsum, dolor sit amet')	
	app.mainloop()
	