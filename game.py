import random

from card import *
from player import Player
from utils import Utils


class Game(object):
  def __init__(self):
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

    self.players = []

    random.shuffle(self.deck)

    num_players = int(Utils.read('Number of players?'))
    for i in range(num_players):
      name = Utils.read('Player %d name? ' % (i+1))
      self.players.append(Player(name, self))

  def draw(self):
    return self.deck.pop()

  def start(self):
    self._initial_discard()

    for player in self.players:
      active_players = len([p for p in self.players if p.active])
      if active_players == 1:
        # ROUND END
        break
      player.turn()

  def _initial_discard(self):
    if len(self.players) > 2:
      self.draw()
    elif len(self.players) == 2:
      for i in range(3):
        self.draw()


if __name__ == '__main__':
  game = Game()
  game.start()
