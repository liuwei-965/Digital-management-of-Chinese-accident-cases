

from GUI.LineNumber import LineMain
from GUI.ScrollBar import Scrollbar
# from StationeryFunctions import StationeryFunctions
# from PopupMenu import Popup
# from FIndAndReplace import FindReplaceFunctions
# from FileHandler import FileHandler
# from FontChooser import FontChooser
# from Settings import Configuration

class Connect:
	def __init__(self, pad):
		self.pad = pad
		self.modules_connections()


	def modules_connections(self):
		LineMain(self.pad)
		Scrollbar(self.pad)
		# StationeryFunctions(self.pad)
		# Popup(self.pad)
		# FindReplaceFunctions(self.pad)
		# FileHandler(self.pad)
		# FontChooser(self.pad)
#		Configuration(self.pad)
		return