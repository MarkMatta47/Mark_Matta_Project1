import main


# test to get 250 tv shows
def test_get_top250_tv():
    search = main.get_top250_data()
    assert len(search) == 250
