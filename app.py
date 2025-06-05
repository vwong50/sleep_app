from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QSize, Qt
import sys # For command line stuff, idk.

# Makes QMainWindow a subclass
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__() # Initialises QMainWindow
		self.setWindowTitle("Prototype") 	
		self.button = QPushButton("Button")

		# Signal
		self.button.clicked.connect(self.button_clicked) 
		self.setCentralWidget(self.button)
		self.setMinimumSize(QSize(500, 500))

	# Slot for button_clicked
	def button_clicked(self):
		# Updates the interface
		self.button.setText("Clicked")
		self.button.setEnabled(False)

		self.setWindowTitle("Prototyp: Revamped")

# Starts the app
app = QApplication(sys.argv) # Starts app

window = MainWindow()
window.show() # Shows parent GUI

app.exec()
