from __future__ import annotations

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
