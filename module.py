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

from PySide6.QtGui import QFont
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QApplication


# set window size and position
def init_win(self, wd=500, ht=500, move_x=0, move_y=0,
             bg="background-color: White", title="", icon=None):
    geometry = QApplication.primaryScreen().availableGeometry()
    self.screen_wd = geometry.width()
    self.screen_ht = geometry.height()
    self.setFixedSize(self.screen_wd * wd, self.screen_ht * ht)
    self.move(int(self.screen_wd * move_x), int(self.screen_wd * move_y))
    self.setStyleSheet(bg)
    self.setWindowTitle(title)
    if icon is not None:
        self.setWindowIcon(icon)


# set font
def custom_font(widget=None, font_size=12, bold=False, underline=False):
    font = QFont()
    font.setPointSize(font_size)
    font.setBold(bold)
    font.setUnderline(underline)
    widget.setFont(font)

# validation
def alpha_or_space(text):
    if all(char.isalpha() or char.isspace() for char in text):
        return True
    else:
        return False


def valid_space(text):
    space = 0
    for char in text:
        if char == ' ':
            space = space + 1
            if space > 1:
                return False
        else:
            space = 0
    return True


def min_length(length, min_len):
    if length >= min_len:
        return True
    else:
        return False


def is_unique(mobile_number, rec_id):
    result = (True, '')
    if rec_id is None:
        query = QSqlQuery(f'SELECT id, name, contact FROM contacts')
    else:
        query = QSqlQuery(f'SELECT id, name, contact FROM contacts WHERE id != {rec_id}')

    while query.next():
        person_name = query.value(1)
        person_contact = query.value(2)
        if person_contact == mobile_number:
            result = (False, person_name)
            return result
    return result
