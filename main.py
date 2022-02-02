import secrets
import requests
import json
import imdb

file1 = open('output.txt', 'w')


def main():
    id_num_list = ['tt7462410', 'tt5491994', 'tt0081834', 'tt0096697', 'tt2100976']
    for i in range(len(id_num_list)):
        print_show_data(id_num_list[i])
        file1.write('\n')


def print_show_data(id_num: str):
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
                    file1.writelines('\t' + rating_key + ' : ' + rating_value)
                file1.write('\n')
        else:
            file1.writelines(f'{key} : {value}')
            file1.write('\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# ia = imdb.IMDb()
# search = ia.get_top250_tv()
#
#
# for i in range(250):
#     for key, value in search[i].items()[0:6]:
#         print(key, value)
#     print()


