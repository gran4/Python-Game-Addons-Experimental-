import arcade

class CustomText(object):
    def __init__(self, x:float, y:float, text:str, size:int, color=arcade.color.BLACK, rotated:int=1):
        self.y = y
        self.x = x
        self.text = text
        self.size = size
        self.color = color
    
        self.rotated = rotated
        self.rotation = 0
        self.change()

    #used to change direction in world editor
    def change(self):
        #up to left
        if self.rotated == 1:
            self.rotation = 0
        #left to down
        elif self.rotated == 2:
            self.rotation = 90
        #down to right
        elif self.rotated == 3:
            self.rotation = 180
        #right to up
        elif self.rotated == 4:
            self.rotation = 270

class Land(arcade.Sprite):
    def __init__(self, x:float, y:float):
        super().__init__()
        self.texture = arcade.load_texture("Sprites/land.png")
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points

class SpringBoard(arcade.Sprite):
    def __init__(self, x:float, y:float, impulse:list=[0, 1000], rotated:int=4):
        super().__init__()
        self.texture = arcade.load_texture("Sprites/SpringBoard.png")
        self.center_x = x
        self.center_y = y
        self.flipped_diagonally = False
        self.flipped_vertically = False
        self.flipped_horizontally = False
        self.rotated = rotated
        self.hit_box = self.texture.hit_box_points
        self.impulse = impulse
        self.updateAngle()
        self.impulseAim()

    def impulseAim(self):
        #aims left
        if self.rotated == 1:
            self.impulse[0] = -1000
        #aims down
        elif self.rotated == 2:
            self.impulse[1] = -1000
        #aims right
        elif self.rotated == 3:
            self.impulse[0] = 1000
        
        #aims up
        elif self.rotated == 4:
            self.impulse[1] = 1000

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
        self.texture = arcade.load_texture("Sprites/SpringBoard.png", 
        flipped_vertically=self.flipped_vertically, 
        flipped_diagonally=self.flipped_diagonally, 
        flipped_horizontally=self.flipped_horizontally)
        self.hit_box = self.texture.hit_box_points


class Bullet(arcade.Sprite):
    def __init__(self,
                 scale:int=1,
                 center_x:float=0,
                 center_y:float=0, 
                 damage:float = 1):
        super().__init__("Sprites/Bullet.png", center_x=center_x, center_y=center_y, scale=scale)
        self.texture = arcade.load_texture("Sprites/Bullet.png")
        self.damage = damage

    #Handle collisions
    def wall_hit_handler(self, bullet_sprite:arcade.Sprite, _wall_sprite:arcade.Sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()

    def vampire_hit_handler(self, bullet_sprite:arcade.Sprite, _vampire_sprite:arcade.Sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _vampire_sprite.health -= self.damage
        if _vampire_sprite.health <= 0:
            _vampire_sprite.remove_from_sprite_lists()
        bullet_sprite.remove_from_sprite_lists()

    def maggot_hit_handler(self, bullet_sprite:arcade.Sprite, _maggot_sprite:arcade.Sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _maggot_sprite.health -= self.damage
        if _maggot_sprite.health <= 0:
            _maggot_sprite.remove_from_sprite_lists()
        bullet_sprite.remove_from_sprite_lists()

    def player_hit_handler(self, bullet_sprite:arcade.Sprite, _player_sprite:arcade.Sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _player_sprite.health -= self.damage
        bullet_sprite.remove_from_sprite_lists()

    def bullet_hit_handler(self, bullet_sprite:arcade.Sprite, _bullet_sprite:arcade.Sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _bullet_sprite.remove_from_sprite_lists()
        bullet_sprite.remove_from_sprite_lists()

    def pymunk_moved(self, physics_engine, dx:float, dy:float, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class healUps(arcade.Sprite):
    def __init__(self,
                 scale:int=.5,
                 center_x:float=0,
                 center_y:float=0, 
                 heal:float = 1):
        super().__init__("Sprites/Heal.png", center_x=center_x, center_y=center_y, scale=.5)
        self.texture = arcade.load_texture("Sprites/Heal.png")
        self.hit_box = self.texture.hit_box_points
        self.heal = heal

    #Handle Collision
    def player_hit_handler(self, heal_sprite:arcade.Sprite, _player_sprite:arcade.Sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _player_sprite.health += self.heal
        heal_sprite.remove_from_sprite_lists()

