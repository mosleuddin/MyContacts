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

from PySide6.QtSql import QSqlQuery


def createTables():
    query = QSqlQuery()
    query.exec_("""
            CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name       VARCHAR(30)  NOT NULL,
            job        VARCHAR(20)  NOT NULL,
            location   VARCHAR(20)  NOT NULL,
            contact    CHAR(10)     NOT NULL)
        """)

    query.finish()

    query.exec("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                username   VARCHAR(20)  NOT NULL,
                password   VARCHAR(20)  NOT NULL)
            """)

    query.finish()





