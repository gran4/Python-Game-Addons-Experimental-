import arcade
import pymunk
import math

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

# class Player(arcade.Sprite):
#     def __init__(self,
#                  scale=1,
#                  center_x=0,
#                  center_y=0, 
#                  mass: float = 2,
#                  moment: float = 0,
#                  body_type=pymunk.Body.DYNAMIC,
#                  friction: float = .5,
#                  collision_type: int = 0,
#                  shape: pymunk.Shape = None,
#                  angle=0):
#         """The PhysicsSprite matches up to a pymunk Body as well as being an arcade Sprite."""

#         super().__init__("ball_court.jpeg", center_x=center_x, center_y=center_y, scale=scale)

#         #self.texture = arcade.load_texture("ball_court.jpeg")
#         #self._texture = arcade.load_texture("ball_court.jpeg")
#         self._width = self._texture.width * scale
#         self._height = self._texture.height * scale
#         self._angle = angle
#         self._position = center_x, center_y

#         self.body = pymunk.Body(mass, moment, body_type=body_type)
#         self.body.position = pymunk.Vec2d(center_x, center_y)
#         if shape is not None:
#             self.shape = shape
#             self.shape.body = self.body
#         else:
#             self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
#         self.shape.friction = friction
#         self.shape.collision_type = collision_type

#         #self._position.center_x = self.body.position.x
#         #self._position.center_y = self.body.position.y
#         """The player matches up to a pymunk Body as well as being an arcade Sprite."""


#     def limit_velocity(body, gravity, damping, dt):
#         pymunk.Body.update_velocity(body, gravity, damping, dt)
#         horiz_vel = body.velocity.x
#         if horiz_vel > 500:
#             body.velocity = pymunk.Vec2d(500, body.velocity.y)
#         elif horiz_vel < -500:
#             body.velocity = pymunk.Vec2d(-500, body.velocity.y)

#     def resync(self):
#         """ Resyncs the sprite to the pymunk Body """
#         self.center_x = self.body.position.x
#         self.center_y = self.body.position.y
#         print(self.body.position.x,  self.body.position.y)
#         self.angle = math.degrees(self.body.angle)




class PlayerSprite(arcade.Sprite):
    def __init__(self,
                 scale=1,
                 center_x=0,
                 center_y=0):
        super().__init__("Player.png", center_x=center_x, center_y=center_y, scale=scale)
        self.textures = load_texture_pair("Player.png")
        self.texture = self.textures[0]#arcade.load_texture("Player.png")

    def changeDir(self, i):
        self.texture = self.textures[i]
    
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx > 0.25:
            self.texture = self.textures[0]
        elif dx < -0.25:
            self.texture = self.textures[1]
class Bullet(arcade.Sprite):
    def __init__(self,
                 scale=1,
                 center_x=0,
                 center_y=0, 
                 damage = 1):
        super().__init__("Bullet.png", center_x=center_x, center_y=center_y, scale=scale)
        self.texture = arcade.load_texture("Bullet.png")
        self.damage = damage
    #collision handlers
    def wall_hit_handler(self, bullet_sprite, _wall_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()
    def enemy_hit_handler(self, bullet_sprite, _enemy_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _enemy_sprite.health -= self.damage
        if _enemy_sprite.health <= 0:
            _enemy_sprite.remove_from_sprite_lists()
        bullet_sprite.remove_from_sprite_lists()
    def player_hit_handler(self, bullet_sprite, _player_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        _player_sprite.health -= self.damage
        bullet_sprite.remove_from_sprite_lists()

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()
    