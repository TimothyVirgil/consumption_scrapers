import requests
from bs4 import BeautifulSoup
import time


def scrape_backloggd(username: str) -> dict:
    '''Returns a dictionary like so:

    game: rating

    for all the games a given user has rated on backloggd.

    I only intend to use this for my own username.'''

    a = 1
    url = f'https://www.backloggd.com/u/{username}/games?page={a}'
    curr_game = 'mario'
    last_game = 'luigi'
    game_dict = {}

    while True:
        url = f'https://www.backloggd.com/u/{username}/games?page={a}'
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.find_all(class_='card mx-auto game-cover user-rating')
        curr_game = elements[0].text

        if a == 40:
            print(a)
            break

        if curr_game == last_game:
            break

        else:
            for elem in elements:
                game = elem.find(class_='game-text-centered').text.strip()
                rating = int(elem['data-rating'])
                game_dict[game] = rating

            if a % 5 == 0:
                print('Waiting 5 seconds to ping server')
                # be chill with the scraping
                time.sleep(5)
                a += 1

            else:
                a += 1

            last_game = curr_game

    return game_dict
