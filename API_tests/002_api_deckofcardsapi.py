import requests

# Define Constants
NUMBER_OF_CARDS = int(input('ENTER NUMBER OF CARDS: '))
NUMBER_OF_PLAYERS = int(input('ENTER NUMBER OF PLAYERS: '))
NUMBER_OF_DECKS = int(input('ENTER NUMBER OF DECKS: '))
CARDS_VALUE_10 = ['JACK', 'QUEEN', 'KING']

# Define class for scores
class scores_dictionary(dict):
    # __init__ function
    def __init__(self):
        self = dict()
    # Function to add key:value
    def add(self, key, value):
        self[key] = value

# Init scores
scores = scores_dictionary()

# 3. Shuffle the deck
r=requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=' + str(NUMBER_OF_DECKS))
print(f'\nShuffle the deck')
if r.status_code == 200:
    print(f'"success": true')
deck_id = r.json()["deck_id"]
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"shuffled": {(r.json()["shuffled"])}')
print(f'"remaining": {r.json()["remaining"]}')

# 4. Method draw a cards
def draw_cards_for_players(deck_id):
    r = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" + str(NUMBER_OF_CARDS))
    if r.status_code == 200:
        print(f'"success": true')
    print(f'"deck_id": "{deck_id}"')
    print(f'"cards": {(r.json()["cards"])}')
    print(f'"remaining": {r.json()["remaining"]}\n')
    return r.json()["cards"]

# 5. Method calculate score for players
def calculate_score_for_players(array_of_cards):
        total = 0
        aces = []
        for card in array_of_cards:
            if card["value"] == 'ACE':
                    aces.append(card)
            elif card["value"] in CARDS_VALUE_10:
                    total += 10
            else: total += int(card["value"])
        for ace in aces:
              if total >= 20: total += 1
              else: total += 11
        return total
# 6. Deal three cards to each player
print(f'\nDeal ' + str(NUMBER_OF_CARDS) + ' cards to each of ' + str(NUMBER_OF_PLAYERS) + ' player(s)')

for x in range(NUMBER_OF_PLAYERS):
     print(f'\nTo Player Number ' + str(x+1) + ':')
     array_of_cards = draw_cards_for_players(deck_id)
     for index, card in enumerate(array_of_cards, start=1):
          print(f'\nCard Number ' + str(index) + ': ' + card["value"])
     scores.add('Player ' + str(x+1), calculate_score_for_players(array_of_cards))

# 7. Check whether either has a blackjack
# https://ru.wikihow.com/%D0%B8%D0%B3%D1%80%D0%B0%D1%82%D1%8C-%D0%B2-%D0%B1%D0%BB%D1%8D%D0%BA%D0%B4%D0%B6%D0%B5%D0%BA
# Карты с числом: цена — число на карте.
# Картинки: цена всех — 10.
# Туз: 1 или 11. Обычно считается за 11, но если при таком подсчете сумма очков в вашей руке превышает 21,
# то туз считается за 1.
# Таким образом туз и картинка составляют 21 очка в две карты — это и есть блэкджек.

print(f'\nChecking if somebody has a Black Jack...')
for score in scores:
     if scores[score] == 21:
        print(f'\n' + str(score) + ' has Black Jack')
     else:  print(f'\n' + str(score) + ': ' + str(scores[score]))
