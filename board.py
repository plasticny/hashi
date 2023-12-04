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
        return self.get(box.position.move_to(dir))

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
                    if isinstance(box, Node) and box.node_right is not None:
                        padding_col = '--' if box.right_line_cnt == 1 else '=='
                    if isinstance(box, HorizonLine):
                        padding_col = '==' if box.is_double else '--'
                print(box, end=padding_col)
            print()
            
            # padding row
            if r_idx == self.height-1:
                continue
            print(f'{Fore.CYAN}  #{Style.RESET_ALL}', end='')
            for c_idx, box in enumerate(row):
                col = '  '
                if isinstance(box, Node) and box.node_bottom is not None:
                    col = ' |' if box.bottom_line_cnt == 1 else '||'
                if isinstance(box, VerticalLine):
                    col = '||' if box.is_double else ' |'
                print(col, end='  ')
            print()
            
    def generate(self, _n:int):
        """
            Generate a new game board
            Args:
                `n`: number of node in the board
        """
        # constrcut an empty board
        self.board = [
            [Box(row, col) for col in range(self.width)] for row in range(self.height)
        ]

        # created nodes the can be connected to other nodes
        _avai_node_set : set[Node] = set()

        # choose first random node
        _first_node = Node(randint(0, self.height-1), randint(0, self.width-1))
        self.board[_first_node.position.row][_first_node.position.col] = _first_node
        _avai_node_set.add(_first_node)
        self.node_ls.append(_first_node)

        # choose n-1 more boxes as node
        for _ in range(_n-1):
            # find a node and a direction that can create another node
            _from_node : Node = None
            _dir : Direction = None
            while _from_node is None or _dir is None:
                _from_node = choice(list(_avai_node_set))
                
                _unlinked_dir_ls = _from_node.get_unlinked_dir()
                if len(_unlinked_dir_ls) == 0:
                    _avai_node_set.remove(_from_node)
                    continue
                
                # randomly choose a direction
                _dir = choice(_unlinked_dir_ls)
                
            # choose a random empty box in this direction
            _empty_box_ls = []
            _b = self.get_relative(_from_node, _dir)
            while _b is not None and not isinstance(_b, Node) and not isinstance(_b, Line):
                _empty_box_ls.append(_b)
                _b = self.get_relative(_b, _dir)
            _box : Box = choice(_empty_box_ls)
            
            # convert box to node
            _to_node = Node(_box.position.row, _box.position.col)
            self.board[_box.position.row][_box.position.col] = _to_node
            _avai_node_set.add(_to_node)
            self.node_ls.append(_to_node)

            # draw a line
            self.draw_line(_from_node, _to_node)
            # increase number of line of both node
            _from_node.n += 1
            _to_node.n += 1
            
            # 50% chance to make it double
            if randint(0, 1) == 1:
                self.draw_line(_from_node, _to_node)
                _from_node.n += 1
                _to_node.n += 1
                
        # clear all link
        for r_idx, row in enumerate(self.board):
            for c_idx, box in enumerate(row):
                if isinstance(box, Node):
                    box.clear_link()
                elif isinstance(box, Line):
                    self.board[r_idx][c_idx] = Box(r_idx, c_idx)
        
    def draw_line(self, from_node:Node, to_node:Node):
        dir = from_node.position.dir_to(to_node.position)
        
        if dir.is_horizontal():
            line_class = HorizonLine
        elif dir.is_vertical():
            line_class = VerticalLine
        else:
            raise Exception('Drawing diagonal line')
        
        from_node.link_node(to_node)
        to_node.link_node(from_node)
        
        box = self.get_relative(from_node, dir)
        while box.position != to_node.position:
            if isinstance(box, Line):
                box.is_double = True
            else:
                _line = line_class(box.position.row, box.position.col)
                self.board[box.position.row][box.position.col] = _line
            box = self.get_relative(box, dir)

board = Board(15, 10)
board.generate(46)
board.print_board()
