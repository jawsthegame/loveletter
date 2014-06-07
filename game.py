from card import Guard
from utils import Utils

class Game(object):
  def __init__(self):
    self.deck = [
      Guard(), Guard(), Guard(), Guard(), Guard(),
      Priest(), Priest(),
      Baron(), Baron(),
      Handmaid(), Handmaid(),
    ]

    random.shuffle(self.deck)

    num_players = Utils.read('Number of players?')

  def draw(self):
    return self.deck.pop()
