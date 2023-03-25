class Rectangle:
  def __init__(self, width, height) -> None:
    self.width = width
    self.height = height
  
  def set_width(self, width):
    self.width = width

  def set_height(self, height):
    self.height = height

  def get_area(self):
    return self.width * self.height
  
  def get_perimeter(self):
    return 2 * self.width + 2 * self.height
  
  def get_diagonal(self):
     return ((self.width ** 2 + self.height ** 2) ** .5)
  
  def get_picture(self):
    if self.width > 50 or self.height > 50:
      return "Too big for picture."
    
    picture = ""
    for _ in range(self.height):
      picture += ("*"*self.width) + "\n"

    return picture
  
  def get_amount_inside(self,shape):
    return int(self.width / shape.width) * int(self.height / shape.height)

  def __str__(self) -> str:
    return f"Rectangle(width={self.width}, height={self.height})"


class Square(Rectangle):
  def __init__(self, side) -> None:
    super().__init__(side, side)
    self.side = side

  # overloaded functions
  def set_width(self, side):
    self.width = side
    self.height = side
    self.side = side

  def set_heigth(self, side):
    self.height = side
    self.width = side
    self.side = side

  # own functions
  def set_side(self, side):
    self.height = side
    self.width = side
    self.side = side

  def __str__(self) -> str:
    return f"Square(side={self.side})"
