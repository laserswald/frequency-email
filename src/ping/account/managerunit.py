import unittest
import manager as am

class AccountTests(unittest.TestCase):


	def setUp(self):
		self.manager = am.AccountManager()
		
	def test_new_account(self):
		self.manager.new_account()
		assertTrue
	
	def test_load_config(self):
		self.manager.loadConfigFile('wellformed.config')
	
	def test_load_malformed_config(self):
		self.manager.loadConfigFile("malformed.config")
		
	def test_save_config(self):
		self.manager.save_account()
	
if __name__ == "__main__":
	unittest.main()
	

