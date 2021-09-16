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

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon, QAction
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QTableView, QAbstractItemView, QPushButton, QDialog,
                               QLineEdit, QMessageBox, QLabel, QComboBox)

from .about import About
from .models import ContactsModel, UsersModel
from .contacts import MangeDialog
from .change_password import ChangePassword
from .module import custom_font, init_win


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.user_no = 1
        self.setWindowModality(Qt.ApplicationModal.WindowModal)
        self.wd = .8
        self.ht = .962
        self.bg = 'background-color: rgb(100, 150, 255)'
        self.title = "Contacts Book"
        self.icon = QIcon('icons/app132.png')
        init_win(self, wd=self.wd, ht=self.ht, move_x=.1, move_y=0, bg=self.bg,
                 title=self.title, icon=self.icon)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)

        self.button_bg = 'background-color: rgba(190, 190, 190, 1); color: Blue'
        self.edit_bg = 'background-color: rgba(255, 255, 255, .75)'
        self.combo_bg = 'background-color: rgba(50, 145, 255, 1)'

        self.contactsModel = ContactsModel(self)
        self.usersModel = UsersModel(self)

        self.createMenu()
        self.createToolbar()
        self.setupUI()
        self.create_statusbar()

    def createMenu(self):
        # create actions
        self.actionResetUserPassword = QAction(QIcon('icons/reset_password.png'), 'Reset User &Password', self)
        self.actionResetUserPassword.setShortcut("Ctrl+P")
        self.actionResetUserPassword.setStatusTip("Reset user password to default")
        self.actionResetUserPassword.triggered.connect(self.onResetUserPassword)
        self.actionResetUserPassword.setEnabled(False)

        self.actionChangePassword = QAction(QIcon('icons/change_password.png'), 'Change Pass&word', self)
        self.actionChangePassword.setShortcut("Ctrl+W")
        self.actionChangePassword.setStatusTip("Change current password")
        self.actionChangePassword.triggered.connect(self.onChangePassword)

        self.actionAbout = QAction(QIcon('icons/about.png'), 'A&bout', self)
        self.actionAbout.setShortcut("Ctrl+B")
        self.actionAbout.setStatusTip("About the application and developer")
        self.actionAbout.triggered.connect(self.onAbout)

        # create menus
        self.menuBar().setStyleSheet("background-color: rgb(120, 200, 120)")
        self.adminMenu = self.menuBar().addMenu("A&dmin")
        self.userMenu = self.menuBar().addMenu("U&ser")

        # adding action to menus
        self.adminMenu.addAction(self.actionResetUserPassword)

        self.userMenu.addAction(self.actionChangePassword)
        self.userMenu.addAction(self.actionAbout)

    def createToolbar(self):
        # set tooltip
        self.actionChangePassword.setToolTip("Change current password")
        self.actionAbout.setToolTip("About the application and developer")

        # create toolbar
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.setStyleSheet("background-color: rgb(50, 170, 150)")
        self.mainToolBar.addAction(self.actionChangePassword)
        self.mainToolBar.addAction(self.actionAbout)


    def setupUI(self):
        self.model = self.contactsModel.model

        # Create table view widget
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setStyleSheet("background-color: rgb(220, 220, 255)")
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setAutoScroll(True)
        self.table.hideColumn(0)

        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 225)
        self.table.setColumnWidth(3, 215)

        # Create other widgets
        self.addButton = QPushButton(QIcon('icons/add.png'), '&Add')
        self.addButton.setStatusTip("Add new record")
        self.addButton.setStyleSheet(self.button_bg)
        self.addButton.clicked.connect(self.onAddContact)

        self.updateButton = QPushButton(QIcon('icons/update.png'), "&Update")
        self.updateButton.setStatusTip("Edit the selected record")
        self.updateButton.setStyleSheet(self.button_bg)
        self.updateButton.clicked.connect(self.onUpdateContact)

        self.removeButton = QPushButton(QIcon('icons/remove.png'), "&Remove")
        self.removeButton.setStatusTip("Delete the selected record")
        self.removeButton.setStyleSheet(self.button_bg)
        self.removeButton.clicked.connect(self.onRemoveContact)

        self.exitButton = QPushButton(QIcon('icons/exit.png'), "E&xit")
        self.exitButton.setStatusTip("Quit application")
        self.exitButton.setStyleSheet(self.button_bg)
        self.exitButton.clicked.connect(self.close)

        self.searchLabel = QLabel('Search &Criteria')
        self.searchLabel.setFixedWidth(150)
        custom_font(self.searchLabel, 12)

        self.searchCombo = QComboBox()
        self.searchCombo.setFixedWidth(275)
        custom_font(self.searchCombo, 14)
        self.searchCombo.setStyleSheet(self.combo_bg)
        self.searchCombo.addItems(['Select',
                                   'Search by Name', 'Search by Job',
                                   'Search by Location', 'Search by Contact Number'])
        self.searchCombo.setCurrentIndex(0)
        self.searchCombo.currentIndexChanged.connect(self.onIndexChanged)

        self.searchLabel.setBuddy(self.searchCombo)

        self.searchEdit = QLineEdit()
        self.searchEdit.setStyleSheet(self.edit_bg)
        self.searchEdit.setFixedWidth(300)
        custom_font(self.searchEdit, 14)
        self.searchEdit.setVisible(False)
        self.searchEdit.addAction(QIcon('icons/search.png'), QLineEdit.ActionPosition.LeadingPosition)
        self.searchEdit.setClearButtonEnabled(True)
        self.searchEdit.textChanged.connect(self.onTextChanged)
        self.searchEdit.setStatusTip("Enter the name of the person to be searched")

        self.messageLabel = QLabel()
        self.messageLabel.setAlignment(Qt.AlignCenter)
        custom_font(self.messageLabel, font_size=10, bold=True)
        self.messageLabel.setStyleSheet("color: Blue")
        self.messageLabel.setVisible(False)

        # declare layout
        right_layout = QVBoxLayout()  # accommodates all buttons
        top_layout = QHBoxLayout()  # accommodates table and right_layout
        bottom_layout = QHBoxLayout()  # accommodates search searchCombo and searchEdit
        bottom_layout.setSpacing(30)

        # right layout
        right_layout.addSpacing(25)
        right_layout.addWidget(self.addButton)

        right_layout.addSpacing(15)
        right_layout.addWidget(self.updateButton)

        right_layout.addSpacing(15)
        right_layout.addWidget(self.removeButton)

        right_layout.addSpacing(15)
        right_layout.addWidget(self.exitButton)

        right_layout.addStretch()

        # top layout
        top_layout.addSpacing(40)
        top_layout.addWidget(self.table)
        top_layout.addSpacing(20)
        top_layout.addLayout(right_layout)
        top_layout.addSpacing(40)

        # bottom layout
        bottom_layout.addSpacing(40)
        bottom_layout.addWidget(self.searchLabel)
        bottom_layout.addWidget(self.searchCombo)
        bottom_layout.addWidget(self.searchEdit)
        #bottom_layout.addWidget(self.messageLabel)
        bottom_layout.addStretch()

        # main layout
        self.main_layout.setContentsMargins(0, 20, 0, 20)
        self.main_layout.addWidget(self.messageLabel)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(top_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(bottom_layout)

        self.searchEdit.setFocus()

    def create_statusbar(self):
        curr_date = QDate.currentDate()
        self.statusLabel = QLabel(curr_date.toString('dd-MMM-yyyy'))
        self.statusLabel.setStyleSheet('border :2px solid blue;')
        self.statusBar().addPermanentWidget(self.statusLabel, 0)
        self.statusBar().setStyleSheet('border :1px solid black;')
        # self.statusBar().setStyleSheet('background-color: rgb(50, 170, 150); border :1px solid black;')

    def keyPressEvent(self, event):
        if event.key == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        confirm = QMessageBox.question(self, "Confirm Exit ", f"Are you sure you want to exit?")
        if confirm == QMessageBox.Yes:

            self.conn.close()
            self.conn.setDatabaseName("")
            QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

            event.accept()
        else:
            event.ignore()

    def onIndexChanged(self):
        self.messageLabel.setVisible(False)
        self.searchEdit.setText('')
        if self.searchCombo.currentIndex() == 0:
            self.searchEdit.setVisible(False)
            self.model.setFilter('')
        else:
            self.searchEdit.setVisible(True)
            self.searchEdit.setFocus()
            if self.searchCombo.currentIndex() == 1:
                self.searchEdit.setPlaceholderText('Enter Name')
            elif self.searchCombo.currentIndex() == 2:
                self.searchEdit.setPlaceholderText('Enter Job')
            elif self.searchCombo.currentIndex() == 3:
                self.searchEdit.setPlaceholderText('Enter Location')
            elif self.searchCombo.currentIndex() == 4:
                self.searchEdit.setPlaceholderText('Enter Contact Number')

    def onTextChanged(self, text):
        if self.searchCombo.currentIndex() == 1:
            self.model.setFilter("name like '" + text + "%'")
        elif self.searchCombo.currentIndex() == 2:
            self.model.setFilter("job like '" + text + "%'")
        elif self.searchCombo.currentIndex() == 3:
            self.model.setFilter("location like '" + text + "%'")
        elif self.searchCombo.currentIndex() == 4:
            self.model.setFilter("contact like '" + text + "%'")
        else:
            self.model.setFilter('')

    def onAddContact(self):
        self.messageLabel.setVisible(False)

        self.table.clearSelection()
        dialog = MangeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.searchCombo.setCurrentIndex(0)
            self.messageLabel.setVisible(True)

    def onUpdateContact(self):
        self.messageLabel.setVisible(False)
        if self.table.selectedIndexes():
            row = self.table.currentIndex().row()
            record = self.model.record(row)
            dialog = MangeDialog(self, record)
            if dialog.exec() == QDialog.Accepted:
                self.contactsModel.updateContact(row, dialog.data)
                self.searchCombo.setCurrentIndex(0)
                self.messageLabel.setVisible(True)
        else:
            QMessageBox.information(self, "Update Contact",
                                    "Please select the record before clicking the Update button")

        self.table.clearSelection()

    def onRemoveContact(self):
        self.messageLabel.setVisible(False)
        if self.table.selectedIndexes():
            row = self.table.currentIndex().row()
            reord = self.model.record(row)
            name = reord.value(1)
            message = f"Do you want to remove '{name}' from your Contact Book?"
            answer = QMessageBox.warning(self, "Remove Contact", message, QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.contactsModel.removeContact(row)
                self.searchCombo.setCurrentIndex(0)
                self.messageLabel.setVisible(True)
        else:
            QMessageBox.information(self, "Remove Contact",
                                    "Please select the record before clicking the Remove button")

        self.table.clearSelection()

    def onChangePassword(self):
        self.searchCombo.setCurrentIndex(0)
        dlg = ChangePassword(self.user_no, self)
        dlg.show()

    def onAbout(self):
        self.searchCombo.setCurrentIndex(0)
        dlg = About(self)
        dlg.show()

    def onResetUserPassword(self):
        self.searchCombo.setCurrentIndex(0)
        self.usersModel.resetUserPassword()
