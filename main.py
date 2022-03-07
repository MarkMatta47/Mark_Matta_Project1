import sys
import secrets
import requests
import sqlite3
from typing import Tuple
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QWidget
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os


file1 = open('output.txt', 'w')

imdb_id = ''
imdb_id_list = []


def main():
    id_num_list = ['tt7462410', 'tt5491994', 'tt0081834', 'tt0096697', 'tt1492966']

    app = QApplication(sys.argv)
    ex = MainWindow()
    print(ex)

    # get_movies_up()

    # # loop through list and write data for each show Id to output file
    for i in range(len(id_num_list)):
        print_show_data(id_num_list[i])
        file1.write('\n')

    get_top250_data()

    sys.exit(app.exec_())


def print_show_data(id_num: str):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{id_num}"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    # loop through ratings' data to format output display
    for key, value in data.items():
        if key == 'ratings':
            for i in range(len(data['ratings'])):
                for rating_key, rating_value in data['ratings'][i].items():
                    file1.writelines('\t' + rating_key + ' : ' + rating_value)
                file1.write('\n')
        else:
            file1.writelines(f'{key} : {value}')
            file1.write('\n')


def add_show_data_to_db(cursor: sqlite3.Cursor, conn):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    # loop through list of dictionaries assigned to "items" key
    for entry in data["items"]:
        cursor.execute('''INSERT INTO top_250_data (imdb_id, title, fullTitle, year, crew, imDbRating,
                        imDbRatingCount) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (entry['id'], entry['title'], entry['fullTitle'], entry['year'], entry['crew'],
                        entry['imDbRating'], entry['imDbRatingCount']))
        conn.commit()
    cursor.execute('''INSERT INTO top_250_data (imdb_id, title, fullTitle, year, crew, imDbRating,
                            imDbRatingCount) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   ('tt7462410', 'The Wheel of Time', 'The Wheel of Time (TV Series 2021– )', '2021',
                    'People', '0', '84387'))
    conn.commit()


def add_rating_data_to_db(cursor: sqlite3.Cursor, id_num: str, conn):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{id_num}"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    cursor.execute('''INSERT INTO ratings_data (imdb_id, total_rating, total_rating_votes, rating_percent_10,
    rating_votes_10, rating_percent_9, rating_votes_9, rating_percent_8, rating_votes_8, rating_percent_7,
    rating_votes_7, rating_percent_6, rating_votes_6, rating_percent_5, rating_votes_5, rating_percent_4,
    rating_votes_4, rating_percent_3, rating_votes_3, rating_percent_2, rating_votes_2, rating_percent_1,
    rating_votes_1) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                   (data['imDbId'], data['totalRating'], data['totalRatingVotes'],
                    data['ratings'][0]['percent'], data['ratings'][0]['votes'],
                    data['ratings'][1]['percent'], data['ratings'][1]['votes'],
                    data['ratings'][2]['percent'], data['ratings'][2]['votes'],
                    data['ratings'][3]['percent'], data['ratings'][3]['votes'],
                    data['ratings'][4]['percent'], data['ratings'][4]['votes'],
                    data['ratings'][5]['percent'], data['ratings'][5]['votes'],
                    data['ratings'][6]['percent'], data['ratings'][6]['votes'],
                    data['ratings'][7]['percent'], data['ratings'][7]['votes'],
                    data['ratings'][8]['percent'], data['ratings'][8]['votes'],
                    data['ratings'][9]['percent'], data['ratings'][9]['votes']))
    conn.commit()


def get_top250_data():
    # use secret key to get show data
    loc = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    for key, value in data.items():
        if key == 'items':
            for i in range(len(data['items'])):
                for rating_key, rating_value in data['items'][i].items():
                    file1.writelines(rating_key + ' : ' + rating_value)
                    file1.write('\n')
                file1.write('\n')
        else:
            file1.writelines(f'{key} : {value}')
            file1.write('\n')

    return data


def get_top_tvs(cursor: sqlite3.Cursor, conn):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/MostPopularTVs/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    for entry in data["items"]:
        cursor.execute('''INSERT INTO top_tvs (id, rank, rankUpDown, title, fullTitle, year, crew, imDbRating,
                        imDbRatingCount) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)''',
                       (entry['id'], entry['rank'], entry['rankUpDown'], entry['title'], entry['fullTitle'],
                        entry['year'], entry['crew'], entry['imDbRating'], entry['imDbRatingCount']))
        conn.commit()


def get_top250_movies(cursor: sqlite3.Cursor, conn):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/Top250Movies/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    for entry in data["items"]:
        cursor.execute('''INSERT INTO top_250_movies (id, rank, title, fullTitle, year, crew, imDbRating,
                        imDbRatingCount) VALUES (?, ?, ?, ?, ?, ?,?, ?)''',
                       (entry['id'], entry['rank'], entry['title'], entry['fullTitle'],
                        entry['year'], entry['crew'], entry['imDbRating'], entry['imDbRatingCount']))
        conn.commit()


def get_popular_movies(cursor: sqlite3.Cursor, conn):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/MostPopularMovies/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    for entry in data["items"]:
        cursor.execute('''INSERT INTO popular_movies (id, rank, rankUpDown, title, fullTitle, year, crew, imDbRating,
                        imDbRatingCount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (entry['id'], entry['rank'], entry['rankUpDown'], entry['title'], entry['fullTitle'],
                        entry['year'], entry['crew'], entry['imDbRating'], entry['imDbRatingCount']))
        conn.commit()


def get_movie_rating_data(cursor: sqlite3.Cursor, id_num: str, conn):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{id_num}"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    cursor.execute('''INSERT INTO movie_ratings_data (imdb_id, title, fullTitle, year, total_rating, total_rating_votes,
    rating_percent_10, rating_votes_10, rating_percent_9, rating_votes_9, rating_percent_8, rating_votes_8,
    rating_percent_7, rating_votes_7, rating_percent_6, rating_votes_6, rating_percent_5, rating_votes_5,
    rating_percent_4, rating_votes_4, rating_percent_3, rating_votes_3, rating_percent_2, rating_votes_2,
    rating_percent_1, rating_votes_1) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                   (data['imDbId'], data['title'], data['fullTitle'], data['year'],
                    data['totalRating'], data['totalRatingVotes'],
                    data['ratings'][0]['percent'], data['ratings'][0]['votes'],
                    data['ratings'][1]['percent'], data['ratings'][1]['votes'],
                    data['ratings'][2]['percent'], data['ratings'][2]['votes'],
                    data['ratings'][3]['percent'], data['ratings'][3]['votes'],
                    data['ratings'][4]['percent'], data['ratings'][4]['votes'],
                    data['ratings'][5]['percent'], data['ratings'][5]['votes'],
                    data['ratings'][6]['percent'], data['ratings'][6]['votes'],
                    data['ratings'][7]['percent'], data['ratings'][7]['votes'],
                    data['ratings'][8]['percent'], data['ratings'][8]['votes'],
                    data['ratings'][9]['percent'], data['ratings'][9]['votes']))
    conn.commit()


def get_movies_up():
    loc = f"https://imdb-api.com/en/API/MostPopularMovies/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    movie_rank_up_list = []
    for items in range(len(data['items'])):
        ranks = (data['items'][items]['rankUpDown'])
        if ranks[0] == '+':
            movie_rank_up_list.append(data['items'][items]['title'])
            movie_rank_up_list.append(ranks)

    print(movie_rank_up_list)


def get_movies_down():
    loc = f"https://imdb-api.com/en/API/MostPopularMovies/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    movie_rank_down_list = []
    for items in range(len(data['items'])):
        ranks = (data['items'][items]['rankUpDown'])
        if ranks[0] == '-':
            movie_rank_down_list.append(data['items'][items]['title'])
            movie_rank_down_list.append(ranks)
    print(movie_rank_down_list)


def get_tvs_up():
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/MostPopularTVs/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    tv_rank_up_list = []
    for items in range(len(data['items'])):
        ranks = (data['items'][items]['rankUpDown'])
        if ranks[0] == '+':
            tv_rank_up_list.append(data['items'][items]['title'])
            tv_rank_up_list.append(ranks)
    print(tv_rank_up_list)


def get_tvs_down():
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/MostPopularTVs/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    tv_rank_down_list = []
    for items in range(len(data['items'])):
        ranks = (data['items'][items]['rankUpDown'])
        if ranks[0] == '-':
            tv_rank_down_list.append(data['items'][items]['title'])
            tv_rank_down_list.append(ranks)
    print(tv_rank_down_list)


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_250_data(
    imdb_id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    fullTitle TEXT NOT NULL,
    year TEXT NOT NULL,
    crew TEXT NOT NULL,
    imDbRating TEXT NOT NULL,
    imDbRatingCount TEXT NOT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imdb_id TEXT NOT NULL,
    total_rating TEXT NOT NULL,
    total_rating_votes TEXT NOT NULL,
    rating_percent_10 TEXT NOT NULL,
    rating_votes_10 TEXT NOT NULL,
    rating_percent_9 TEXT NOT NULL,
    rating_votes_9 TEXT NOT NULL,
    rating_percent_8 TEXT NOT NULL,
    rating_votes_8 TEXT NOT NULL,
    rating_percent_7 TEXT NOT NULL,
    rating_votes_7 TEXT NOT NULL,
    rating_percent_6 TEXT NOT NULL,
    rating_votes_6 TEXT NOT NULL,
    rating_percent_5 TEXT NOT NULL,
    rating_votes_5 TEXT NOT NULL,
    rating_percent_4 TEXT NOT NULL,
    rating_votes_4 TEXT NOT NULL,
    rating_percent_3 TEXT NOT NULL,
    rating_votes_3 TEXT NOT NULL,
    rating_percent_2 TEXT NOT NULL,
    rating_votes_2 TEXT NOT NULL,
    rating_percent_1 TEXT NOT NULL,
    rating_votes_1 TEXT NOT NULL,
    FOREIGN KEY (imdb_id) REFERENCES top_250_data (imdb_id)
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_tvs(
        id TEXT NOT NULL PRIMARY KEY,
        rank TEXT NOT NULL,
        rankUpDown TEXT NOT NULL,
        title TEXT NOT NULL,
        fullTitle TEXT NOT NULL,
        year TEXT NOT NULL,
        crew TEXT NOT NULL,
        imDbRating TEXT NOT NULL,
        imDbRatingCount TEXT NOT NULL
        );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_250_movies(
        id TEXT NOT NULL PRIMARY KEY,
        rank TEXT NOT NULL,
        title TEXT NOT NULL,
        fullTitle TEXT NOT NULL,
        year TEXT NOT NULL,
        crew TEXT NOT NULL,
        imDbRating TEXT NOT NULL,
        imDbRatingCount TEXT NOT NULL
        );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS popular_movies(
            id TEXT NOT NULL PRIMARY KEY,
            rank TEXT NOT NULL,
            rankUpDown TEXT NOT NULL,
            title TEXT NOT NULL,
            fullTitle TEXT NOT NULL,
            year TEXT NOT NULL,
            crew TEXT NOT NULL,
            imDbRating TEXT NOT NULL,
            imDbRatingCount TEXT NOT NULL
            );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_ratings_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imdb_id TEXT NOT NULL,
        title TEXT NOT NULL,
        fullTitle TEXT NOT NULL,
        year TEXT NOT NULL,
        total_rating TEXT NOT NULL,
        total_rating_votes TEXT NOT NULL,
        rating_percent_10 TEXT NOT NULL,
        rating_votes_10 TEXT NOT NULL,
        rating_percent_9 TEXT NOT NULL,
        rating_votes_9 TEXT NOT NULL,
        rating_percent_8 TEXT NOT NULL,
        rating_votes_8 TEXT NOT NULL,
        rating_percent_7 TEXT NOT NULL,
        rating_votes_7 TEXT NOT NULL,
        rating_percent_6 TEXT NOT NULL,
        rating_votes_6 TEXT NOT NULL,
        rating_percent_5 TEXT NOT NULL,
        rating_votes_5 TEXT NOT NULL,
        rating_percent_4 TEXT NOT NULL,
        rating_votes_4 TEXT NOT NULL,
        rating_percent_3 TEXT NOT NULL,
        rating_votes_3 TEXT NOT NULL,
        rating_percent_2 TEXT NOT NULL,
        rating_votes_2 TEXT NOT NULL,
        rating_percent_1 TEXT NOT NULL,
        rating_votes_1 TEXT NOT NULL
        );''')


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.display_window = None
        conn, cursor = open_db("sprint2_db.sqlite")
        self.title = QLabel(self)
        self.update_info_button = QPushButton(self)
        self.display_button = QPushButton(self)
        self.sql_cursor = cursor
        self.sql_conn = conn
        setup_db(self.sql_cursor)
        self.setup_ui()

    def setup_ui(self):
        # Window
        self.resize(600, 500)
        window_width = int(self.frameGeometry().width())
        self.setWindowTitle("Main Window")

        # Title
        self.title.setText("Choose an option")
        self.title.setFont(QFont('Georgia', 16, QFont.Bold))
        self.title.adjustSize()
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(int((window_width - self.title.width()) / 2), 100)

        # Update Button
        self.update_info_button.resize(100, 50)
        self.update_info_button.move(250, 300)
        self.update_info_button.setText('Update')

        # Display Button
        self.display_button.resize(100, 50)
        self.display_button.move(355, 300)
        self.display_button.setText('Display')

        # Signals/Slots
        self.update_info_button.clicked.connect(self.update_button_clicked)
        self.display_button.clicked.connect(self.display_button_clicked)

        self.show()

    def update_button_clicked(self):
        print('updated!')
        id_num_list = ['tt7462410', 'tt5491994', 'tt0081834', 'tt0096697', 'tt1492966']
        rank_change_list = ['tt8851148', 'tt10733228', 'tt10298810', 'tt10023022']

        add_show_data_to_db(self.sql_cursor, self.sql_conn)
        get_top250_movies(self.sql_cursor, self.sql_conn)
        get_top_tvs(self.sql_cursor, self.sql_conn)
        get_popular_movies(self.sql_cursor, self.sql_conn)

        for i in range(len(id_num_list)):
            add_rating_data_to_db(self.sql_cursor, id_num_list[i], self.sql_conn)
        for i in range(len(rank_change_list)):
            get_movie_rating_data(self.sql_cursor, rank_change_list[i], self.sql_conn)

        close_db(self.sql_conn)
        self.close()

    def display_button_clicked(self):
        print('Displayed!')
        self.display_window = DisplayWindow()
        self.display_window.show()
        self.close()


class DisplayWindow(QWidget):
    def __init__(self):
        super(DisplayWindow, self).__init__()
        self.movie_info_window = None
        self.show_info_window = None
        self.title = QLabel(self)
        self.movie_info_button = QPushButton(self)
        self.show_info_button = QPushButton(self)
        self.setup_ui()

    def setup_ui(self):
        # Window
        self.resize(600, 500)
        window_width = int(self.frameGeometry().width())
        self.setWindowTitle("Display Window")

        # Title
        self.title.setText("Choose an option")
        self.title.setFont(QFont('Georgia', 16, QFont.Bold))
        self.title.adjustSize()
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(int((window_width - self.title.width()) / 2), 100)

        # Movies Button
        self.movie_info_button.resize(100, 50)
        self.movie_info_button.move(250, 300)
        self.movie_info_button.setText('Movies')

        # Shows Button
        self.show_info_button.resize(100, 50)
        self.show_info_button.move(355, 300)
        self.show_info_button.setText('Shows')

        # Signals/Slots
        self.movie_info_button.clicked.connect(self.movie_info_button_clicked)
        self.show_info_button.clicked.connect(self.show_info_button_clicked)

    def show_info_button_clicked(self):
        print('Displayed!')
        self.show_info_window = DisplayShowWindow()
        self.show_info_window.show()
        self.close()

    def movie_info_button_clicked(self):
        print('Displayed!')
        self.movie_info_window = DisplayMovieWindow()
        self.movie_info_window.show()
        self.close()


class DisplayShowWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(DisplayShowWindow, self).__init__()
        self.title = QLabel(self)
        self.shows_up_button = QPushButton(self)
        self.shows_down_button = QPushButton(self)
        self.setup_ui()

    def setup_ui(self):
        # Window
        self.resize(600, 500)
        window_width = int(self.frameGeometry().width())
        self.setWindowTitle("Display Show Window")

        # Title
        self.title.setText("Choose an option")
        self.title.setFont(QFont('Georgia', 16, QFont.Bold))
        self.title.adjustSize()
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(int((window_width - self.title.width()) / 2), 100)

        # Shows up Button
        self.shows_up_button.resize(100, 50)
        self.shows_up_button.move(250, 300)
        self.shows_up_button.setText('Shows Up')

        # Shows down Button
        self.shows_down_button.resize(100, 50)
        self.shows_down_button.move(355, 300)
        self.shows_down_button.setText('Shows Down')

        # Signals/Slots
        self.shows_up_button.clicked.connect(self.shows_up_button_clicked)
        self.shows_down_button.clicked.connect(self.shows_down_button_clicked)

    def shows_up_button_clicked(self):
        print('Displayed the shows trending up!')
        get_tvs_up()
        self.close()

    def shows_down_button_clicked(self):
        print('Displayed the shows trending down!')
        get_tvs_down()
        self.close()


class DisplayMovieWindow(QWidget):
    def __init__(self):
        super(DisplayMovieWindow, self).__init__()
        self.title = QLabel(self)
        self.movies_up_button = QPushButton(self)
        self.movies_down_button = QPushButton(self)
        self.setup_ui()

    def setup_ui(self):
        # Window
        self.resize(600, 500)
        window_width = int(self.frameGeometry().width())
        self.setWindowTitle("Display Movie Window")

        # Title
        self.title.setText("Choose an option")
        self.title.setFont(QFont('Georgia', 16, QFont.Bold))
        self.title.adjustSize()
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(int((window_width - self.title.width()) / 2), 100)

        # Shows up Button
        self.movies_up_button.resize(100, 50)
        self.movies_up_button.move(250, 300)
        self.movies_up_button.setText('Movies Up')

        # Shows down Button
        self.movies_down_button.resize(100, 50)
        self.movies_down_button.move(355, 300)
        self.movies_down_button.setText('Movies Down')

        # Signals/Slots
        self.movies_up_button.clicked.connect(self.movies_up_button_clicked)
        self.movies_down_button.clicked.connect(self.movies_down_button_clicked)

    def movies_up_button_clicked(self):
        print('Displayed the movies trending up!')
        get_movies_up()
        self.close()

    def movies_down_button_clicked(self):
        print('Displayed the movies trending down!')
        get_movies_down()
        self.close()


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
