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

import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QMessageBox


class ContactsModel:
    def __init__(self, parent):
        self.model = QSqlTableModel()
        self.model.setTable("contacts")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setSort(1, Qt.AscendingOrder)
        self.model.select()
        self.parent = parent
        headers = ("ID", "Name", "Job", "Location", "Contact No.")
        for columnIndex, header in enumerate(headers):
            self.model.setHeaderData(columnIndex, Qt.Horizontal, header)

    def addContact(self, data):
        try:
            row = self.model.rowCount()
            self.model.insertRows(row, 1)
            for col, value in enumerate(data):
                self.model.setData(self.model.index(row, col + 1), value)
            self.model.submitAll()
            self.parent.messageLabel.setText('Record added successfully')
            self.model.select()
        except sqlite3.Error:
            self.parent.messageLabel.setText('Could not add record!')

    def updateContact(self, row, data):
        try:
            record = self.model.record(row)
            for col, value in enumerate(data):
                record.setValue(col + 1, value)
            self.model.updateRowInTable(row, record)
            self.model.submitAll()
            self.parent.messageLabel.setText('Record updated successfully')
            self.model.select()
        except sqlite3.Error:
            self.parent.messageLabel.setText('Could not update the record! Please try again')

    def removeContact(self, row):
        try:
            self.model.removeRow(row)
            self.model.submitAll()
            self.model.select()
            self.parent.messageLabel.setText('Record removed successfully')
        except Exception:
            self.parent.messageLabel.setText('Could not remove the record!')


class UsersModel:
    def __init__(self, parent):
        self.model = QSqlTableModel()
        self.model.setTable("users")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setSort(1, Qt.AscendingOrder)
        self.model.select()
        self.parent = parent
        headers = ("ID", "Username", "Password")
        for columnIndex, header in enumerate(headers):
            self.model.setHeaderData(columnIndex, Qt.Horizontal, header)

    def addUser(self):
        data = [('admin', 'manish_1975'), ('user', '1234')]
        for i in range(2):
            try:
                row = self.model.rowCount()
                self.model.insertRows(row, 1)
                for col, value in enumerate(data[i]):
                    self.model.setData(self.model.index(row, col + 1), value)
                self.model.submitAll()
                self.model.select()
            except sqlite3.Error:
                QMessageBox.critical(self.parent, 'Error', 'Could not create user!')

    def resetUserPassword(self):
        title = 'Reset User Credentials'
        password = 1234  # default password for user
        try:
            record = self.model.record(1)
            record.setValue(2, password)
            self.model.updateRowInTable(1, record)
            self.model.submitAll()
            self.model.select()
            msg = f'Password of the user have been reset to {password}'
            QMessageBox.information(self.parent, title, msg)
        except sqlite3.Error:
            QMessageBox.critical(self.parent, title, 'Error!!! Could not reset username and Password')

    def changePassword(self, rec_no, password):
        title = 'Change Password'
        try:
            record = self.model.record(rec_no)
            record.setValue(2, password)
            self.model.updateRowInTable(rec_no, record)
            self.model.submitAll()
            self.model.select()
            msg = 'Password has been changed successfully'
            QMessageBox.information(self.parent, title, msg)
        except sqlite3.Error:
            QMessageBox.critical(self.parent, title, 'Error!!! Could not Change Password')

    def removeUser(self, row):
        try:
            self.model.removeRow(row)
            self.model.submitAll()
            self.model.select()
            QMessageBox.information(self.parent, 'Remove User', 'User removed successfully')
        except Exception:
            QMessageBox.critical(self.parent, 'Error', 'Could not removed user!')
