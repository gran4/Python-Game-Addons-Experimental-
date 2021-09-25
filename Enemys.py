import arcade


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

        

class Vampire(arcade.Sprite):
    def __init__(self, x:float, y:float):
        super().__init__("Sprites/Vampire.png", center_x=x, center_y=y, scale=1)
        self.texture = arcade.load_texture("Sprites/Vampire.png")
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points
        self.health = 10


class Maggot(arcade.Sprite):
    def __init__(self, x:float, y:float):
        super().__init__("Sprites/Maggot.png", center_x=x, center_y=y, scale=2)
        self.textures = load_texture_pair("Sprites/Maggot.png")
        self.texture = self.textures[1]
        #which direction
        self.i = 1

        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points
        self.health = 10
        self.change_x = 100
    def change_texture(self):
        if self.i == 0: 
            self.i = 1
        else: 
            self.i = 0
        self.texture = self.textures[self.i]

class Turret(arcade.Sprite):
    def __init__(self, x:float, y:float, rotated:int=1):
        super().__init__("Sprites/Turret.png", center_x=x, center_y=y, scale=2)
        self.texture = arcade.load_texture("Sprites/Turret.png")
        
        #defualts to up angle
        self.flipped_diagonally = False
        self.flipped_vertically = False
        self.flipped_horizontally = False


        self.center_x = x
        self.center_y = y

        #The way the turret is turned
        self.rotated = rotated
        self.updateAngle()


        #used to spawn Bullet by giving point to shoot at
        self.change_x = x
        self.change_y = y

        self.bulletAim()

    
    #specifies where to aim using x, y values 
    def bulletAim(self):
        #aims left
        if self.rotated == 1:
            self.change_x -= 10
        #aims down
        elif self.rotated == 2:
            self.change_y -= 10
        #aims right
        elif self.rotated == 3:
            self.change_x += 10
        
        #aims up
        elif self.rotated == 4:
            self.change_y += 10

    #used to change direction in world editor
    def updateAngle(self):
        #up to left
        if self.rotated == 1:
            self.flipped_diagonally = True
        #left to down
        elif self.rotated == 2:
            self.flipped_diagonally = False
            self.flipped_vertically = True
        #down to right
        elif self.rotated == 3:
            self.flipped_horizontally = True
            self.flipped_diagonally = True
        #right to up
        elif self.rotated == 4:
            self.flipped_diagonally = False
            self.flipped_vertically = False
            self.flipped_horizontally = False
        self.texture = arcade.load_texture("Sprites/Turret.png", 
        flipped_vertically=self.flipped_vertically, 
        flipped_diagonally=self.flipped_diagonally, 
        flipped_horizontally=self.flipped_horizontally)
        self.hit_box = self.texture.hit_box_points
        #flipped_vertically, flipped_diagonally, and flipped_horizontally
        #specify direction