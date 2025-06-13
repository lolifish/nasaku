from datetime import date

class UsrData():
	def __init__(self):
		self.id: int = None
		self.imp: int = None
		self.fish: int = None
		self.signin: date = None
		self.inventory: dict = {}
		self.chat: dict = []
	