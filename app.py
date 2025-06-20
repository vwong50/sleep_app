from PyQt6 import QtWidgets, uic
import sys
import sqlite3


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('main.ui', self)
        self.pagesWidget.setCurrentIndex(1)
        self.signUpBtn.clicked.connect(self.signUpBtn_pressed)
        self.signInBtn.clicked.connect(self.signInBtn_pressed)
        self.nextPageBtn1.clicked.connect(self.tab_1_btn)
        self.nextPageBtn2.clicked.connect(self.tab_2_btn)
        self.nextPageBtn3.clicked.connect(self.main_page_btn)

    def signUpBtn_pressed(self):
        self.FormPage.setCurrentIndex(0)
        self.pagesWidget.setCurrentIndex(0)

    def signInBtn_pressed(self):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        u_form = self.nameInput.text()
        p_form = self.passwordInput.text()

        u_db = cur.execute("SELECT name FROM users WHERE name=?", (u_form,)).fetchone()
        p_db = cur.execute("SELECT password FROM users WHERE password=?", (p_form,)).fetchone()
        if u_db is None or p_db is None:
            return None
        elif u_form == u_db[0] and p_form == p_db[0]:
            self.pagesWidget.setCurrentIndex(2)
        else:
            pass

    def tab_1_btn(self):
        # Store username and password
        self.username = self.newNameInput.text()
        self.password = self.newPasswordInput.text()
        self.FormPage.setCurrentIndex(1)

    def tab_2_btn(self):
        # Store sleep data
        self.sleep_goal = self.goalInput.value()
        self.sleep_amount = self.sleepInput.value()
        self.FormPage.setCurrentIndex(2)

    def main_page_btn(self):
        self.pagesWidget.setCurrentIndex(1)


def app():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    app()
