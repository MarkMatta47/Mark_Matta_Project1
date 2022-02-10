import secrets
import requests
import imdb
import sqlite3
from typing import Tuple


# open text file
file1 = open('output.txt', 'w')

show_id = 0
title = ''
full_title = ''
year = ''
crew = ''
imdb_rating = ''
imdb_rating_count = ''

imdb_id = ''
imdb_id_list = []


def main():
    # create list of Ids
    id_num_list = ['tt7462410', 'tt5491994', 'tt0081834', 'tt0096697', 'tt2100976']
    # # loop through list and write data for each show Id to output file
    # for i in range(len(id_num_list)):
    #     print_show_data(id_num_list[i])
    #     file1.write('\n')

    for i in range(len(id_num_list)):
        add_rating_data_to_db(id_num_list[i])

    # function call for getting top 250 show data
    get_top250_data()
    conn, cursor = open_db("sprint2_db.sqlite")
    setup_db(cursor)
    # make_initial_top250(cursor)
    add_show_data_to_db(cursor)

    print(type(conn))
    close_db(conn)


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


def add_show_data_to_db(cursor: sqlite3.Cursor):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}/"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    count = 1
    # loop through list of dictionaries assigned to "items" key
    for entry in data["items"]:

        cursor.execute(f'''INSERT INTO top_250_data (id, title, fullTitle, year, crew, imDbRating, 
                               imDbRatingCount) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (count, entry['title'], entry['fullTitle'], entry['year'], entry['crew'], entry['imDbRating'],
                        entry['imDbRatingCount']))
        count += 1


def add_rating_data_to_db(id_num: str):
    rating_percent_10 = ''
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{id_num}"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    for key, value in data.items():
        if key == 'ratings':
            for i in range(len(data['ratings'])):
                for rating_key, rating_value in data['ratings'][i].items():
                    if rating_key == 'percent':
                        rating_percent_10 = value
            print(rating_percent_10)



def get_top250_data():
    ia = imdb.IMDb()
    search = ia.get_top250_tv()

    # loop through top 250 shows and write them to output file
    for i in range(250):
        for key, value in search[i].items()[0:6]:
            file1.write(f'{key} : {value}')
            file1.write('\n')
        file1.write('\n')


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_250_data(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    fullTitle TEXT NOT NULL,
    year TEXT NOT NULL,
    crew TEXT NOT NULL,
    imDbRating TEXT NOT NULL,
    imDbRatingCount TEXT NOT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings_data(
    imdb_id INTEGER PRIMARY KEY,
    total_rating INTEGER NOT NULL,
    total_rating_votes INTEGER NOT NULL,
    rating_percent_10 INTEGER NOT NULL,
    rating_votes_10 INTEGER NOT NULL,
    rating_percent_9 INTEGER NOT NULL,
    rating_votes_9 INTEGER NOT NULL,
    rating_percent_8 INTEGER NOT NULL,
    rating_votes_8 INTEGER NOT NULL,
    rating_percent_7 INTEGER NOT NULL,
    rating_votes_7 INTEGER NOT NULL,
    rating_percent_6 INTEGER NOT NULL,
    rating_votes_6 INTEGER NOT NULL,
    rating_percent_5 INTEGER NOT NULL,
    rating_votes_5 INTEGER NOT NULL,
    rating_percent_4 INTEGER NOT NULL,
    rating_votes_4 INTEGER NOT NULL,
    rating_percent_3 INTEGER NOT NULL,
    rating_votes_3 INTEGER NOT NULL,
    rating_percent_2 INTEGER NOT NULL,
    rating_votes_2 INTEGER NOT NULL,
    rating_percent_1 INTEGER NOT NULL,
    rating_votes_1 INTEGER NOT NULL
    );''')


# def make_initial_top250(cursor: sqlite3.Cursor):
#     cursor.execute(f'''INSERT INTO top_250_data (show_id, title, full_title, year, crew, imdb_rating, imdb_rating_count)
#                    VALUES (1004, "the show", "the 250 show", 200.98, "10 people", 7, 2987.5)''')


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
