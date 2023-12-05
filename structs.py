from __future__ import annotations
from colorama import Fore, Style

class Direction:
    """Vector that represent a direction"""
    @staticmethod
    def UP() -> Direction:
        return Direction(-1, 0)
    @staticmethod
    def BOTTOM() -> Direction:
        return Direction(1, 0)
    @staticmethod
    def LEFT() -> Direction:
        return Direction(0, -1)
    @staticmethod
    def RIGHT() -> Direction:
        return Direction(0, 1)

    def __init__(self, v, h):
        """
            Args:
                v (number): vertical scalar, negative means up
                h (number): horizontal scalar, negative means left
        """
        self.v = v
        self.h = h
    def __eq__(self, _v):
        assert isinstance(_v, Direction)        
        return self.v == _v.v and self.h == _v.h

    def is_horizontal(self) -> bool:
        return self.v == 0 and self.h != 0
    def is_vertical(self) -> bool:
        return self.h == 0 and self.v != 0

    def add(self, _dir) -> Direction:
        assert isinstance(_dir, Direction)
        return Direction(self.v+_dir.v, self.h+_dir.h)
    def opposite(self) -> Direction:
        assert isinstance(self, Direction)
        return Direction(-self.v, -self.h)

class Position:
    """Position in the game board"""
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return f"{self.row} {self.col}"
    def __eq__(self, _value):
        assert isinstance(_value, Position)
        return self.row == _value.row and self.col == _value.col
    
    def move_to(self, dir) -> Position:
        assert isinstance(dir, Direction)
        return Position(self.row+dir.v, self.col+dir.h)
    
    def dir_to(self, _pos) -> Direction:
        assert isinstance(_pos, Position)
        _dv = _pos.row - self.row
        _dh = _pos.col - self.col
        
        _v = int(_dv / abs(_dv)) if _dv != 0 else 0
        _h = int(_dh / abs(_dh)) if _dh != 0 else 0
        return Direction(_v, _h)

# an empty box in the game board
class Box:
    def __init__(self, row:int, col:int):
        self.position = Position(row, col)

    def __str__(self):
        return '  '
    
    def is_empty(self) -> bool:
        return True
    
# Node
class Node(Box):
    def __init__(self, row, col):
        super().__init__(row, col)
        
        # number of this node
        self.n : int = 0 
        
        # variables related to linked node
        self.node_up : Node = None
        self.node_bottom : Node = None
        self.node_left : Node = None
        self.node_right : Node = None
        self.up_line_cnt : int = 0
        self.bottom_line_cnt : int = 0
        self.left_line_cnt : int = 0
        self.right_line_cnt : int = 0

    def __str__(self):
        line_cnt = self.get_line_cnt()
        if self.n == line_cnt:
            color = Fore.GREEN
        elif self.n > line_cnt:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        return f"{color}${self.n}{Style.RESET_ALL}"
    
    def is_empty(self) -> bool:
        return False
    
    def get_line_cnt(self) -> int:
        return self.up_line_cnt + self.bottom_line_cnt + self.left_line_cnt + self.right_line_cnt
    
    def get_line_cnt_in_dir(self, _dir:Direction) -> int:
        if _dir == Direction.UP():
            return self.up_line_cnt
        elif _dir == Direction.BOTTOM():
            return self.bottom_line_cnt
        elif _dir == Direction.LEFT():
            return self.left_line_cnt
        elif _dir == Direction.RIGHT():
            return self.right_line_cnt
    
    def get_node_in_dir(self, _dir:Direction) -> Node:
        if _dir == Direction.UP():
            return self.node_up
        elif _dir == Direction.BOTTOM():
            return self.node_bottom
        elif _dir == Direction.LEFT():
            return self.node_left
        elif _dir == Direction.RIGHT():
            return self.node_right
    
    def get_unlinked_dir(self) -> list[Direction]:
        res = []
        if self.up_line_cnt == 0:
            res.append(Direction.UP())
        if self.bottom_line_cnt == 0:
            res.append(Direction.BOTTOM())
        if self.left_line_cnt == 0:
            res.append(Direction.LEFT())
        if self.right_line_cnt == 0:
            res.append(Direction.RIGHT())
        return res
    
    def get_linked_dir(self) -> list[Direction]:
        res = []
        if self.up_line_cnt > 0:
            res.append(Direction.UP())
        if self.bottom_line_cnt > 0:
            res.append(Direction.BOTTOM())
        if self.left_line_cnt > 0:
            res.append(Direction.LEFT())
        if self.right_line_cnt > 0:
            res.append(Direction.RIGHT())
        return res
    
    def link_node(self, _node:Node):
        _dir = self.position.dir_to(_node.position)
        
        assert _dir.is_horizontal() or _dir.is_vertical()
        
        if _dir == Direction.UP():
            assert self.node_up is None or self.node_up == _node
            self.node_up = _node
            self.up_line_cnt += 1
        elif _dir == Direction.BOTTOM():
            assert self.node_bottom is None or self.node_bottom == _node
            self.node_bottom = _node
            self.bottom_line_cnt += 1
        elif _dir == Direction.LEFT():
            assert self.node_left is None or self.node_left == _node
            self.node_left = _node
            self.left_line_cnt += 1
        elif _dir == Direction.RIGHT():
            assert self.node_right is None or self.node_right == _node
            self.node_right = _node
            self.right_line_cnt += 1
            
    def unlink_dir(self, _dir:Direction):
        if _dir == Direction.UP():
            self.node_up.bottom_line_cnt -= 1
            self.up_line_cnt -= 1
            if self.node_up.bottom_line_cnt == 0:
                self.node_up.node_bottom = None
                self.node_up = None
        elif _dir == Direction.BOTTOM():
            self.node_bottom.up_line_cnt -= 1
            self.bottom_line_cnt -= 1
            if self.node_bottom.up_line_cnt == 0:
                self.node_bottom.node_up = None
                self.node_bottom = None
        elif _dir == Direction.LEFT():
            self.node_left.right_line_cnt -= 1
            self.left_line_cnt -= 1
            if self.node_left.right_line_cnt == 0:
                self.node_left.node_right = None
                self.node_left = None
        elif _dir == Direction.RIGHT():
            self.node_right.left_line_cnt -= 1
            self.right_line_cnt -= 1
            if self.node_right.left_line_cnt == 0:
                self.node_right.node_left = None
                self.node_right = None
            
    def clear_link(self):
        for dir in self.get_linked_dir():
            for _ in range(self.get_line_cnt_in_dir(dir)):
                self.unlink_dir(dir)
                    
# Line 
class Line(Box):
    def __init__(self, dir:Direction, row, col):
        super().__init__(row, col)
        
        self.dir = dir
        self.is_double : bool = False
        
    def is_empty(self) -> bool:
        return False

class HorizonLine(Line):
    def __init__(self, row, col):
        super().__init__(Direction.RIGHT(), row, col)
    def __str__(self):
        return '==' if self.is_double else '--'

class VerticalLine(Line):
    def __init__(self, row, col):
        super().__init__(Direction.UP(), row, col)
    def __str__(self):
        return '||' if self.is_double else ' |'
