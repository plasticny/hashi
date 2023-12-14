from colorama import Fore, Style
from skill import Skill

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
  
  def __init__(
      self, name : str = 'player', color : int = Fore.WHITE, 
      hp : int = 30, mp : int = 0,
      skills : list[Skill] = []
    ) -> None:
    super().__init__(name, color)
    self._hp = hp
    self._mp = mp
    self.end_turn = False
    self.skills = skills

  def take_damage(self, damage : int) -> None:
    assert damage >= 0, 'damage must not be negative'
    self._hp -= damage if damage < self._hp else self._hp
    print(f'{self} takes {Fore.RED}{damage}{Style.RESET_ALL} damage')

  def gain_mp(self, mp : int) -> None:
    assert mp >= 0, 'mp must not be negative'
    self._mp += mp
    print(f'{self} gains {Fore.BLUE}{mp}{Style.RESET_ALL} MP')

  def print_skills(self) -> None:
    print(f'{self} skills:')
    for i, skill in enumerate(self.skills):
      print(f'{i+1}. {skill} ({skill.cost} MP)')
      
  def cast_skill(self, skill : Skill) -> None:
    if self.mp < skill.cost:
      raise Exception('Not enough mana')
    skill.cast()
    self._mp -= skill.cost
