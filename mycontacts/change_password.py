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

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QLineEdit, QPushButton)

from mycontacts.models import UsersModel
from mycontacts.module import custom_font


class ChangePassword(QDialog):
    def __init__(self, rec_no, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.usersModel = UsersModel(self)
        self.rec_no = rec_no
        self.setWindowIcon(QIcon('icons/app32.png'))
        self.setWindowTitle('Contacts Book')
        self.setStyleSheet("background-color: rgb(100, 200, 200)")
        self.setFixedSize(600, 400)
        self.initUI()

    def initUI(self):
        self.label_heading = QLabel('Change Password')
        custom_font(self.label_heading, font_size=16, underline=True)
        self.label_heading.setAlignment(Qt.AlignCenter)

        self.label_error_msg = QLabel('')
        self.label_error_msg.setAlignment(Qt.AlignCenter)
        self.label_error_msg.setStyleSheet('color:Red')
        self.label_error_msg.hide()

        self.label_current_password = QLabel('Current &Password')
        self.edit_current_password = QLineEdit()
        self.edit_current_password.setMaxLength(20)
        self.edit_current_password.setEchoMode(QLineEdit.Password)
        self.edit_current_password.setPlaceholderText('current password')
        self.edit_current_password.setStyleSheet('background-color: rgb(200, 200, 200); font-size: 18px')
        self.label_current_password.setBuddy(self.edit_current_password)

        self.label_new_password = QLabel('&New Password')
        self.edit_new_password = QLineEdit()
        self.edit_new_password.setMaxLength(20)
        self.edit_new_password.setEchoMode(QLineEdit.Password)
        self.edit_new_password.setPlaceholderText('new password')
        self.edit_new_password.setStyleSheet('background-color: rgb(200, 200, 200); font-size: 18px')
        self.label_new_password.setBuddy(self.edit_new_password)

        self.label_confirm_password = QLabel('Con&firm Password')
        self.edit_confirm_password = QLineEdit()
        self.edit_confirm_password.setMaxLength(20)
        self.edit_confirm_password.setEchoMode(QLineEdit.Password)
        self.edit_confirm_password.setPlaceholderText('confirm password')
        self.edit_confirm_password.setStyleSheet('background-color: rgb(200, 200, 200); font-size: 18px')
        self.label_confirm_password.setBuddy(self.edit_confirm_password)

        self.btn_submit = QPushButton(QIcon('./icons/check.png'), '&Submit')
        self.btn_submit.setStyleSheet('background-color: rgb(125, 0, 200); font-size: 18px')
        self.btn_submit.setFixedSize(150, 35)
        self.btn_submit.setEnabled(False)

        self.btn_close = QPushButton(QIcon('./icons/remove.png'), '&Close')
        self.btn_close.setStyleSheet('background-color: rgb(255, 50, 50); font-size: 18px')
        self.btn_close.setFixedSize(150, 35)

        # set events
        self.btn_submit.clicked.connect(self.onSubmit)
        self.btn_close.clicked.connect(self.close)
        self.edit_current_password.textChanged.connect(self.onTextChange)
        self.edit_new_password.textChanged.connect(self.onTextChange)
        self.edit_confirm_password.textChanged.connect(self.onTextChange)

        # setting layout
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        heading_layout = QHBoxLayout()
        btns_layout = QHBoxLayout()

        heading_layout.addSpacing(40)
        heading_layout.addWidget(self.label_heading)

        form_layout.setHorizontalSpacing(30)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.addRow(self.label_current_password, self.edit_current_password)
        form_layout.addRow(self.label_new_password, self.edit_new_password)
        form_layout.addRow(self.label_confirm_password, self.edit_confirm_password)

        btns_layout.addSpacing(40)
        btns_layout.addWidget(self.btn_close)
        btns_layout.addWidget(self.btn_submit)

        main_layout.addSpacing(20)
        main_layout.addLayout(heading_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.label_error_msg)
        main_layout.addSpacing(20)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(btns_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def onSubmit(self):
        self.msg = ''
        self.model = self.usersModel.model
        record = self.model.record(self.rec_no)
        pwd = record.field(2).value()
        current_password = self.edit_current_password.text().strip()
        new_password = self.edit_new_password.text().strip()
        confirm_password = self.edit_confirm_password.text().strip()

        if not current_password == pwd:
            self.msg = 'Incorrect Password'
            self.edit_current_password.setFocus()

        elif len(new_password) < 4:
            self.msg = 'Length of Password should be 4 to 20 characters'
            self.edit_new_password.setFocus()

        elif new_password != confirm_password:
            self.msg = 'Confirm Password does not match with the New Password'
            self.edit_confirm_password.setFocus()

        elif new_password == current_password:
            self.msg = 'New Password must be different from the Current Password'
            self.edit_new_password.setFocus()

        else:
            self.usersModel.changePassword(self.rec_no, new_password)
            self.close()

        self.label_error_msg.setText(self.msg)
        self.label_error_msg.setVisible(True)
        self.edit_current_password.setText('')
        self.edit_new_password.setText('')
        self.edit_confirm_password.setText('')

    def onTextChange(self, text):
        if text:
            self.label_error_msg.hide()
            self.btn_submit.setEnabled(True)
        else:
            self.btn_submit.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        event.accept()
