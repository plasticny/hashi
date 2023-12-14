from board import Board
from geometric import Position
from colorama import Fore, Style

class Skill:
  def __init__(self, name, cost):
    self.name = name
    self.cost = cost
    
  def __str__(self) -> str:
    return self.name
    
  def cast(self):
    print(f'[{Fore.YELLOW}Skill {self.name}{Style.RESET_ALL}]')
  
class Wall(Skill):
  def __init__(self, board):
    super().__init__('wall', 2)
    self.board : Board = board
    
  def cast(self):
    while True:
      in_pos = input('Position: ')
      col = int(in_pos[0:2])
      row = int(in_pos[2:4])
      try:
        self.board.set_wall(Position(row, col))
        break
      except Exception as e:
        print(e)