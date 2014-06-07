from abc import ABCMeta
from abc import abstractmethod

from utils import Utils


CARD_TYPES = [
  (1, 'Guard'),
  (2, 'Priest'),
  (3, 'Baron'),
  (4, 'Handmaid'),
  (5, 'Prince'),
  (6, 'King'),
  (7, 'Countess'),
  (8, 'Princess')
]


class Card(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def effect(self, player, others):
    return NotImplemented

  @abstractmethod
  def draw_effect(self, player, card):
    return NotImplemented

  def pick_player(self, others):
    for i, player in enumerate(others):
      Utils.write('%d: %s' % (i, player.name))
    pick = int(Utils.read('Which Player? '))
    return others[pick]

  def assert_hand(self, player):
    assert len(player.hand) is 1


class Guard(Card):
  type_ = CARD_TYPES[0]

  def effect(self, player, others):
    for i, t in enumerate(CARD_TYPES[1:]):
      _, name = t
      Utils.write('%d: %s' % (i, name))

    pick = int(Utils.read('Card Type? '))
    card_type = CARD_TYPES[pick+1]

    other = self.pick_player(others)
    self.assert_hand(other)
    if other.hand[0].type_ == card_type:
      Utils.write('MATCH! %s is out of the round.' % other.name)
      other.active = False

  def draw_effect(self, player, card):
    pass


class Priest(Card):
  type_ = CARD_TYPES[1]

  def effect(self, player, others):
    other = self.pick_player(others)
    for card in other.hand:
      Utils.write('%d: %s' % card.type_)

  def draw_effect(self, player, card):
    pass


class Baron(Card):
  type_ = CARD_TYPES[2]

  def effect(self, player, others):
    other = self.pick_player(others)
    self.assert_hand(player)
    self.assert_hand(other)

    val, _        = player.hand[0].type_
    other_val, _  = other.hand[0].type_

    if val > other_val:
      other.active = False
    elif val < other_val:
      player.active = False
    else:
      Utils.write('Tie!')

  def draw_effect(self, player, card):
    pass


class Handmaid(Card):
  type_ = CARD_TYPES[3]

  def effect(self, player, others):
    player.immune = True

  def draw_effect(self, player, card):
    pass


class Prince(Card):
  type_ = CARD_TYPES[4]

  def effect(self, player, others):
    other = self.pick_player([player] + others)
    other.discard_all()
    other.draw()

  def draw_effect(self, player, card):
    pass


class King(Card):
  type_ = CARD_TYPES[5]

  def effect(self, player, others):
    other = self.pick_player(others)
    tmp = other.hand
    other.hand = player.hand
    player.hand = tmp

  def draw_effect(self, player, card):
    pass


class Countess(Card):
  type_ = CARD_TYPES[6]

  def effect(self, player, others):
    pass

  def draw_effect(self, player, card):
    if isinstance(card, Prince) or isinstance(card, King):
      player.hand.remove(self)
