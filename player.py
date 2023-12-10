from colorama import Fore, Style

class Player:
  def __init__(self, name : str = 'player', color : int = Fore.WHITE) -> None:
    self.name = name
    self.color = color
    
  def __str__(self) -> str:
    return f"{self.color}{self.name}{Style.RESET_ALL}"
  
class PvpPlayer(Player):
  @property
  def hp(self) -> int:
    return self._hp
  @property
  def mp(self) -> int:
    return self._mp
  
  def __init__(self, name : str = 'player', color : int = Fore.WHITE, hp : int = 30, mp = 0) -> None:
    super().__init__(name, color)
    self._hp = hp
    self._mp = mp
    self.end_turn = False
    
  def take_damage(self, damage : int) -> None:
    if damage < 0:
      raise ValueError('damage must be positive')
    self._hp -= damage if damage < self._hp else self._hp
