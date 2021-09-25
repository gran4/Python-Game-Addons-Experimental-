import arcade

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class PlayerSprite(arcade.Sprite):
    def __init__(self,
                 scale:int=1,
                 center_x:float=0,
                 center_y:float=0):
        super().__init__("Sprites/Player.png", center_x=center_x, center_y=center_y, scale=scale)
        self.textures = load_texture_pair("Sprites/Player.png")
        self.texture = self.textures[0]
        self.health = 100
        self.x = center_x
        self.y = center_y 
    
    #change directions
    def pymunk_moved(self, physics_engine, dx:float, dy:float, d_angle):
        if dx > 0.25:
            self.texture = self.textures[0]
        elif dx < -0.25:
            self.texture = self.textures[1]

        
    