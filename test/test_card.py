from mock import MagicMock as Mock
from unittest import TestCase

from card import Baron
from card import Countess
from card import Guard
from card import Handmaid
from card import King
from card import Priest
from card import Prince
from card import Princess
from player import Player
from utils import Utils


class TestCard(TestCase):

  def setUp(self):
    Utils.read  = Mock()
    Utils.write = Mock()
    self.game = Mock()

  def _new_player(self, name):
    return Player(name, self.game)

  def test_guard(self):
    g = Guard()
    other1 = self._new_player('Jimbo')
    other1.hand = [Baron()]
    other2 = self._new_player('Janet')
    other2.hand = [Priest()]

    # RETURN VALUES (in reverse order)
      # 0 - Priest
      # 0 - Jimbo
      # 0 - Priest
      # 1 - Janet

    return_values = [1, 0, 0, 0]
    Utils.read.side_effect = lambda x: return_values.pop()

    g.effect(None, [other1, other2])
    self.assertTrue(other1.active)

    g.effect(None, [other1, other2])
    self.assertFalse(other2.active)

  def test_priest(self):
    pr = Priest()
    other = self._new_player('Jimbo')
    other.hand = [Guard()]

    Utils.read.return_value = 0
    pr.effect(None, [other])
    Utils.write.assert_called_with('1: Guard')

  def test_baron(self):
    b = Baron()
    other1 = self._new_player('Jimbo')
    other1.hand = [Guard()]
    other2 = self._new_player('Janet')
    other2.hand = [Handmaid()]
    other3 = self._new_player('Jill')
    other3.hand = [Priest()]
    me = self._new_player('Alice')
    me.hand = [Priest()]

    return_values = [2, 1, 0]
    Utils.read.side_effect = lambda x: return_values.pop()

    b.effect(me, [other1, other2, other3])
    self.assertFalse(other1.active)

    b.effect(me, [other1, other2, other3])
    self.assertFalse(me.active)

    b.effect(me, [other1, other2, other3])
    self.assertTrue(other3.active)

  def test_handmaid(self):
    h = Handmaid()
    me = self._new_player('Alice')

    self.assertFalse(me.immune)
    h.effect(me, [])
    self.assertTrue(me.immune)

  def test_prince(self):
    prn = Prince()
    other = self._new_player('Jimbo')
    other.hand = [Guard()]
    me = self._new_player('Alice')
    me.hand = [Priest()]

    Utils.read.return_value = 1
    self.game.draw.return_value = Baron()

    prn.effect(me, [other])
    self.assertEquals(1, len(other.hand))
    self.assertIsInstance(other.hand[0], Baron)

  def test_king(self):
    k = King()
    other = self._new_player('Jimbo')
    other.hand = [Guard()]
    me = self._new_player('Alice')
    me.hand = [Handmaid()]

    Utils.read.return_value = 0

    k.effect(me, [other])
    self.assertIsInstance(other.hand[0], Handmaid)
    self.assertIsInstance(me.hand[0], Guard)

  def test_countess(self):
    c = Countess()
    me = self._new_player('Alice')

    me.hand = [c]
    c.draw_effect(me, Prince())
    self.assertEquals(0, len(me.hand))

    me.hand = [c]
    c.draw_effect(me, King())
    self.assertEquals(0, len(me.hand))

    me.hand = [c]
    c.draw_effect(me, Baron())
    self.assertEquals(1, len(me.hand))

  def test_princess(self):
    prns = Princess()
    me = self._new_player('Alice')

    prns.discard_effect(me)
    self.assertFalse(me.active)
