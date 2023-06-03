from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import requests

driver = webdriver.Chrome()
driver.maximize_window()
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Locators
B_THREE = (By.XPATH, "//img[@name='space62']")
C_FOUR_1 = (By.XPATH, "//img[@name='space53']")
C_FOUR_2 = (By.XPATH, "//img[@onclick='didClick(5, 3)']")
MAKE_A_MOVE = EC.visibility_of_element_located((By.XPATH, "//p[@id='message']"))
D_FIVE = (By.XPATH, "//img[@name='space44']")

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
    print(f'Expected "{expected_url}", and got: "{actual_url}"\n')
else:
    print(f'Expected "{expected_url}", but got: "{actual_url}"\n')

# 2. Get a new deck
r=requests.get('https://deckofcardsapi.com/api/deck/new/')
print(f'Get a new deck')
if 300 >= r.status_code >= 200:
    print(f'"success": true')
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"shuffled": {(r.json()["shuffled"])}')
print(f'"remaining": {r.json()["remaining"]}')

# 3. Shuffle the deck
r=requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
print(f'\nShuffle the deck')
if 300 >= r.status_code >= 200:
    print(f'"success": true')
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"shuffled": {(r.json()["shuffled"])}')
print(f'"remaining": {r.json()["remaining"]}')

# 4. Deal three cards to each of two players
# 4.1. To player 1
r=requests.get('https://deckofcardsapi.com/api/deck/new/draw/?count=3')
print(f'\nDeal three cards to each of two players')
print(f'To player 1')
if 300 >= r.status_code >= 200:
    print(f'"success": true')
deck_id = r.json()["deck_id"]
print(f'"deck_id": "{deck_id}"')
print(f'"cards": {(r.json()["cards"])}')
print(f'"remaining": {r.json()["remaining"]}\n')
# 4.2. Count the score of player 1
pics_score = r.json()["cards"]
print(f'1th player.\n1th card: "{pics_score[0]["value"]}";\n2d card: "{pics_score[1]["value"]}";\n3d card: "{pics_score[2]["value"]}"')
total_1 = []
if len(pics_score[0]["value"]) < 3:
    total_1.append(int(pics_score[0]["value"]))
elif type(pics_score[0]["value"]) != int:
    if pics_score[0]["value"] == 'JACK' or pics_score[0]["value"] == 'QUEEN' or pics_score[0]["value"] == 'KING':
        total_1.append(10)
    elif pics_score[0]["value"] == 'ACE':
        total_1.append(11)

if len(pics_score[1]["value"]) < 3:
    total_1.append(int(pics_score[1]["value"]))
elif type(pics_score[1]["value"]) != int:
    if pics_score[1]["value"] == 'JACK' or pics_score[1]["value"] == 'QUEEN' or pics_score[1]["value"] == 'KING':
        total_1.append(10)
    elif pics_score[1]["value"] == 'ACE':
        total_1.append(11)

if len(pics_score[2]["value"]) < 3:
    total_1.append(int(pics_score[2]["value"]))
elif type(pics_score[2]["value"]) != int:
    if pics_score[2]["value"] == 'JACK' or pics_score[2]["value"] == 'QUEEN' or pics_score[2]["value"] == 'KING':
        total_1.append(10)
    elif pics_score[2]["value"] == 'ACE':
        total_1.append(11)
print(f'{total_1}: total_1 = {sum(total_1)}')

# 4.3. To player 2
print(f'\nTo player 2')
message = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=3"
r=requests.get(message, params=deck_id)
if 300 >= r.status_code >= 200:
    print(f'"success": true')
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"cards": {(r.json()["cards"])}')
print(f'"remaining": {r.json()["remaining"]}')
# 4.2. Count the score of player 1
pics_score = r.json()["cards"]
print(f'\n2d player.\n1th card: "{pics_score[0]["value"]}";\n2d card: "{pics_score[1]["value"]}";\n3d card: "{pics_score[2]["value"]}"')
total_2 = []
if len(pics_score[0]["value"]) < 3:
    total_2.append(int(pics_score[0]["value"]))
elif type(pics_score[0]["value"]) != int:
    if pics_score[0]["value"] == 'JACK' or pics_score[0]["value"] == 'QUEEN' or pics_score[0]["value"] == 'KING':
        total_2.append(10)
    elif pics_score[0]["value"] == 'ACE':
        total_2.append(11)

if len(pics_score[1]["value"]) < 3:
    total_2.append(int(pics_score[1]["value"]))
elif type(pics_score[1]["value"]) != int:
    if pics_score[1]["value"] == 'JACK' or pics_score[1]["value"] == 'QUEEN' or pics_score[1]["value"] == 'KING':
        total_2.append(10)
    elif pics_score[1]["value"] == 'ACE':
        total_2.append(11)

if len(pics_score[2]["value"]) < 3:
    total_2.append(int(pics_score[2]["value"]))
elif type(pics_score[2]["value"]) != int:
    if pics_score[2]["value"] == 'JACK' or pics_score[2]["value"] == 'QUEEN' or pics_score[2]["value"] == 'KING':
        total_2.append(10)
    elif pics_score[2]["value"] == 'ACE':
        total_2.append(11)
print(f'{total_2}: total_2 = {sum(total_2)}')

# 5. Check whether either has a blackjack
if total_1[0] + total_1[1] == 21:
    print(f'\n1th player has a blackjack')

if total_2[0] + total_2[1] == 21:
    print(f'\n2d player has a blackjack')

