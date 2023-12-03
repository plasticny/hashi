from structs import *
from random import choice, shuffle, randint
from colorama import Fore, Style

class Board:
    def __init__(self, width:int, height:int):
        assert width > 0 and height > 0

        self.width = width
        self.height = height
        self.board:list[list[Box]] = []
        self.node_ls:list[Node] = []
    
    def get(self, pos:Position) -> Box:
        """Get box in `pos`"""
        # if out of bound
        if pos.row < 0 or pos.row >= self.height or pos.col < 0 or pos.col >= self.width:
               return None
        return self.board[pos.row][pos.col]
    
    def get_relative(self, box:Box, dir:Direction) -> Box:
        """Get the nearest box in `dir` from `box`"""
        return self.get(box.position.add(dir))

    def print_board(self):
        # header
        print(f'  {Fore.CYAN}#{Fore.GREEN}', end='')
        for i in range(self.width):
            if i < 10:
                print(0, end='')
            print(i, end='  ' if i < self.width-1 else '')
        print(Style.RESET_ALL)

        # 2nd row split line
        print(f'{Fore.CYAN}{"#"*(self.width*4+1)}{Style.RESET_ALL}')

        # body
        for r_idx, row in enumerate(self.board):
            print(f'{Fore.GREEN}{"0" if r_idx < 10 else ""}{r_idx}{Fore.CYAN}#', end='')
            print(Style.RESET_ALL, end='')
            for c_idx, box in enumerate(row):
                padding_col = '  '
                if c_idx < self.width-1:
                    if (box.is_node() and box.node_right is not None):
                        padding_col = '--' if box.right_line_cnt == 1 else '=='
                    if (box.is_line() and box.dir == Direction.RIGHT()):
                        padding_col = '==' if box.is_double else '--'
                print(box, end=padding_col)
            print()
            
            # padding row
            if r_idx == self.height-1:
                continue
            print(f'{Fore.CYAN}  #{Style.RESET_ALL}', end='')
            for c_idx, box in enumerate(row):
                col = '  '
                if (box.is_node() and box.node_bottom is not None):
                    col = ' |' if box.bottom_line_cnt == 1 else '||'
                if (box.is_line() and box.dir == Direction.UP()):
                    col = '||' if box.is_double else ' |'
                print(col, end='  ')
            print()
            

    def generate(self, _n:int):
        """
            Generate a new game board
            Args:
                `n`: number of node in the board
        """
        def _find_empty_boxes(__node:Node, __dir:Direction) -> list[Position]:
            """Find all empty boxed in a direction from a node"""
            __res = []
            __box = self.get_relative(__node, __dir)
            while __box is not None and __box.is_empty():
                __res.append(__box.position)
                __box = self.get_relative(__box, __dir)
            return __res

        # first constrcut an answer board
        self.board = [
            [Box(row, col) for col in range(self.width)] for row in range(self.height)
        ]

        # choices n boxes as node
        _avai_node_set : set[Node] = set()
        _dir_ls = [Direction.UP(), Direction.BOTTOM(), Direction.LEFT(), Direction.RIGHT()]
        for _i in range(_n):
            if _i == 0:
                # first node, randomly choice a box
                _row = randint(0, self.height-1)
                _col = randint(0, self.width-1)
                
                _node = self.board[_row][_col].to_Node()
                self.board[_row][_col] = _node
                
                _avai_node_set.add(_node)
                self.node_ls.append(_node)
            else:
                # after first node
                _pos = None
                _dir = None

                # find an availabe node to connect
                while _pos is None:
                    _from_node = choice(list(_avai_node_set))
                    shuffle(_dir_ls)

                    for _d in _dir_ls:
                        _empty_box_pos_ls = _find_empty_boxes(_from_node, _d)
                        if len(_empty_box_pos_ls) != 0:
                            _pos = choice(_empty_box_pos_ls)
                            _dir = _d
                            break

                    # if pos is None in here, from_node cannot connect more node
                    # remove it from avai_node_set
                    if _pos is None:
                        _avai_node_set.remove(_from_node)

                _to_node = self.get(_pos).to_Node()
                
                # add to board
                self.board[_pos.row][_pos.col] = _to_node
                
                _avai_node_set.add(_to_node)
                self.node_ls.append(_to_node)

                # draw a line
                self.draw_line(_from_node, _to_node)

                # increase line counter of both node
                _from_node.n += 1
                _to_node.n += 1
                
                # set linked node
                _from_node.link_node(_to_node, _dir)
                _to_node.link_node(_from_node, _dir.opposite())

        # for each connection, 50% chance to make it double
        for _node in self.node_ls:
            if _node.node_right is not None and randint(0, 1) == 1:
                # draw a line
                self.draw_line(_node, _node.node_right)

                # increase line counter of both node
                _node.n += 1
                _node.node_right.n += 1
                
                # set linked node
                _node.link_node(_node.node_right, Direction.RIGHT())
                _node.node_right.link_node(_node, Direction.LEFT())
                
            if _node.node_bottom is not None and randint(0, 1) == 1:
                # draw a line
                self.draw_line(_node, _node.node_bottom)

                # increase line counter of both node
                _node.n += 1
                _node.node_bottom.n += 1
                
                # set linked node
                _node.link_node(_node.node_bottom, Direction.BOTTOM())
                _node.node_bottom.link_node(_node, Direction.UP())
                
        # clear all link
        for r_idx, row in enumerate(self.board):
            for c_idx, box in enumerate(row):
                if box.is_node():
                    box.clear_link()
                elif box.is_line():
                    self.board[r_idx][c_idx] = box.to_Box()
        
    def draw_line(self, from_node:Node, to_node:Node):
        horizon = from_node.position.row == to_node.position.row 
        vertical = from_node.position.col == to_node.position.col
        assert horizon or vertical

        dir = from_node.dir_to(to_node)
        box = self.get_relative(from_node, dir)
        while box.position != to_node.position:
            if horizon:
                if box.is_line():
                    box.is_double = True
                else:
                    _line = box.to_hl()
                    self.board[box.position.row][box.position.col] = _line
            else:
                if box.is_line():
                    box.is_double = True
                else:
                    _line = box.to_vl()
                    self.board[box.position.row][box.position.col] = _line
            box = self.get_relative(box, dir)

board = Board(15, 10)
board.generate(46)
board.print_board()
