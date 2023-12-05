from __future__ import annotations

from structs import *
from board import *
from colorama import Fore, Style

class Game:
  def __init__(self, row, col, node_cnt):
    self.board = Board(row, col)
    self.board.generate(node_cnt)
    
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
  
  def handle_action(self, from_node : Node, direction : Direction, action : str):
    # undo
    if action == 'r':
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
    
    # get to_node
    if from_node.get_node_in_dir(direction) is None:
      to_node = self.board.get_nearest_non_empty(from_node, direction)
      if not isinstance(to_node, Node):
        raise Exception('Cannot draw line there')
    else:
      to_node = from_node.get_node_in_dir(direction)  
    
    connected_line_cnt = from_node.get_line_cnt_in_dir(direction)
    # draw a line
    if action == 'd':
      if connected_line_cnt == 2:
        raise Exception('Cannot draw line there')
      self.board.draw_line(from_node, to_node)
    # draw a double line
    elif action == 'dd':
      if connected_line_cnt != 0:
        raise Exception('Cannot draw line there')
      self.board.draw_line(from_node, to_node)
      self.board.draw_line(from_node, to_node)
    # erase a line
    elif action == 'e':
      if connected_line_cnt > 0:
        self.board.erase_line(from_node, direction)
    # double erase line
    elif action == 'ee':
      if connected_line_cnt == 2:
        self.board.erase_line(from_node, direction)
      if connected_line_cnt == 1:
        self.board.erase_line(from_node, direction)
  
  def start(self):
    while not self.board.is_finish():
      self.board.print_board()
      move = input('Move: ')
      print()
      
      try:  
        # parse input
        (from_node, direction, action) = self.parse_input(move)
        
        # actions
        self.handle_action(from_node, direction, action)
        
        # add to move history
        if action != 'r':
          self.move_history.append((from_node, direction, action))

      except Exception as e:
        print(f"{Fore.YELLOW}{e}{Style.RESET_ALL}", end='\n\n')
        continue
      
    self.board.print_board()
    print(f"{Fore.GREEN}Game over{Style.RESET_ALL}")
    
if __name__ == '__main__':
  print(f"{Fore.GREEN}########## Hashi ##########{Style.RESET_ALL}")
  
  # setup game
  print(f"{Fore.CYAN}==== Setup game ====")
  print(f'If you do not know how to setup, try 9 for row, 6 for col, 15 for number of node{Style.RESET_ALL}')
  row = int(input('Row: '))
  col = int(input('Col: '))
  node_cnt = int(input('Number of node: '))
  print()
  
  # print player guide
  print(f"{Fore.CYAN}===== Player guide ====={Style.RESET_ALL}")
  print(f'{Fore.GREEN}You can wiki hashi for game rule{Style.RESET_ALL}')
  print(f'{Fore.YELLOW}Input Format{Style.RESET_ALL}: {"{col, 2 char}{row, 2 char}{direction, 1 char}{action, remaining char}"}')
  print(f'{Fore.YELLOW}Direction{Style.RESET_ALL}: "8" for up, "2" for down, "4" for left, "6" for right')
  print(f'{Fore.YELLOW}Action{Style.RESET_ALL}: ""/"d" for draw, "dd" for double draw, "e" for erase, "ee" for double erase')
  print(f'{Fore.YELLOW}Example{Style.RESET_ALL}: "010208d" for draw a single line from (01, 02) to the node in the up direction (8)')
  print()
  print(f'{Fore.YELLOW}Note{Style.RESET_ALL}: Enter "r" only to undo a move')
  print()
  
  # start game
  game = Game(row, col, node_cnt)
  game.start()