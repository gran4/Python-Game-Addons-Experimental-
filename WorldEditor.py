import arcade
import json
from Player import PlayerSprite
from Enemys import Vampire, Maggot, Turret
from CustomClasses import CustomText, Land, SpringBoard, healUps

    
class MyEditor(arcade.Window):
    """ Main application class. """

    def __init__(self, width:int, height:int, title:str):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.title = title
        self.add = True
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        #create sprite lists
        #also nothing should move/have gravity so don't 
        #change use_spatial_hash or is_static(objects like tiles are to be
        #deleted instead of moved for simplicity) only the player will move.
        self.Lands = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.SpringBoards = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Vampires = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Maggots = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Turrets = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Healups = arcade.SpriteList(use_spatial_hash=True, is_static=True)

        #list of texts
        self.Texts = []

        #Power Ups
        self.heals = []
        
        #to localize mouse position
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0

        #last object rotatable is saved as self.last
        self.last = None

        #Check what to keys are pressed(Bypass the if extra variables)

        #current num
        self.num = 0
        #list of numbers 1-9 
        self.numlist = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58]

        #current key being pressed
        self.key = 108
        
        #list keys that can be pressed
        self.keylist = [108, 101, 118, 109, 116, 104, 115]


        self.camera = arcade.Camera(self.width, self.height)
        self.load()

        self.textBox = arcade.Sprite(filename="Sprites/Box.png", center_x=500, center_y=100, scale=1)

    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        self.camera.use()

        self.Lands.draw()
        self.SpringBoards.draw()

        self.player.draw()

        self.Turrets.draw()
        self.Vampires.draw()
        self.Maggots.draw()

        self.Healups.draw()

        [arcade.draw_text(Text.text, Text.x, Text.y, color=Text.color, rotation=Text.rotation) for Text in self.Texts]  
        self.textBox.center_x = 50+self.x
        self.textBox.center_y = 250+self.y
        self.textBox.draw()

    def on_key_press(self, key: int, modifiers: int):
        #move camera
        if key == arcade.key.LEFT:
            self.x -= 50
        elif key == arcade.key.RIGHT:
            self.x += 50
        elif key == arcade.key.DOWN:
            self.y -= 50
        elif key == arcade.key.UP:
            self.y += 50

        #flips last item rotatable(stored as self.last)
        elif key == arcade.key.E:
            self.last.rotated += 1
            if self.last.rotated == 5:
                self.last.rotated = 1
            #update changes on sprite
            self.last.updateAngle()
        #save and quit
        elif key == arcade.key.Q:
            self.save()
            arcade.close_window()
        elif key == arcade.key.DELETE:
            if type(self.last) == CustomText:
                self.last.text[:-1]

        #checks if number or key is pressed
        elif key in self.numlist:
            self.num = key
        elif key in self.keylist:
            self.key = key
        
    def on_update(self, delta_time: float):
        #centers camera on position
        self.camera.move_to((self.x, self.y))

    def load(self):
        with open("WorldFile.json", "r") as read_file:
            World = json.load(read_file)

        #Retrieve value's from dict and restores them as objects

        #create tiles
        for land in World["land"]:
            self.Lands.append(Land(land[0], land[1]))

        #create enemys
        for turret in World["turret"]:
            self.Turrets.append(Turret(turret[0], turret[1], rotated=turret[2]))
        for vampire in World["vampire"]:
            self.Vampires.append(Vampire(vampire[0], vampire[1]))
        for maggot in World["maggot"]:
            self.Maggots.append(Maggot(maggot[0], maggot[1]))
        for heal in World["heal"]:
            self.Healups.append(healUps(center_x=heal[0], center_y=heal[1]))
        for springboard in World["springBoards"]:
            self.SpringBoards.append(SpringBoard(springboard[0], springboard[1], impulse=springboard[2], rotated=springboard[3]))
        for text in World["text"]:
            self.Texts.append(CustomText(text[0], text[1], text[2]))

        #create player
        if World["player"] is not None:
            self.player = PlayerSprite(1, World["player"][0], World["player"][1])
        else:
            self.player = PlayerSprite(1, 500, 500)

    #saves values of objects since json doesn't support object saving
    def save(self):
        with open("WorldFile.json", "w") as write_file:
            #saves values using list comprehension makes a list of values in tuples:
            #[(values), (values), (values)]
            cords = [(land.center_x, land.center_y) for land in self.Lands]
            Turret_cords = [(turret.center_x, turret.center_y, turret.rotated) for turret in self.Turrets]
            Vampire_cords = [(vampire.center_x, vampire.center_y) for vampire in self.Vampires]
            Maggot_cords = [(maggot.center_x, maggot.center_y) for maggot in self.Maggots]
            Heal_cords = [(heal.center_x, heal.center_y, heal.heal) for heal in self.Healups]
            SpringBoardCords = [(spring.center_x, spring.center_y, spring.impulse, spring.rotated) for spring in self.SpringBoards]
            Text_cords = [(Text.center_x, Text.center_y, Text.rotated) for Text in self.Texts]
            
            #tuple of values
            player_cords = int(self.player.center_x), int(self.player.center_y)


            #Stores each list of value's in a dict to make it easy to retrieve1
            json.dump({"land":cords, "turret":Turret_cords, "vampire":Vampire_cords, "player":player_cords, "maggot":Maggot_cords, "heal":Heal_cords, "springBoards":SpringBoardCords, "text":Text_cords}, write_file)


    #Where is it pressed
    def on_mouse_press(self, x:float, y:float, button, modifiers):
        #creates tile like affect
        x += self.x
        y += self.y

        x = x/50
        x = round(x)
        x *= 50

        y = y/50
        y = round(y)
        y *= 50

        #adds object to world
        if button == arcade.MOUSE_BUTTON_LEFT:
            if type(self.last) == CustomText:
                if self.textBox.center_x == x and self.textBox.center_y == y:
                    self.last.text = input("Text: ")
            elif type(self.last) == healUps:
                if self.textBox.center_x == x and self.textBox.center_y == y:
                    self.last.text = input("Health: ")
            [self.change(land) for land in self.Lands if land.center_x == x and land.center_y == y]
            [self.change(vampire) for vampire in self.Vampires if vampire.center_x == x and vampire.center_y == y]
            [self.change(maggot) for maggot in self.Maggots if maggot.center_x == x and maggot.center_y == y]
            [self.change(turret) for turret in self.Turrets if turret.center_x == x and turret.center_y == y]
            [self.change(heal) for heal in self.Healups if heal.center_x == x and heal.center_y == y]
            [self.change(spring) for spring in self.SpringBoards if spring.center_x == x and spring.center_y == y]
            [self.change(text) for text in self.Texts if text.x == x and text.y == y]
            if self.add:
                #AddObj function checks and sets object
                self.AddObj(x, y)
            elif not self.add:
                pass
            else:
                raise TypeError("self.add is not a bool")


        #deletes object if object is right clicked on
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            [land.remove_from_sprite_lists() for land in self.Lands if land.center_x == x and land.center_y == y]
            [vampire.remove_from_sprite_lists() for vampire in self.Vampires if vampire.center_x == x and vampire.center_y == y]
            [maggot.remove_from_sprite_lists() for maggot in self.Maggots if maggot.center_x == x and maggot.center_y == y]                
            [turret.remove_from_sprite_lists() for turret in self.Turrets if turret.center_x == x and turret.center_y == y]
            [heal.remove_from_sprite_lists() for heal in self.Healups if heal.center_x == x and heal.center_y == y]
            [spring.remove_from_sprite_lists() for spring in self.SpringBoards if spring.center_x == x and spring.center_y == y]
            [self.Texts.remove(text) for text in self.Texts if text.x == x and text.y == y]
    def change(self, obj):
        self.add = False
        self.last = obj


        # if type(self.last) == Land:
        #     changeDict = {"rotation_type":1}
        # elif type(self.last) == Maggot:
        #     changeDict = {"direction":True, "speed":1}
        # elif type(self.last) == Turret:
        #     changeDict = {"bullet_speed":1}
        # elif type(self.last) == CustomText:
        #     changeDict = {"rotation_type":2, }

        #return changeDict
    
    def AddObj(self, x:float, y:float):
        #check value's if they match 
        #REMEMBER When Adding add to num and key lists
        #This is my garbage work around to writing if statements for each Key

        #move player
        if self.num == self.numlist[0]:#if num == 1: basicly
            self.player.center_x = x
            self.player.center_y = y

        #tiles, crates, spring boards, items in world
        elif self.num == self.numlist[1]:#if num == 2: basicly
            if self.key == arcade.key.L:#if key == L: basicly
                self.Lands.append(Land(x, y))
            elif self.key == arcade.key.S:
                self.last = SpringBoard(x, y)
                self.SpringBoards.append(self.last)

        #enemies
        elif self.num == self.numlist[2]:
            if self.key == arcade.key.T:
                self.last = Turret(x, y)
                self.Turrets.append(self.last)
            elif self.key == arcade.key.V:
                self.Vampires.append(Vampire(x, y))
            elif self.key == arcade.key.M:
                self.Maggots.append(Maggot(x, y))
        elif self.num == self.numlist[3]:
            self.last = CustomText(x, y, "Big Bio", 12)
            self.Texts.append(self.last)
        elif self.num == self.numlist[4]:
            if self.key == arcade.key.H:
                self.last = healUps(center_x=x, center_y=y)
                self.Healups.append(self.last)
#Bonn Hoffer
        
        
Editor = MyEditor(1000, 1000, "MyEditor")
arcade.run()