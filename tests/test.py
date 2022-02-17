import main


# test to get 250 tv shows
def test_get_top250_tv():
    data = main.get_top250_data()
    assert len(data['items']) == 250
