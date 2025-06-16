from PyQt6 import QtWidgets, uic
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('main.ui', self)
        self.nextPageButton.clicked.connect(self.new_user_button)

    def new_user_button(self):
        username = self.newNameInput.text()
        password = self.newPasswordInput.text()
        print(username)


def app():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    app()
