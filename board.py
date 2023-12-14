from structs import Box, Node, Line, HorizonLine, VerticalLine, Wall
from geometric import Position, Direction
from random import choice, randint
from colorama import Fore, Style
from math import ceil

class Board:
    def __init__(self, width:int, height:int):
        if not(width >= 2 and height >=2):
            raise Exception('Board size must be at least 2x2')

        self.width = width
        self.height = height
        self.board:list[list[Box]] = []
        self.node_ls:list[Node] = []
    
    # ==================== Get box in board ==================== #
    def get(self, pos:Position) -> Box:
        """Get box in `pos`"""
        # if out of bound
        if pos.row < 0 or pos.row >= self.height or pos.col < 0 or pos.col >= self.width:
            return None
        return self.board[pos.row][pos.col]
    
    def get_relative(self, box:Box, dir:Direction) -> Box:
        """Get the near box in `dir` from `box`"""
        return self.get(box.position.move_to(dir))
    
    def get_nearest_non_empty(self, box:Box, dir:Direction) -> Box:
        """Get the near non empty box in `dir` from `box`"""
        _box = self.get_relative(box, dir)
        while _box is not None and _box.is_empty():
            _box = self.get_relative(_box, dir)
        return _box    
    # ==================== Get box in board ==================== #
        
    # ==================== Board Manipulation ==================== #
    def draw_line(self, from_node:Node, to_node:Node):        
        dir = from_node.position.dir_to(to_node.position)
        
        if dir.is_horizontal():
            line_class = HorizonLine
        elif dir.is_vertical():
            line_class = VerticalLine
        else:
            raise Exception('Drawing diagonal line')
        
        if from_node.get_line_cnt_in_dir(dir) == 2:
            raise Exception('Already have 2 lines in this direction')
        
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
            
    def erase_line(self, node:Node, dir:Direction):
        if node.get_line_cnt_in_dir(dir) == 0:
            raise Exception('No line in this direction')
        
        node.unlink_dir(dir)
        
        box = self.get_relative(node, dir)
        while isinstance(box, Line):
            if box.is_double:
                box.is_double = False
            else:
                self.board[box.position.row][box.position.col] = Box(box.position.row, box.position.col)
            box = self.get_relative(box, dir)

    def set_wall(self, pos:Position):
        box = self.get(pos)
        if not isinstance(box, Box):
            raise Exception('Not a box')
        if not box.is_empty():
            raise Exception('Not an empty box')
        self.board[pos.row][pos.col] = Wall(pos.row, pos.col)
    # ==================== Board Manipulation ==================== #

    # ==================== Board status checkers ==================== #
    def print_board(self):
        def print_col_number():
            print(f'  {Fore.CYAN}#{Fore.WHITE}', end='')
            for i in range(self.width):
                if i < 10:
                    print(0, end='')
                print(i, end=' ' if i < self.width-1 else '')
            print(f'{Fore.CYAN}#{Style.RESET_ALL}')
            return
        def print_horizon_line():
            print(f'{Fore.CYAN}{"#"*((self.width+1)*3+2)}{Style.RESET_ALL}')
            return
        
        # header
        print_col_number()
        print_horizon_line()

        # body
        for r_idx, row in enumerate(self.board):
            print(f'{Fore.WHITE}{"0" if r_idx < 10 else ""}{r_idx}{Fore.CYAN}#', end='')
            print(Style.RESET_ALL, end='')
            for c_idx, box in enumerate(row):
                padding_col = ''
                if c_idx < self.width-1:
                    padding_col = ' '
                    if isinstance(box, Node) and box.node_right is not None:
                        padding_col = '-' if box.right_line_cnt == 1 else '='
                    if isinstance(box, HorizonLine):
                        padding_col = '-' if not box.is_double else '='
                print(box, end=padding_col)
            print(f'{Fore.CYAN}#{Fore.WHITE}{"0" if r_idx < 10 else ""}{r_idx}')
            
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
                print(col, end=' ' if c_idx < self.width-1 else '')
            print(f'{Fore.CYAN}#{Style.RESET_ALL}')
            
        # footer
        print_horizon_line()
        print_col_number()
    
    def is_finish(self) -> bool:
        """
            Check if all node has just enough line connected to it,\n
            and all nodes can be reached from the first node
        """        
        _visited_node_set = set()
        _visited_node_set.add(self.node_ls[0])
        _node_ls = [self.node_ls[0]]
        while len(_node_ls) > 0:
            _node = _node_ls.pop()
            
            # check if just enough line connected to it
            if _node.n != _node.get_line_cnt():
                return False
            
            # add all linked node to the list
            for _dir in _node.get_linked_dir():
                _n = _node.get_node_in_dir(_dir)
                if _n not in _visited_node_set:
                    _visited_node_set.add(_n)
                    _node_ls.append(_n)
        
        # check if all node can be reached
        return len(_visited_node_set) == len(self.node_ls)
    
    def is_all_node_full(self):
        """Check if all node are full or overfull"""
        for node in self.node_ls:
            if node.n > node.get_line_cnt():
                return False
        return True
    # ==================== Board status checkers ==================== #
    
    # ==================== Board Generate ==================== #
    def generate(self, _n:int):
        """
            Generate a new game board
            Args:
                `n`: number of node in the board
        """
        w = ceil(self.width/2)
        h = ceil(self.height/2)
        assert _n > 1 and _n <= w * h, f"Number of node of a {self.width}x{self.height} board must be between 2 and {w*h}"
        
        # first constrcut an board with size width/2 x height/2
        temp_board = Board(w, h)
        temp_board.board = [
            [Box(row, col) for col in range(temp_board.width)] for row in range(temp_board.height)
        ]

        # choose first random node
        _first_node = Node(randint(0, temp_board.height-1), randint(0, temp_board.width-1))
        temp_board.board[_first_node.position.row][_first_node.position.col] = _first_node
        temp_board.node_ls.append(_first_node)

        # created nodes the can be connected to other nodes
        _avai_node_set : set[Node] = set()        
        _avai_node_set.add(_first_node)

        # choose n-1 more boxes as node
        for _ in range(_n-1):
            # find a node and a direction that can create another node
            _from_node : Node = None
            _dir : Direction = None
            while _from_node is None or _dir is None:
                if len(_avai_node_set) == 0:
                    break
                
                _node = choice(list(_avai_node_set))
                
                _avai_dir_ls = []
                for _dir in _node.get_unlinked_dir():
                    _b = temp_board.get_relative(_node, _dir)
                    if _b is not None and _b.is_empty():
                        _avai_dir_ls.append(_dir)
                
                if len(_avai_dir_ls) == 0:
                    _avai_node_set.remove(_node)
                    continue
                                
                _from_node = _node
                _dir = choice(_avai_dir_ls)
                
            if len(_avai_node_set) == 0:
                break
                
            # choose a random empty box in this direction
            _empty_box_ls = []
            _b = temp_board.get_relative(_from_node, _dir)
            while _b is not None and _b.is_empty():
                _empty_box_ls.append(_b)
                _b = temp_board.get_relative(_b, _dir)
            _box : Box = choice(_empty_box_ls)
            
            # convert box to node
            _to_node = Node(_box.position.row, _box.position.col)
            temp_board.board[_box.position.row][_box.position.col] = _to_node
            _avai_node_set.add(_to_node)
            temp_board.node_ls.append(_to_node)

            # draw a line, and increase number of line of both node
            temp_board.draw_line(_from_node, _to_node)
            _from_node.n += 1
            _to_node.n += 1
            
            # 50% chance to double it
            if randint(0, 1) == 1:
                temp_board.draw_line(_from_node, _to_node)
                _from_node.n += 1
                _to_node.n += 1
                
        # construct the real board by adding padding
        self.board = []
        for tr_idx, t_row in enumerate(temp_board.board):
            row = []
            r_idx = tr_idx * 2
            for tc_idx, t_col in enumerate(t_row):
                c_idx = tc_idx * 2
                if isinstance(t_col, Node):
                    node = Node(r_idx, c_idx)
                    node.n = t_col.n
                    self.node_ls.append(node)
                    row.append(node)
                else:
                    row.append(Box(r_idx, c_idx))
                
                # padding col
                if c_idx < self.width-1:
                    row.append(Box(r_idx, c_idx+1))
            self.board.append(row)
            
            # padding row
            if r_idx < self.height-1:
                self.board.append([Box(r_idx+1, c_idx) for c_idx in range(self.width)])
    # ==================== Board Generate ==================== #