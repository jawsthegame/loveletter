class Player(object):
  def __init__(self, name, game):
    self.name = name
    self.game = game
    self.hand = []
    self.played = []
    self.wins = 0
    self.active = True
    self.immune = False

  def next_turn(self):
    self.immune = False

  def draw(self):
    self.hand.append(self.game.draw())
    if len(self.hand) is 2:
      self.hand[0].draw_effect()

  def play(self):
    if len(self.hand) > 1:
      Utils.read('Card to Play? ')

  def discard(self):
    pass

  def discard_all(self):
    self.played += self.hand
    self.hand = []

  def turn(self):
    self.draw()
    self.play()
