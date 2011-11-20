class AccountError(Exception):
	def __init__(self, error):
		self.value = error
