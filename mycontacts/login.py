"""
    Copyright © 2021  Mosleuddin Sarkar

    This file is part of MyContacts.

    MyContacts is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MyContacts is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MyContacts.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox)

from .database import createTables
from .main_window import MainWindow
from .models import UsersModel
from .module import custom_font


class LogInWindow(QDialog):
    def __init__(self):
        super(LogInWindow, self).__init__()

        if not self.createConnection():
            sys.exit(1)

        self.model = UsersModel(self).model
        if not self.model.rowCount():
            UsersModel(self).addUser()

        self.setWindowIcon(QIcon('icons/app32.png'))
        self.setWindowTitle('MyContacts')
        self.setStyleSheet("background-color: rgb(50, 170, 150)")
        self.setFixedSize(600, 400)
        self.main_window_open = False           # whether MainWindow is called or not
        self.initUI()
        self.show()

    def initUI(self):
        self.label_heading = QLabel('Please enter correct credentials')
        custom_font(self.label_heading, font_size=16, underline=True)
        self.label_heading.setAlignment(Qt.AlignCenter)

        self.label_invalid_login = QLabel('Invalid username/password')
        self.label_invalid_login.setAlignment(Qt.AlignCenter)
        self.label_invalid_login.setStyleSheet('color:Red')
        self.label_invalid_login.hide()

        self.label_username = QLabel('&Username')
        self.edit_username = QLineEdit()
        self.edit_username.setMaxLength(20)
        self.edit_username.setPlaceholderText('username')
        self.edit_username.setStyleSheet('background-color: rgb(200, 200, 200); font-size: 18px')
        self.label_username.setBuddy(self.edit_username)

        self.label_password = QLabel('&Password')
        self.edit_password = QLineEdit()
        self.edit_password.setMaxLength(20)
        self.edit_password.setPlaceholderText('password')
        self.edit_password.setStyleSheet('background-color: rgb(200, 200, 200); font-size: 18px')
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.label_password.setBuddy(self.edit_password)

        self.btn_login = QPushButton(QIcon('icons/check.png'), '&Login')
        self.btn_login.setStyleSheet('background-color: rgb(125, 0, 200); font-size: 18px')
        self.btn_login.setFixedSize(150, 35)
        self.btn_login.setEnabled(False)

        self.btn_close = QPushButton(QIcon('icons/remove.png'), '&Close')
        self.btn_close.setStyleSheet('background-color: rgb(255, 50, 50); font-size: 18px')
        self.btn_close.setFixedSize(150, 35)

        # set events
        self.btn_login.clicked.connect(self.onLogin)
        self.btn_close.clicked.connect(self.close)
        self.edit_username.textChanged.connect(self.onTextChange)
        self.edit_password.textChanged.connect(self.onTextChange)

        # setting layout
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        heading_layout = QHBoxLayout()
        btns_layout = QHBoxLayout()

        heading_layout.addSpacing(40)
        heading_layout.addWidget(self.label_heading)

        form_layout.setHorizontalSpacing(30)
        form_layout.setContentsMargins(50, 10, 50, 10)
        form_layout.addRow(self.label_username, self.edit_username)
        form_layout.addRow(self.label_password, self.edit_password)

        btns_layout.addSpacing(40)
        btns_layout.addWidget(self.btn_close)
        btns_layout.addWidget(self.btn_login)

        main_layout.addSpacing(20)
        main_layout.addLayout(heading_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.label_invalid_login)
        main_layout.addSpacing(20)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(btns_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def onLogin(self):
        username = self.edit_username.text()
        password = self.edit_password.text()

        admin_record = self.model.record(0)
        admin_username = admin_record.field(1).value()
        admin_password = admin_record.field(2).value()

        user_record = self.model.record(1)
        user_username = user_record.field(1).value()
        user_password = user_record.field(2).value()

        if (username == admin_username and password == admin_password) or (username == user_username and password == user_password):
            win = MainWindow()
            win.conn = self.conn
            win.show()
            self.main_window_open = True
            self.close()

            if username == admin_username and password == admin_password:
                win.user_no = 0
                win.actionResetUserPassword.setEnabled(True)
        else:
            self.label_invalid_login.show()
            self.edit_password.setText('')

    def onTextChange(self, text):
        if text:
            self.label_invalid_login.hide()
            self.btn_login.setEnabled(True)
        else:
            self.btn_login.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        if not self.main_window_open:
            self.conn.close()
            self.conn.setDatabaseName("")
            QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

        event.accept()

    def createConnection(self):
        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("contacts.sqlite")
        if not self.conn.open():
            QMessageBox.warning(None, "Database Error",
                                f"Unable to connect to the database\n\n{self.conn.lastError().text()}")
            return False

        createTables()
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily('Verdana, Helvetica, sans-serif')
    font.setPointSize(12)
    app.setFont(font)
    my_win = LogInWindow()
    my_win.show()
    app.exec_()
    sys.exit()
