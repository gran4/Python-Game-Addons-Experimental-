import arcade
import json
from Player import PlayerSprite
from Enemys import Land, Enemy
  
class MyEditor(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        #create sprite lists
        #also nothing should move/have gravity so don't 
        #change use_spatial_hash or is_static(objects like tiles are to be
        #deleted instead of moved for simplicity) only the player will move.
        self.Lands = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Enemys = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        
        #to localize mouse position
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0

        #Check what to keys are pressed(Bypass the if extra variables)
        self.num = 0
        self.numlist = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
        self.key = 108
        self.keylist = [108, 101]


        self.camera = arcade.Camera(self.width, self.height)
        self.load()

    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        self.camera.use()
        self.Lands.draw()
        self.player.draw()
        self.Enemys.draw()

    def on_key_press(self, key: int, modifiers: int):
        #move camera
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.x -= 50
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.x += 50
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.y -= 50
        elif key == arcade.key.UP or key == arcade.key.W:
            self.y += 50
        #save and quite
        elif key == arcade.key.Q:
            self.save()
            arcade.close_window()
        #checks if number or key is pressed
        elif key in self.numlist:
            self.num = key
        elif key in self.keylist:
            self.key = key
        
    def on_update(self, delta_time: float):
        self.camera.move_to((self.x, self.y))

    def load(self):
        with open("WorldFile.json", "r") as read_file:
            World = json.load(read_file)

        #Retrieve value's from dict and restores them as objects

        #create tiles
        for cord in World["land"]:
            self.Lands.append(Land(cord[0], cord[1]))
        #create enemys
        for cord in World["enemy"]:
            self.Enemys.append(Enemy(cord[0], cord[1]))
        #create player
        if World["player"] is not None:
            self.player = PlayerSprite(1, World["player"][0], World["player"][1])
        else:
            self.player = PlayerSprite(1, 500, 500)

    #saves values of objects since json doesn't support object saving
    def save(self):
        with open("WorldFile.json", "w") as write_file:
            #saves using list comprehension to save value's in a tuple
            cords = [(land.center_x, land.center_y) for land in self.Lands]
            Enemy_cords = [(enemy.center_x, enemy.center_y) for enemy in self.Enemys]
            player_cords = int(self.player.center_x), int(self.player.center_y)


            #Stores each list of value's in a dict to make it easy to retrieve
            json.dump({"land":cords, "enemy":Enemy_cords, "player":player_cords}, write_file)


    #Where is it pressed
    def on_mouse_press(self, x, y, button, modifiers):
        #all calculations in on_mouse_press are to round until
        #AddObj function
        start_x = self.x
        start_y = self.y

        x += start_x
        y += start_y


        x = x/50
        x = round(x)
        x *= 50

        y = y/50
        y = round(y)
        y *= 50

        if button == arcade.MOUSE_BUTTON_LEFT:

            #AddObj function checks and sets object
            self.AddObj(x, y)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            [land.remove_from_sprite_lists() for land in self.Lands if land.center_x == x and land.center_y == y]
            [enemy.remove_from_sprite_lists() for enemy in self.Enemys if enemy.center_x == x and enemy.center_y == y]

    def AddObj(self, x, y):
        #check value's if they match 
        #REMEMBER When Adding add to num and key lists
        #This is my garbage work around to writing
        #if statements for each Key

        if self.num == self.numlist[0]:#if num == 1: basicly
            self.player.center_x = x
            self.player.center_y = y
        elif self.num == self.numlist[1]:#if num == 2: basicly
            if self.key == arcade.key.L:#if key == L: basicly
                self.Lands.append(Land(x, y))
        elif self.num == self.numlist[2]:
            if self.key == arcade.key.E:
                self.Enemys.append(Enemy(x, y))

        print(self.num, self.key, arcade.key.L)
        
        
Editor = MyEditor(1000, 1000, "MyEditor")
arcade.run()