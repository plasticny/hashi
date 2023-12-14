from __future__ import annotations
from colorama import Fore, Style

from board import Direction, Node
from skill import Wall as skill_wall
from structs import Node
from player import PvpPlayer
from structs import Direction, Node
from game import Game

class PvpGame(Game):
  """Hashi game with pvp feature"""
  def __init__(self) -> None:
    super().__init__()
    self.p1 = PvpPlayer(
      name='Player 1', color=Fore.GREEN, mp=0, 
      skills=[skill_wall(self.board)]
    )
    self.p2 = PvpPlayer(
      name='Player 2', color=Fore.CYAN, mp=1, 
      skills=[skill_wall(self.board)]
    )
    self.player = self.p1 # the player who own the turn
  
  def parse_input(self, move_input) -> tuple[Node, Direction, str]:
    """
      Add end turn action
      End turn move_input: 'f'
      Cast skill move_input: 'c'
    """
    if move_input == 'f':
      return (None, None, 'f')
    if move_input == 'c':
      return (None, None, 'c')
    return super().parse_input(move_input)
  
  # ==================== Handle actions ==================== #
  def handle_action_main(self, from_node: Node, direction: Direction, action: str):
    """Add end turn, and skill"""
    if action == 'f':
      self.handle_end_turn()
      return
    if action == 'c':
      self.handle_cast_skill()
      return
    super().handle_action_main(from_node, direction, action)
  
  def handle_undo(self):
    """
      Override handle_undo()
      Block undo in this mode
    """
    raise Exception('Cannot undo in pvp mode')
  
  def handle_double_draw(self, from_node: Node, to_node: Node, direction: Direction) -> None:
    """
      Override handle_double_draw()
      Block this action in this mode
    """
    raise Exception('Connot draw doube line in pvp mode')
  
  def handle_double_erase(self, from_node: Node, direction: Direction) -> None:
    """
      Override handle_double_erase()
      Block this action in this mode
    """
    raise Exception('Connot doube erase line in pvp mode')
  
  def handle_draw(self, from_node: Node, to_node: Node, direction: Direction) -> None:
    """Add attack"""
    super().handle_draw(from_node, to_node, direction)
    
    enemy = self.get_enemy(self.player)
    
    # damage to players
    # if a node is just full after the connection, it will deal damage to enemy
    dmg_to_enemy = int(from_node.is_just_full()) * from_node.n + int(to_node.is_just_full()) * to_node.n      
    if dmg_to_enemy > 0:
      enemy.take_damage(dmg_to_enemy)
    # if a node is over full after the connection, it will deal damage to self
    dmg_to_self = int(from_node.is_over_full()) * from_node.get_line_cnt() + int(to_node.is_over_full()) * to_node.get_line_cnt()    
    if dmg_to_self > 0:
      self.player.take_damage(dmg_to_self)
    
    # gain mp, 1 mp for each node that is just full after the connection
    mp_gain = int(from_node.is_just_full()) + int(to_node.is_just_full())
    if mp_gain > 0:
      self.player.gain_mp(mp_gain)
  
  def handle_end_turn(self):
    self.player.end_turn = True
    print(f'{self.player} end turn')
  
  def handle_cast_skill(self):
    self.player.print_skills()
    skill_idx = int(input('Choose Skill (0 to cancel): ')) - 1
    if skill_idx == -1:
      raise Exception('Cancel cast skill')
    skill = self.player.skills[skill_idx]
    self.player.cast_skill(skill)
  # ==================== Handle actions ==================== #
  
  def get_enemy(self, player : PvpPlayer) -> PvpPlayer:
    """Helper funtion, get the enemy PvpPlayer instance of `player`"""
    return self.p1 if player == self.p2 else self.p2
  
  def start(self):
    turn = 1
    
    while self.p1.hp > 0 and self.p2.hp > 0:
      print(f'{Fore.YELLOW}========= Turn {turn} ========={Style.RESET_ALL}')
      print(f'{self.p1} HP: {self.p1.hp} MP: {self.p1.mp}')
      print(f'{self.p2} HP: {self.p2.hp} MP: {self.p2.mp}')
      self.board.print_board()
      move = input(f'[{self.player}] Move: ')
      print()
      
      try:
        # parse input
        (from_node, direction, action) = self.parse_input(move)
        
        # actions
        self.handle_action_main(from_node, direction, action)
        
        # switch player
        enemy = self.get_enemy(self.player)
        if not enemy.end_turn:
          self.player = self.get_enemy(self.player)
        
        # check generate new board
        if self.board.is_finish() or self.board.is_all_node_full() or (self.p1.end_turn and self.p2.end_turn):
          self.board.generate(self.node_cnt)
          self.p1.end_turn = False
          self.p2.end_turn = False
          print('Generate new board')
          
        turn += 1

      except Exception as e:
        print(f"{Fore.YELLOW}{e}{Style.RESET_ALL}", end='\n\n')      
      print()

    print(f'{Fore.YELLOW}========= End Game ========={Style.RESET_ALL}')
    print(f'{self.p1} HP: {self.p1.hp} / {self.p2} HP: {self.p2.hp}')
    print(f'{self.p1 if self.p1.hp > 0 else self.p2} win')

if __name__ == '__main__':  
  # start game
  PvpGame().start()