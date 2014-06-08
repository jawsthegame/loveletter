from utils import Utils


class Player(object):
  def __init__(self, name, game):
    self.name = name
    self.game = game
    self.hand = []
    self.played = []
    self.wins = 0
    self.active = True
    self.immune = False

  def draw(self):
    self.hand.append(self.game.draw())
    if len(self.hand) is 2:
      self.print_hand()
      self.hand[0].draw_effect(self, self.hand[1])

  def play(self):
    if len(self.hand) > 1:
      pick = int(Utils.read('Card to Play? '))
      played = self.hand[pick]
      self.discard(played)
      Utils.write('')
      played.effect(self, self._other_players())

  def discard(self, card):
    self.hand.remove(card)
    self.played.append(card)
    Utils.write('')
    card.discard_effect(self)

  def discard_all(self):
    self.played += self.hand
    self.hand = []

  def print_hand(self):
    for i, card in enumerate(self.hand):
      (val, name) = card.type_
      Utils.write('%d: %s (%d)' % (i, name, val))
    Utils.write('')

  def turn(self):
    Utils.write('\n%s\'s Turn:\n' % self.name)
    self.immune = False
    self.draw()
    self.play()

  def _other_players(self):
    return [p for p in self.game.players if p != self]
