import arcade, json, math
from Enemys import Vampire, Maggot, Turret
from Player import PlayerSprite
from CustomClasses import CustomText, Land, Bullet, SpringBoard, healUps

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(750, 500, "SCREEN_TITLE")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        

    #Creates Land and adds hitbox
    def addLand(self, x:float, y:float):
        land = Land(x, y)
        land.hit_box = land.texture.hit_box_points
        self.Lands.append(land)

    def addCoin(self, x:float, y:float):
        coin = arcade.Sprite("Sprites/coin.png", 1)
        coin.center_x = x
        coin.center_y = y
        coin.hit_box = coin.texture.hit_box_points
        self.Coins.append(coin)

    def addHeal(self, x:float, y:float, heal):
        Healup = healUps(center_x=x, center_y=y, heal=heal)
        self.Healups.append(Healup)#[print(heal) for heal in self.Healups]
        self.physics_engine.add_collision_handler("heal", "player", post_handler=Healup.player_hit_handler)
    def addSpringBoard(self, x:float, y:float, impulse:list=[0, 0], rotated:int=4):
        Springboard = SpringBoard(x, y, impulse=impulse, rotated=rotated)
        self.SpringBoards.append(Springboard)#[print(heal) for heal in self.Healups]
        self.physics_engine.add_collision_handler("spring", "player", post_handler=self.addPlayerImpulse)
    #Creates Enemy and adds hitbox
    def addVampire(self, x:float, y:float):
        enemy = Vampire(x, y)
        enemy.hit_box = enemy.texture.hit_box_points
        self.Vampires.append(enemy)

    def addMaggot(self, x:float, y:float):
        enemy = Maggot(x, y)
        enemy.hit_box = enemy.texture.hit_box_points
        self.Maggots.append(enemy)

    def addTurret(self, x:float, y:float, rotated):
        enemy = Turret(x, y, rotated=rotated)
        enemy.hit_box = enemy.texture.hit_box_points
        self.Turrets.append(enemy)

    #call to start/restart game
    def setup(self):
        self.physics_engine = None
        self.camera = None
        self.player = None
        self.gravity =(0, -4000)
        
        #sprite lists
        self.Lands = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Vampires = arcade.SpriteList()
        self.Maggots = arcade.SpriteList()
        self.Coins = arcade.SpriteList()
        self.Turrets = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Bullets = arcade.SpriteList()
        self.Healups = arcade.SpriteList()
        self.SpringBoards = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Texts = []

        #springs
        self.playerImpulive = []

        #time until next turret update
        self.Turrettime = 0

        #coyote time
        self.SinceOnGround = .1

        #When allowed to jump
        #self.SinceJump = 1
        
        #controlls
        self.left_pressed = False
        self.right_pressed = False
        self.jump = False

        #splits jump for smooth animation and better collision detection
        self.jumpindex = 0



        self.camera = arcade.Camera(self.width, self.height)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=.5, gravity=(self.gravity))

        #loads saved world
        self.load()

        #add physics to objects in game
        self.physics_engine.add_sprite(sprite=self.player, friction=1.0, mass=2.0, gravity=self.gravity, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="player", max_horizontal_velocity=450, max_vertical_velocity=1600)
        self.physics_engine.add_sprite_list(sprite_list=self.Lands, friction=1.0, collision_type="wall", body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(sprite_list=self.SpringBoards, friction=1.0, collision_type="spring", body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(sprite_list=self.Vampires, friction=1.0, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="vampire")
        self.physics_engine.add_sprite_list(sprite_list=self.Coins, friction=1.0, moment=arcade.PymunkPhysicsEngine.DYNAMIC, collision_type="coin")
        self.physics_engine.add_sprite_list(sprite_list=self.Healups, friction=1.0, collision_type="heal")
        self.physics_engine.add_sprite_list(sprite_list=self.Turrets, friction=1.0, collision_type="turret", body_type=arcade.PymunkPhysicsEngine.STATIC)

    #loads actual world/level
    def load(self):
        with open("WorldFile.json", "r") as read_file:
            World = json.load(read_file)

        #values in list in list in dict
        #Retrieve value's from dict and restores them as objects

        #create player
        if World["player"] is not None:
            self.player = PlayerSprite(1, World["player"][0], World["player"][1])
        else:
            self.player = PlayerSprite(1, 500, 500)

        #create tiles
        for land in World["land"]:
            self.addLand(land[0], land[1])

        #create enemys
        for turret in World["turret"]:
            self.addTurret(turret[0], turret[1], turret[2])
        for vampire in World["vampire"]:
            self.addVampire(vampire[0], vampire[1])
        for maggot in World["maggot"]:
            self.addMaggot(maggot[0], maggot[1])
        for heal in World["heal"]:
            self.addHeal(heal[0], heal[1], heal=heal[2])
        for springboard in World["springBoards"]:
            self.addSpringBoard(springboard[0], springboard[1], springboard[2], springboard[3])
        for text in World["text"]:
            self.Texts.append(CustomText(text[0], text[1], text[2]))
        
   
    def on_draw(self):
        """Render the screen."""
        #arcade.start_render() clears screen
        arcade.start_render()
        self.camera.use()

        #tiles
        self.Lands.draw()
        self.SpringBoards.draw()
        
        #player
        self.player.draw()

        #enemies
        self.Turrets.draw()
        self.Vampires.draw()
        self.Maggots.draw()

        #projectiles
        self.Bullets.draw()

        #power ups
        self.Healups.draw()
        
        #Text
        [arcade.draw_text(Text.text, Text.x, Text.y, color=Text.color, rotation=Text.rotation) for Text in self.Texts]
        

    def on_key_press(self, key:int, modifiers):
        """Called whenever a key is pressed. """

        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            
            self.jumpindex = 3
            self.jump = True

    def on_key_release(self, key:int, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.SpawnBullet(x, y, 10000, self.player, isPlayer=True, bullet_gravity=(0, -250))
    
    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def on_update(self, delta_time:float):
        """Movement and game logic"""

        
        self.UpdatePlayer() 
        self.generalUpdate(delta_time)

        is_on_ground = self.physics_engine.is_on_ground(self.player)
        if is_on_ground:
            self.SinceOnGround = .2
        elif not is_on_ground:
            self.SinceOnGround -= delta_time
        if self.jump and self.SinceOnGround > 0: 
            self.Jump()
        

        self.physics_engine.step(delta_time=delta_time)
        self.center_camera_to_player()
    

    # Move the player with the physics engine
    # Update player forces based on keys pressed
    def UpdatePlayer(self):
        is_on_ground = self.physics_engine.is_on_ground(self.player)
                
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

        if self.player.health <= 0: self.setup()
        self.UpdatePlayerImpulse()


    #updates everything except player
    def generalUpdate(self, delta_time:float):
        #updates maggots
        for maggot in self.Maggots:
            #change position
            maggot.center_x += maggot.change_x*delta_time

            #check for collision
            walls_hit = arcade.check_for_collision_with_list(sprite=maggot, sprite_list=self.Lands)
            if arcade.check_for_collision(maggot, self.player): self.player.health -= .05
            
            #changes direction if collides by making it move in the opposite direction
            if walls_hit:
                maggot.change_x *= -1
                maggot.center_x += maggot.change_x*delta_time
                #flips texture
                maggot.change_texture()

        self.Turrettime += delta_time
        if self.Turrettime >= 1.5:
            #uses SpawnBullet() to spawn bullets
            [self.SpawnBullet(turret.change_x, turret.change_y, 1000, turret) for turret in self.Turrets]
            self.Turrettime = 0

    #makes the player jump
    #splits jump for smooth animation and better collision detection
    def Jump(self):
        if self.jumpindex == 0:
            self.jump = False
        self.jumpindex -= 1
        self.physics_engine.apply_impulse(self.player, (0, 750))
    def addPlayerImpulse(self, spring_sprite:arcade.Sprite, _player_sprite:arcade.Sprite, _arbiter, _space, _data):
        self.playerImpulive.append([spring_sprite.impulse, 8])
    def UpdatePlayerImpulse(self):
        for impulse in self.playerImpulive:
            if impulse[1] != 7 or 8:
                self.physics_engine.apply_impulse(self.player, impulse[0])#impulse[0]
                if impulse[1] == 0:
                    self.playerImpulive.remove(impulse)
            impulse[1] -= 1
            print(impulse[1])


    def SpawnBullet(self, x:float, y:float, BulletForce:int, object, isPlayer:bool=False, scale:int=2, bullet_gravity:tuple= (0, 0)):

        #create bullet with initial values
        bullet = Bullet(scale, 0, 0)
        self.Bullets.append(bullet)
        bullet.position = object.position


        if isPlayer:
            #gets center of screen
            x_diff = x - (self.camera.viewport_width / 2)
            y_diff = y - (self.camera.viewport_height / 2)

            # What is the 1/2 size of this sprite, so we can figure out how far
            # away to spawn the bullet
            size = max(object.width, object.height)/2

        else:
            #gets center of screen
            x_diff = x-object.center_x
            y_diff = y-object.center_y

            # What is the 1/2 size of this sprite, so we can figure out how far
            # away to spawn the bullet
            size = max(object.width, object.height)*2

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.

        angle = math.atan2(y_diff, x_diff)


        # Use angle to to spawn bullet away from player in proper direction
        bullet.center_x += size * math.cos(angle)
        bullet.center_y += size * math.sin(angle)

        # Set angle of bullet
        bullet.angle = math.degrees(angle)


        # Gravity to use for the bullet
        # If we don't use custom gravity, bullet drops too fast, or we have
        # to make it go too fast.
        # Force is in relation to bullet's angle.

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.physics_engine.add_sprite(bullet,
                                       mass=.1,
                                       damping=1,
                                       friction=0.6,
                                       collision_type="bullet",
                                       gravity=bullet_gravity,
                                       elasticity=0.9)

        #adds collision hadlers which define which calls function on collision
        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=bullet.wall_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "vampire", post_handler=bullet.vampire_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "maggot", post_handler=bullet.maggot_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "player", post_handler=bullet.player_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "bullet", post_handler=bullet.bullet_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "heal", post_handler=bullet.wall_hit_handler)

        # Add force to bullet
        force = (BulletForce, 0)
        self.physics_engine.apply_force(bullet, force)



def main():
    """Main method"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
