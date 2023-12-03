from __future__ import annotations

class Direction():
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
        self.v = v
        self.h = h

    def __eq__(self, _v):
        if not (hasattr(_v, 'v') and hasattr(_v, 'h')):
            return False
        return self.v == _v.v and self.h == _v.h

    def add(self, _dir):
        return Direction(self.v+_dir.v, self.h+_dir.h)
    
    def opposite(self) -> Direction:
        return Direction(-self.v, -self.h)

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return f"{self.row} {self.col}"
    def __eq__(self, _value):
        if not hasattr(_value, 'row') or not hasattr(_value, 'col'):
            return False
        return self.row == _value.row and self.col == _value.col
    
    def add(self, dir:Direction) -> Position:
        return Position(self.row+dir.v, self.col+dir.h)

    def to_direction(self) -> Direction:
        _v = int(self.row / abs(self.row)) if self.row != 0 else 0
        _h = int(self.col / abs(self.col)) if self.col != 0 else 0
        return Direction(_v, _h)
    
# an empty box in the game board
class Box:
    def __init__(self, row, col):
        self.position : Position = Position(row, col)

    def __str__(self):
        return '  '
    
    def is_empty(self):
        return True

    def is_line(self):
        return False
    
    def is_node(self):
        return False
        
    def to_Box(self) -> Box:
        return Box(self.position.row, self.position.col)
        
    def to_Node(self) -> Node:
        return Node(self.position.row, self.position.col)

    def to_vl(self) -> VerticalLine:
        return VerticalLine(self.position.row, self.position.col)

    def to_hl(self) -> HorizonLine:
        return HorizonLine(self.position.row, self.position.col)

    def dir_to(self, _box) -> Direction:
        p = Position(
                _box.position.row - self.position.row,
                _box.position.col - self.position.col
            )
        return p.to_direction()

class Node(Box):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.n : int = 0
        
        self.node_up : Node = None
        self.node_bottom : Node = None
        self.node_left : Node = None
        self.node_right : Node = None
        
        self.up_line_cnt : int = 0
        self.bottom_line_cnt : int = 0
        self.left_line_cnt : int = 0
        self.right_line_cnt : int = 0

    def __str__(self):
        return f"${self.n}"

    def is_empty(self):
        return False
    
    def is_node(self):
        return True
    
    def link_node(self, _node:Node, _dir:Direction):
        if _dir == Direction.UP():
            self.node_up = _node
            self.up_line_cnt += 1
        elif _dir == Direction.BOTTOM():
            self.node_bottom = _node
            self.bottom_line_cnt += 1
        elif _dir == Direction.LEFT():
            self.node_left = _node
            self.left_line_cnt += 1
        elif _dir == Direction.RIGHT():
            self.node_right = _node
            self.right_line_cnt += 1
            
    def unlink_node(self, _dir:Direction):
        if _dir == Direction.UP():
            self.node_up.bottom_line_cnt = 0
            self.up_line_cnt = 0
            self.node_up.node_bottom = None
            self.node_up = None
        elif _dir == Direction.BOTTOM():
            self.node_bottom.up_line_cnt = 0
            self.bottom_line_cnt = 0
            self.node_bottom.node_up = None
            self.node_bottom = None
        elif _dir == Direction.LEFT():
            self.node_left.right_line_cnt = 0
            self.left_line_cnt = 0
            self.node_left.node_right = None
            self.node_left = None
        elif _dir == Direction.RIGHT():
            self.node_right.left_line_cnt = 0
            self.right_line_cnt = 0
            self.node_right.node_left = None
            self.node_right = None
            
    def clear_link(self):
        if self.node_up is not None:
            self.unlink_node(Direction.UP())
        if self.node_bottom is not None:
            self.unlink_node(Direction.BOTTOM())
        if self.node_left is not None:
            self.unlink_node(Direction.LEFT())
        if self.node_right is not None:
            self.unlink_node(Direction.RIGHT())
        
# Line 
class Line(Box):
    def __init__(self, row, col, dir:Direction):
        super().__init__(row, col)
        self.dir = dir
        self.is_double : bool = False
    
    def is_empty(self):
        return False

    def is_line(self):
        return True

class VerticalLine(Line):
    def __init__(self, row, col):
        super().__init__(row, col, Direction.UP())
    def __str__(self):
        return '||' if self.is_double else ' |'

class HorizonLine(Line):
    def __init__(self, row, col):
        super().__init__(row, col, Direction.RIGHT())
    def __str__(self):
        return '==' if self.is_double else '--'

