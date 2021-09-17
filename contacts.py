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
from PySide6.QtGui import QIntValidator, QIcon
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                               QLineEdit, QDialogButtonBox, QApplication, QLabel)

from module import valid_space, min_length, alpha_or_space, is_unique, custom_font


class MangeDialog(QDialog):
    def __init__(self, parent, record=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.record = record
        self.data = None
        self.wd = int(self.parent.width() * .5)
        self.ht = int(self.parent.height() * .5)
        self.resize(self.wd, self.ht)
        self.setWindowModality(Qt.WindowModal)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.setupUI()

        QApplication.instance().focusChanged.connect(self.onFocusChanged)

    def setupUI(self):
        # Create line edits for data fields
        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText('Enter name')
        self.nameEdit.setObjectName('Name')
        self.nameEdit.setMaxLength(30)
        self.nameEdit.addAction(QIcon('icons/edit.png'), QLineEdit.ActionPosition.LeadingPosition)
        self.nameEdit.textChanged.connect(self.onTextChanged)

        self.jobEdit = QLineEdit()
        self.jobEdit.setPlaceholderText('Enter occupation')
        self.jobEdit.setObjectName("Job")
        self.jobEdit.setMaxLength(20)
        self.jobEdit.addAction(QIcon('icons/edit.png'), QLineEdit.ActionPosition.LeadingPosition)
        self.jobEdit.textChanged.connect(self.onTextChanged)

        self.locationEdit = QLineEdit()
        self.locationEdit.setPlaceholderText('Enter location')
        self.locationEdit.setObjectName("Location")
        self.locationEdit.setMaxLength(20)
        self.locationEdit.addAction(QIcon('icons/edit.png'), QLineEdit.ActionPosition.LeadingPosition)
        self.locationEdit.textChanged.connect(self.onTextChanged)

        self.contactEdit = QLineEdit()
        self.contactEdit.setPlaceholderText('Enter contact number')
        self.contactEdit.setObjectName("Contact")
        self.contactEdit.setMaxLength(10)
        self.contactEdit.addAction(QIcon('icons/edit.png'), QLineEdit.ActionPosition.LeadingPosition)
        self.contactEdit.setValidator(QIntValidator())
        self.contactEdit.textChanged.connect(self.onTextChanged)

        self.errorLabel = QLabel()
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setStyleSheet('color: rgb(255, 0, 0)')
        custom_font(self.errorLabel, font_size=12, bold=False)
        self.errorLabel.setWordWrap(True)
        self.errorLabel.setVisible(False)

        # Lay out the data fields
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(30)
        form_layout.setVerticalSpacing(20)

        form_layout.addRow("&Name", self.nameEdit)
        form_layout.addRow("&Job", self.jobEdit)
        form_layout.addRow("&Location", self.locationEdit)
        form_layout.addRow("Con&tact Number", self.contactEdit)

        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox()
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonsBox.setStyleSheet('background-color: rgba(150, 150, 150, 1)')
        self.buttonsBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)

        self.main_layout.addLayout(form_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.errorLabel)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.buttonsBox)
        self.main_layout.addStretch()

        self.nameEdit.setFocus()

        self.line_edits = [self.nameEdit, self.jobEdit, self.locationEdit, self.contactEdit]

        for widget in self.line_edits:
            widget.setStyleSheet('background-color: rgb(245, 245, 245)')

        if self.record is None:
            self.setWindowTitle("Add Contact")
            self.setStyleSheet("background-color: rgb(150, 200, 145)")
        else:
            self.setWindowTitle("Update Contact")
            self.setStyleSheet("background-color: rgb(150, 200, 125)")

            self.load_record()

    def load_record(self):
        for index, widget in enumerate(self.line_edits):
            widget.setText(self.record.field(index + 1).value())

        self.buttonsBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.nameEdit.setFocus()

    def onFocusChanged(self, old, now):
        for widget in self.line_edits:
            if widget == old:
                txt = widget.text().upper()
                widget.setText(txt)
            elif widget == now:
                widget.deselect()

    def onTextChanged(self, text):
        if self.errorLabel.isVisible():
            self.errorLabel.setVisible(False)

        if text:
            self.buttonsBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonsBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def show_error(self, error_type, widget, min_len=None, name=None):
        error_msg = ''
        if error_type == 'alpha_space_error':
            error_msg = f'\t{widget.objectName()} field accepts only alphabets and space(s)'

        elif error_type == 'space_error':
            error_msg = '\tTwo or more continuous spaces are not allowed in {widget.objectName()} field'

        elif error_type == 'length_error':
            error_msg = f'\tMinimum {min_len} characters required for {widget.objectName()} field'

        elif error_type == 'unique_error':
            error_msg = f'\tContact number {widget.text()} used by {name}'

        self.errorLabel.setText(f'{error_msg}')
        self.errorLabel.setVisible(True)
        widget.setFocus()

    def accept(self):
        sender = self.sender()
        name = self.nameEdit.text().strip()
        job = self.jobEdit.text().strip()
        location = self.locationEdit.text().strip()
        contact_number = self.contactEdit.text().strip()

        # validate name
        if not alpha_or_space(name):
            self.show_error('alpha_space_error', self.nameEdit)
            return False

        elif not valid_space(name):
            self.show_error('space_error', self.nameEdit)
            return False

        elif not min_length(len(name), 3):
            self.show_error('length_error', self.nameEdit, 3)
            return False

        # validate job
        if not alpha_or_space(job):
            self.show_error('alpha_space_error', self.jobEdit)
            return False

        elif not valid_space(job):
            self.show_error('space_error', self.jobEdit)
            return False

        elif not min_length(len(job), 3):
            self.show_error('length_error', self.jobEdit, 3)
            return False

        # validate location
        if not alpha_or_space(location):
            self.show_error('alpha_space_error', self.locationEdit)
            return False

        elif not valid_space(location):
            self.show_error('space_error', self.locationEdit)
            return False

        elif not min_length(len(location), 3):
            self.show_error('length_error', self.locationEdit, 3)
            return False

        # validate contact
        if not min_length(len(contact_number), 10):
            self.show_error('length_error', self.contactEdit, 10)
            return False

        if self.record is None:
            person_id = None
        else:
            person_id = self.record.field(0).value()

        result = is_unique(contact_number, person_id)
        if not result[0]:
            self.show_error('unique_error', self.contactEdit, name=result[1])
            return False

        self.data = []
        for index, widget in enumerate(self.line_edits):
            self.data.append(widget.text().strip().upper())

        super().accept()
