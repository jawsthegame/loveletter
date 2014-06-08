import random

from card import *
from player import Player
from utils import Utils


class Game(object):
  def __init__(self):
    self.deck = []
    self.players = []

    num_players = int(Utils.read('Number of players? '))
    for i in range(num_players):
      name = Utils.read('Player %d name? ' % (i+1))
      self.players.append(Player(name, self))

    self.make_deck()

  def make_deck(self):
    self.deck = [
      Guard(), Guard(), Guard(), Guard(), Guard(),
      Priest(), Priest(),
      Baron(), Baron(),
      Handmaid(), Handmaid(),
      Prince(), Prince(),
      King(),
      Countess(),
      Princess(),
    ]
    random.shuffle(self.deck)

  def next_round(self):
    self.make_deck()
    for player in self.players:
      player.active = True

  def draw(self):
    return self.deck.pop()

  def start(self):
    while not self.game_over():
      self._initial_deal()
      round_over = False
      while not round_over:
        for player in self.players:
          active_players = [p for p in self.players if p.active]
          if len(active_players) == 1:
            # ROUND END
            round_over = True
            Utils.write('ROUND OVER: %s wins!' % active_players[0].name)
            active_players[0].wins += 1
            break
          player.turn()
      self.next_round()

  def game_over(self):
    return False

  def _initial_deal(self):
    if len(self.players) > 2:
      self.draw()
    elif len(self.players) == 2:
      for i in range(3):
        self.draw()

    for player in self.players:
      player.draw()


if __name__ == '__main__':
  game = Game()
  game.start()
