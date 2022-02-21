# from sqlalchemy.engine import cursor

import main


# test to get 250 tv shows
def test_get_top250_tv():
    data = main.get_top250_data()
    assert len(data['items']) == 250


# def test_new_table():
#     main.setup_db(cursor)
#     table_exists = cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table'
#     AND name='top_250_movies' ''')
#     assert table_exists == True
#
#
# def test_write_to_table():
#     main.get_top250_movies(cursor)
