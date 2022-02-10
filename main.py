import secrets
import requests
import imdb
import sqlite3
from typing import Tuple


# open text file
file1 = open('output.txt', 'w')

imdb_id = ''
imdb_id_list = []


def main():
    # create list of Ids
    id_num_list = ['tt7462410', 'tt5491994', 'tt0081834', 'tt0096697']
    # # loop through list and write data for each show Id to output file
    for i in range(len(id_num_list)):
        print_show_data(id_num_list[i])
        file1.write('\n')

    # function call for getting top 250 show data
    get_top250_data()
    conn, cursor = open_db("sprint2_db.sqlite")
    setup_db(cursor)

    add_show_data_to_db(cursor)
    for i in range(len(id_num_list)):
        add_rating_data_to_db(cursor, id_num_list[i])

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


def add_rating_data_to_db(cursor: sqlite3.Cursor, id_num: str):
    # use secret key to get show ratings data
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{id_num}"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()

    cursor.execute(f'''INSERT INTO ratings_data (total_rating, total_rating_votes, rating_percent_10, 
    rating_votes_10, rating_percent_9, rating_votes_9, rating_percent_8, rating_votes_8, rating_percent_7, 
    rating_votes_7, rating_percent_6, rating_votes_6, rating_percent_5, rating_votes_5, rating_percent_4, 
    rating_votes_4, rating_percent_3, rating_votes_3, rating_percent_2, rating_votes_2, rating_percent_1, 
    rating_votes_1) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                   (data['totalRating'], data['totalRatingVotes'],
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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


# def make_initial_top250(cursor: sqlite3.Cursor):
#     cursor.execute(f'''INSERT INTO top_250_data (show_id, title, full_title, year, crew, imdb_rating, imdb_rating_count)
#                    VALUES (1004, "the show", "the 250 show", 200.98, "10 people", 7, 2987.5)''')


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
