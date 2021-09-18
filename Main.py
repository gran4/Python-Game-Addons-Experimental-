import arcade
import json
import math
from Enemys import Land, Enemy
from Player import PlayerSprite, Bullet


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, gravity):

        # Call the parent class and set up the window
        super().__init__(750, 500, "SCREEN_TITLE")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.physics_engine = None
        self.camera = None
        self.player = None
        self.gravity = gravity
        
        #sprite lists
        self.Lands = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Enemys = arcade.SpriteList()
        self.Bullets = arcade.SpriteList()
        
        #controlls
        self.left_pressed = False
        self.right_pressed = False
        self.jump = False


        self.camera = arcade.Camera(self.width, self.height)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=.5, gravity=self.gravity)

    #Creates Land and adds hitbox
    def addLand(self, x, y):
        land = Land(x, y)
        land.hit_box = land.texture.hit_box_points
        self.Lands.append(land)
    #Creates Enemy and adds hitbox
    def addEnemy(self, x, y):
        enemy = Enemy(x, y)
        enemy.hit_box = enemy.texture.hit_box_points
        self.Enemys.append(enemy)
        self.barrier_list = arcade.AStarBarrierList(enemy,
                                                    self.Lands,
                                                    100, -1000,
                                                    1000, -1000, 1000,)
        enemy.path = arcade.astar_calculate_path(enemy.position,
                                                self.player.position,
                                                self.Lands,
                                                diagonal_movement=False)

    def setup(self):

        self.load()

        #add physics to objects in game
        self.physics_engine.add_sprite(sprite=self.player, friction=1.0, mass=2.0, gravity=self.gravity, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="player", max_horizontal_velocity=450, max_vertical_velocity=1600)

        self.physics_engine.add_sprite_list(sprite_list=self.Lands, friction=1.0, collision_type="wall", body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(sprite_list=self.Enemys, friction=1.0, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="enemy")


    def load(self):
        with open("WorldFile.json", "r") as read_file:
            World = json.load(read_file)
        #Retrieve value's from dict and restores them as objects

        #create player
        if World["player"] is not None:
            self.player = PlayerSprite(1, World["player"][0], World["player"][1])
        else:
            self.player = PlayerSprite(1, 500, 500)

        #create tiles
        for cord in World["land"]:
            self.Lands.append(Land(cord[0], cord[1]))
        #create enemys
        for cord in World["enemy"]:
            self.addEnemy(cord[0], cord[1])
        
   
    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        self.camera.use()

        self.Lands.draw()
        self.player.draw()
        for enemy in self.Enemys:
            self.EnemyMove(enemy.center_x, enemy.center_y, enemy.dir)

        #[enemy.update() for enemy in self.Enemys]
        self.Enemys.draw()
        self.Bullets.draw()
        print(len(self.Bullets))
        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            is_on_ground = self.physics_engine.is_on_ground(self.player)
            if is_on_ground:
                self.jumpindex = 5
                self.jump = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.SpawnBullet(x, y, 10000)
    
    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )
        
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine

        # Update player forces based on keys pressed
        is_on_ground = self.physics_engine.is_on_ground(self.player)
        # Update player forces based on keys pressed
                
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            if is_on_ground:
                force = (-8000, 0)
            else:
                force = (-900, 0)
            self.physics_engine.apply_force(self.player, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            if is_on_ground:
                force = (8000, 0)
            else:
                force = (900, 0)
            self.physics_engine.apply_force(self.player, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player, 0)
        else:
            self.physics_engine.set_friction(self.player, 1.0)
        if self.jump:
            self.Jump()  

        self.physics_engine.step(delta_time=delta_time)
        self.center_camera_to_player()

    def Jump(self):
        if self.jumpindex == 0:
            self.jump = False
        self.jumpindex -= 1
        self.physics_engine.apply_impulse(self.player, (0, 500))

    def EnemyMove(self, x, y, tf):
        if tf:
            x += 5
            if len(arcade.get_sprites_at_point((x+10, y), self.Lands)):
                tf = False
        else:
            x -= 5
            if len(arcade.get_sprites_at_point((x-10, y), self.Lands)):
                tf = True

    def SpawnBullet(self, x, y, BulletForce):

        bullet = Bullet(2, 0, 0)
        self.Bullets.append(bullet)

        bullet.position = self.player.position

        # Get from the mouse the destination location for the bullet

        # Position the bullet at the player's current location(center of screen)
        x_diff = x - (self.camera.viewport_width / 2)
        y_diff = y - (self.camera.viewport_height / 2)

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.

        angle = math.atan2(y_diff, x_diff)

        # What is the 1/2 size of this sprite, so we can figure out how far
        # away to spawn the bullet
        size = max(self.player.width, self.player.height) / 2

        # Use angle to to spawn bullet away from player in proper direction
        bullet.center_x += size * math.cos(angle)
        bullet.center_y += size * math.sin(angle)

        # Set angle of bullet
        bullet.angle = math.degrees(angle)


        # Gravity to use for the bullet
        # If we don't use custom gravity, bullet drops too fast, or we have
        # to make it go too fast.
        # Force is in relation to bullet's angle.
        bullet_gravity = (0, -250)

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.physics_engine.add_sprite(bullet,
                                       mass=.1,
                                       damping=.99,
                                       friction=0.6,
                                       collision_type="bullet",
                                       gravity=bullet_gravity,
                                       elasticity=0.9)
        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=bullet.wall_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "enemy", post_handler=bullet.enemy_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "player", post_handler=bullet.player_hit_handler)

        # Add force to bullet
        force = (BulletForce, 0)
        self.physics_engine.apply_force(bullet, force)


def main():
    """Main method"""
    window = MyGame((0, -4000))
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
