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
        self.n = 0
        self.node_up : Node = None
        self.node_bottom : Node = None
        self.node_left : Noe = None
        self.node_right : Node = None

    def __str__(self):
        return f"0{self.n}"

    def is_empty(self):
        return False

    def is_line(self):
        return False
        
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
        super().__init__(row, col, Direction.UP)
    def __str__(self):
        return '||' if self.is_double else ' |'

class HorizonLine(Line):
    def __init__(self, row, col):
        super().__init__(row, col, Direction.RIGHT)
    def __str__(self):
        return '==' if self.is_double else '--'

