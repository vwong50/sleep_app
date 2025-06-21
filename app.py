import os
import sqlite3 as sql
import sys
from datetime import datetime, timedelta

import numpy

os.environ["QT_API"] = "PyQt6"

from PyQt6 import QtWidgets, uic
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('QtAgg')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.parent = parent
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = MplCanvas(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Objects (Not used, just good practise)
        self.username = None
        self.password = None
        self.sleep_goal = None
        self.sleep_amount = None
        self.id = None

        # Load the UI Page
        uic.loadUi('main.ui', self)

        # Signals
        self.pagesWidget.setCurrentIndex(1)
        self.signUpBtn.clicked.connect(self.sign_up_btn_pressed)
        self.signInBtn.clicked.connect(self.sign_in_btn_pressed)
        self.plotButton.clicked.connect(self.plot)
        self.sleepcalcBtn.clicked.connect(self.sleep_calculator)
        self.nextPageBtn1.clicked.connect(self.tab_1_btn)
        self.nextPageBtn2.clicked.connect(self.tab_2_btn)
        self.nextPageBtn3.clicked.connect(self.main_page_btn)

    def plot(self):
        con = sql.connect("users.db")
        cur = con.cursor()
        print(self.id)
        x = cur.execute(
            "SELECT sleeping FROM users WHERE id=?", (self.id,)
        ).fetchone()
        y = cur.execute(
            "SELECT bedtime FROM users WHERE id=?", (self.id,)
        ).fetchone()
        x = [x[0]]
        y = [y[0]]
        con.close()

        model = numpy.poly1d(numpy.polyfit(x, y, 24))

        line = numpy.linspace(1, 24, 12)

        plt.scatter(x, y)
        plt.plot(line, model(line))
        plt.show()

    def sleep_calculator(self):
        bedtime = datetime.strptime(f"{self.bedtimeInput.value()}:0", "%H:%M")

        # Time delta formats into dates
        asleep_time = timedelta(minutes=15)
        sleep_cycle = timedelta(minutes=90)

        start_sleep_time = bedtime + asleep_time

        wake_up_times = []
        for cycles in range(5, 9):
            wake_up_time = start_sleep_time + (sleep_cycle * cycles)
            wake_up_times.append(wake_up_time.strftime("%H:%M"))

        self.time1.setText(f"{wake_up_times[0]}")
        self.time2.setText(f"{wake_up_times[1]}")
        self.time3.setText(f"{wake_up_times[2]}")
        self.time4.setText(f"{wake_up_times[3]}")

    def sign_up_btn_pressed(self):
        self.FormPage.setCurrentIndex(0)
        self.pagesWidget.setCurrentIndex(0)

    def sign_in_btn_pressed(self):
        con = sql.connect("users.db")
        cur = con.cursor()
        u_form = self.nameInput.text()
        p_form = self.passwordInput.text()

        u_db = cur.execute(
            "SELECT id, name FROM users WHERE name=?", (u_form,)
        ).fetchone()

        p_db = cur.execute(
            "SELECT id, password FROM users WHERE password=?", (p_form,)
        ).fetchone()
        if u_db is None or p_db is None:
            return None
        elif u_form == u_db[1] and p_form == p_db[1] and p_db[0] == u_db[0]:
            self.pagesWidget.setCurrentIndex(2)
            self.id = u_db[0]
            return u_db[0]
        else:
            return None

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
    p_app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(p_app.exec())


if __name__ == '__main__':
    app()
