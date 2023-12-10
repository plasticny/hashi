from __future__ import annotations
from board import Direction, Node

from structs import *
from board import *
from player import *
from colorama import Fore, Style

from structs import Direction, Node

class Game:
  """Basic hashi game"""
  def __init__(self):
    print(f"{Fore.GREEN}########## Hashi ##########{Style.RESET_ALL}")
    
    row, col, node_cnt = self.setup()
    
    self.board = Board(row, col)
    self.board.generate(node_cnt)
    
    self.node_cnt = node_cnt
    
    # move history, each element is a tuple of (from_node, direction, action)
    self.move_history : list[tuple[Node, Direction, str]] = []
      
  def parse_input(self, move_input) -> tuple[Node, Direction, str]:
    """
      Parse input to get from_node, direction, action

      `move_input format`: 
        type 1: '{col, 2 char}{row, 2 char}{direction, 1 char}{action, remaining char}'\n
        type 2: '{action, r}'
      
      `direction`:
        '8' for up, '2' for down, '4' for left, '6' for right\n
        
      `action`:
        ''/'d' for draw, 'dd' for double draw, 'e' for erase, 'ee' for double erase\n
        'r' for undo
    """
    # undo
    if move_input == 'r':
      return (None, None, 'r')
    
    col = int(move_input[0:2])
    row = int(move_input[2:4])
    direction = move_input[4]
    action = move_input[5:]
    
    # check if col and row are valid
    from_node = self.board.get(Position(row, col))
    if not isinstance(from_node, Node):
      raise ValueError('No node at position ({}, {})'.format(col, row))
    
    # parse direction
    if direction == '8':
      direction = Direction.UP()
    elif direction == '2':
      direction = Direction.BOTTOM()
    elif direction == '4':
      direction = Direction.LEFT()
    elif direction == '6':
      direction = Direction.RIGHT()
    else:
      raise ValueError('Invalid direction')
    
    # check if action input is valid
    if action not in ['d', 'dd', 'e', 'ee', '']:
      raise ValueError('Invalid action')
    if action == '':
      action = 'd'
    
    return (from_node, direction, action)
  
  # ==================== Handle actions ==================== #
  def handle_action_main(self, from_node : Node, direction : Direction, action : str):
    """Main process of handling action"""
    # undo
    if action == 'r':
      self.handle_undo()
      return      
    
    # get to_node
    if from_node.get_node_in_dir(direction) is None:
      to_node = self.board.get_nearest_non_empty(from_node, direction)
      if not isinstance(to_node, Node):
        raise Exception('Cannot draw line there')
    else:
      to_node = from_node.get_node_in_dir(direction)  
    
    # draw a line
    if action == 'd':
      self.handle_draw(from_node, to_node, direction)
    # draw a double line
    elif action == 'dd':
      self.handle_double_draw(from_node, to_node, direction)
    # erase a line
    elif action == 'e':
      self.handle_erase(from_node, direction)
    # double erase line
    elif action == 'ee':
      self.handle_double_erase(from_node, direction)
  
  def handle_undo(self):
    if len(self.move_history) == 0:
        raise Exception('No move to undo')
    (from_node, direction, action) = self.move_history.pop()
    
    # reverse action
    if action == 'd':
      action = 'e'
    elif action == 'e':
      action = 'd'
    elif action == 'dd':
      action = 'ee'
    elif action == 'ee':
      action = 'dd' 
      
    self.handle_action_main(from_node, direction, action)
  
  def handle_draw(self, from_node : Node, to_node : Node, direction : Direction) -> None:
    if from_node.get_line_cnt_in_dir(direction) == 2:
      raise Exception('Cannot draw line there')
    self.board.draw_line(from_node, to_node)
  
  def handle_double_draw(self, from_node : Node, to_node : Node, direction : Direction) -> None:
    if from_node.get_line_cnt_in_dir(direction) != 0:
      raise Exception('Cannot draw line there')
    self.board.draw_line(from_node, to_node)
    self.board.draw_line(from_node, to_node)
  
  def handle_erase(self, from_node : Node, direction : Direction) -> None:
    if from_node.get_line_cnt_in_dir(direction) > 0:
      self.board.erase_line(from_node, direction)

  def handle_double_erase(self, from_node : Node, direction : Direction) -> None:
    connected_line_cnt = from_node.get_line_cnt_in_dir(direction)
    if connected_line_cnt == 2:
      self.board.erase_line(from_node, direction)
    if connected_line_cnt == 1:
      self.board.erase_line(from_node, direction)
  # ==================== Handle actions ==================== #
  
  def setup(self) -> tuple[int, int, int]:
    """Setup game"""
    print(f"{Fore.CYAN}==== Setup game ====")
    print(f'If you do not know how to setup, try 9 for row, 6 for col, 15 for number of node{Style.RESET_ALL}')
    row = int(input('Row: '))
    col = int(input('Col: '))
    node_cnt = int(input('Number of node: '))
    print()
    return (row, col, node_cnt)
  
  def print_guide(self):
    print(f"{Fore.CYAN}===== Player guide ====={Style.RESET_ALL}")
    print(f'{Fore.GREEN}You can wiki hashi for game rule{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Input Format{Style.RESET_ALL}: {"{col, 2 char}{row, 2 char}{direction, 1 char}{action, remaining char}"}')
    print(f'{Fore.YELLOW}Direction{Style.RESET_ALL}: "8" for up, "2" for down, "4" for left, "6" for right')
    print(f'{Fore.YELLOW}Action{Style.RESET_ALL}: ""/"d" for draw, "dd" for double draw, "e" for erase, "ee" for double erase')
    print(f'{Fore.YELLOW}Example{Style.RESET_ALL}: "010208d" for draw a single line from (01, 02) to the node in the up direction (8)')
    print()
    print(f'{Fore.YELLOW}Note{Style.RESET_ALL}: Enter "r" only to undo a move')
    print()
  
  def start(self):
    self.print_guide()
    
    while not self.board.is_finish():
      self.board.print_board()
      move = input('Move: ')
      print()
      
      try:  
        # parse input
        (from_node, direction, action) = self.parse_input(move)
        
        # actions
        self.handle_action_main(from_node, direction, action)
        
        # add to move history
        if action != 'r':
          self.move_history.append((from_node, direction, action))

      except Exception as e:
        print(f"{Fore.YELLOW}{e}{Style.RESET_ALL}", end='\n\n')
      
    self.board.print_board()
    print(f"{Fore.GREEN}Game over{Style.RESET_ALL}")

class PvpGame(Game):
  """Hashi game with pvp feature"""
  def __init__(self) -> None:
    super().__init__()
    self.p1 = PvpPlayer(name='Player 1', color=Fore.GREEN)
    self.p2 = PvpPlayer(name='Player 2', color=Fore.CYAN)
    self.player = self.p1 # store the current turn belongs to which player
  
  def parse_input(self, move_input) -> tuple[Node, Direction, str]:
    """
      Add end turn action
      End turn move_input: 'f'
    """
    if move_input == 'f':
      return (None, None, 'f')
    return super().parse_input(move_input)
  
  # ==================== Handle actions ==================== #
  def handle_action_main(self, from_node: Node, direction: Direction, action: str):
    """Add end turn"""
    if action == 'f':
      self.handle_end_turn()
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
    dmg = 0
    if from_node.is_just_full():
      dmg += from_node.n
    if to_node.is_just_full():
      dmg += to_node.n
    
    if dmg > 0:
      print(f'{enemy} take {Fore.RED}{dmg}{Style.RESET_ALL} damage')
      enemy.take_damage(dmg)
  
  def handle_end_turn(self):
    self.player.end_turn = True
    print(f'{self.player} end turn')
  # ==================== Handle actions ==================== #
  
  def get_enemy(self, player : PvpPlayer) -> PvpPlayer:
    """Helper funtion, get the enemy PvpPlayer instance of `player`"""
    return self.p1 if player == self.p2 else self.p2
  
  def start(self):
    turn = 1
    
    while self.p1.hp > 0 and self.p2.hp > 0:
      print(f'{Fore.YELLOW}========= Turn {turn} ========={Style.RESET_ALL}')
      print(f'{self.p1} HP: {self.p1.hp} / {self.p2} HP: {self.p2.hp}')
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

      except Exception as e:
        print(f"{Fore.YELLOW}{e}{Style.RESET_ALL}", end='\n\n')
        
      finally:
        turn += 1
        # check generate new board
        if self.board.is_finish() or self.board.is_all_node_full() or (self.p1.end_turn and self.p2.end_turn):
          self.board.generate(self.node_cnt)
          self.p1.end_turn = False
          self.p2.end_turn = False
          print('Generate new board')
      
      print()
    
    print(f'{Fore.YELLOW}========= End Game ========={Style.RESET_ALL}')
    print(f'{self.p1} HP: {self.p1.hp} / {self.p2} HP: {self.p2.hp}')
    if self.p1.hp > 0:
      print(f'{self.p1} win')
    else:
      print(f'{self.p2} win')

if __name__ == '__main__':  
  # start game
  # Game().start()
  PvpGame().start()