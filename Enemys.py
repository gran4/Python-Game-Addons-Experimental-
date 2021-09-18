import arcade


class EnemyManager(object):
    def __init__(self):
        self.Enemys = []

    def AddEnemy(self, x, y):
        self.Enemys.append(Enemy(x, y))
    
    def AddRangedEnemy(self, x, y):
        self.Enemys.append(RangedEnemy(x, y))

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Land(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.load_texture("land.png")
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points
        


class Enemy(arcade.Sprite):
    def __init__(self, x, y, ):
        super().__init__()
        self.texture = arcade.load_texture("Vampire.png")
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points
        self.dir = True
        self.health = 10



class RangedEnemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
    
    def Fire(self, x, y):
        Bullet(x, y)
    
    def HandleCollision():
        pass

class Bullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def Update(self):
        self.x = x

def MoveTowards(x, y, x2, y2):
    val = abs()
    return val