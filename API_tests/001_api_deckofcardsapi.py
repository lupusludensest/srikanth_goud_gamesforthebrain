from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests

driver = webdriver.Chrome()
driver.maximize_window()
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Explicit wait
wait = WebDriverWait(driver, 15)

# 1. Open the url
driver.get('https://deckofcardsapi.com/')
# 1.1. Make a screenshot if 'options.headless = True' it fits the screen
# driver.get_screenshot_as_file('site_is_up.png')
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))
driver.find_element(By.TAG_NAME, 'body').screenshot('site_is_up.png')
# 1.2. Verify the url 'https://deckofcardsapi.com/' is here
expected_url = 'https://deckofcardsapi.com/'
actual_url = driver.current_url
if expected_url in actual_url:
    print(f'Valid. Expected == Actual\n')
else:
    print(f'Alert. Expected != Actual\n')

# 3. Shuffle the deck
r=requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
print(f'\nShuffle the deck')
if r.status_code == 200:
    print(f'"success": true')
deck_id = r.json()["deck_id"]
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"shuffled": {(r.json()["shuffled"])}')
print(f'"remaining": {r.json()["remaining"]}')

# 4. Method draw a cards
def draw_cards_for_players(deck_id):
    r = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=3")
    print(f'Deal three cards to each of two players')
    if r.status_code == 200:
        print(f'"success": true')
    print(f'"deck_id": "{deck_id}"')
    print(f'"cards": {(r.json()["cards"])}')
    print(f'"remaining": {r.json()["remaining"]}\n')
    return r.json()["cards"]

# 5. Method calculate score for players
def calculate_score_for_players(array_of_cards, total):
    if len(array_of_cards[0]["value"]) < 3:
        total.append(int(array_of_cards[0]["value"]))
    elif type(array_of_cards[0]["value"]) != int:
        if array_of_cards[0]["value"] == 'JACK' or array_of_cards[0]["value"] == 'QUEEN' or array_of_cards[0]["value"] == 'KING':
            total.append(10)
        elif array_of_cards[0]["value"] == 'ACE':
            total.append(11)

    if len(array_of_cards[1]["value"]) < 3:
        total.append(int(array_of_cards[1]["value"]))
    elif type(array_of_cards[1]["value"]) != int:
        if array_of_cards[1]["value"] == 'JACK' or array_of_cards[1]["value"] == 'QUEEN' or array_of_cards[1]["value"] == 'KING':
            total.append(10)
        elif array_of_cards[1]["value"] == 'ACE':
            total.append(11)

    if len(array_of_cards[2]["value"]) < 3:
        total.append(int(array_of_cards[2]["value"]))
    elif type(array_of_cards[2]["value"]) != int:
        if array_of_cards[2]["value"] == 'JACK' or array_of_cards[2]["value"] == 'QUEEN' or array_of_cards[2]["value"] == 'KING':
            total.append(10)
        elif array_of_cards[2]["value"] == 'ACE':
            total.append(11)
    print(f'{total}: total_1 = {sum(total)}')

# 6. Deal three cards to each of two players
# 6.1. To player 1
print(f'\nTo player 1')
# 6.2. Count the score of player 1
array_of_cards = draw_cards_for_players(deck_id)
print(f'1th player.\n1th card: "{array_of_cards[0]["value"]}";\n2d card: "{array_of_cards[1]["value"]}";\n3d card: "{array_of_cards[2]["value"]}"')
total_1 = []
calculate_score_for_players(array_of_cards, total_1)

# 6.3. To player 2
print(f'\nTo player 2')
# 6.4. Count the score of player 1
array_of_cards = draw_cards_for_players(deck_id)
print(f'2d player.\n1th card: "{array_of_cards[0]["value"]}";\n2d card: "{array_of_cards[1]["value"]}";\n3d card: "{array_of_cards[2]["value"]}"')
total_2 = []
calculate_score_for_players(array_of_cards, total_2)

# 7. Check whether either has a blackjack
# https://ru.wikihow.com/%D0%B8%D0%B3%D1%80%D0%B0%D1%82%D1%8C-%D0%B2-%D0%B1%D0%BB%D1%8D%D0%BA%D0%B4%D0%B6%D0%B5%D0%BA
# Карты с числом: цена — число на карте.
# Картинки: цена всех — 10.
# Туз: 1 или 11. Обычно считается за 11, но если при таком подсчете сумма очков в вашей руке превышает 21, то туз считается за 1.
# Таким образом туз и картинка составляют 21 очка в две карты — это и есть блэкджек.
if (total_1[0] + total_1[1] + total_1[2]) == 21 or (total_1[0] + total_1[1]) == 21:
    print(f'\n1th player has a blackjack')

if (total_2[0] + total_2[1] + total_2[2]) == 21 or (total_2[0] + total_2[1]) == 21:
    print(f'\n2d player has a blackjack')





