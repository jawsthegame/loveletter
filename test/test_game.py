from mock import MagicMock as Mock
from unittest import TestCase

from game import Game
from utils import Utils


class TestGame(TestCase):

  def setUp(self):
    Utils.read = Mock()
    Utils.write = Mock()

  def test_init(self):
    game = self._game()
    self.assertEquals(2, len(game.players))
    self.assertEquals('Alice', game.players[0].name)
    self.assertEquals('Jimbo', game.players[1].name)

  def test_initial_discard(self):
    game = self._game()
    self.assertEquals(16, len(game.deck))
    game._initial_discard()
    self.assertEquals(13, len(game.deck))

  def _game(self):
    return_values = ['Jimbo', 'Alice', 2]
    Utils.read.side_effect = lambda x: return_values.pop()
    return Game()
