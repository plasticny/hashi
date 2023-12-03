from structs import *
from random import choice, choices, shuffle, randint
from colorama import Fore, Style

class Board:
    def __init__(self, width:int, height:int):
        assert width > 0 and height > 0

        self.width = width
        self.height = height
        self.board:list[list[Box]] = []
        self.node_ls:list[Node] = []
    
    def get(self, pos:Position) -> Box:
        # if out of bound
        if pos.row < 0 or pos.row >= self.height or pos.col < 0 or pos.col >= self.width:
               return None
        return self.board[pos.row][pos.col]
    def get_relative(self, box:Box, dir:Direction) -> Box:
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
        

        def generate(self, _n:int):
        """
            Generate a new game board
            Args:
                `n`: number of node in the board
        """
        # first constrcut an answer board
        self.board = [
            [Box(row, col) for col in range(self.width)] for row in range(self.height)
        ]

        # choices n boxes as node
        _avai_node_set : set[Node] = set()
        _dir_ls = [Direction.UP(), Direction.BOTTOM(), Direction.LEFT(), Direction.RIGHT()]

        def _find_empty_boxes(__node:Node, __dir:Direction) -> list[Position]:
            __res = []
            __box = self.get_relative(__node, __dir.add(__dir))
            while __box is not None and __box.is_empty():
                __res.append(__box.position)
                __box = self.get_relative(__box, __dir)
            return __res

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

                while _pos is None:
                    _from_node = choice(list(_avai_node_set))
                    shuffle(_dir_ls)

                    for _dir in _dir_ls:
                        _empty_box_pos_ls = _find_empty_boxes(_from_node, _dir)
                        if len(_empty_box_pos_ls) != 0:
                            _pos = choice(_empty_box_pos_ls)
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

    def draw_line(self, from_node:Node, to_node:Node):
        horizon = from_node.position.row == to_node.position.row 
        vertical = from_node.position.col == to_node.position.col
        assert horizon or vertical

        dir = from_node.dir_to(to_node)
        box = self.get_relative(from_node, dir)
        while box.position != to_node.position:
            if horizon:
                _line = box.to_hl()
            else:
                _line = box.to_vl()
            self.board[box.position.row][box.position.col] = _line
            box = self.get_relative(box, dir)

board = Board(18, 8)
board.generate(10)
board.print_board()
