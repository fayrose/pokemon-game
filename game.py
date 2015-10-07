import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
   

WIDTH = 480
HEIGHT = 480
BORDERS = [35, 407, 59, 422]
current_background = "map"

moving_left = False
moving_right = False

class ImageInfo:
    """
    Processes image information
    """
    def __init__(self, center, size, image):
        self.center = center
        self.size = size
        self.image = image

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size
                          
    def draw(self, canvas, location):
        canvas.draw_image(self.image, self.center, self.size, location, self.size)
    
map_image = simplegui.load_image("http://i.imgur.com/xIYhInX.jpg")
map_info = ImageInfo([240, 240], [480, 480], map_image)

character_image = simplegui.load_image("http://i.imgur.com/X7rwD5S.png")
character_info = ImageInfo([32, 32], [64, 64], character_image)

pokecenter_map = simplegui.load_image("http://i.imgur.com/S55Faqx.jpg")
pkcmap_info = ImageInfo([325 / 2, 295 / 2], [325, 295], pokecenter_map)

pokemart_map = simplegui.load_image("http://i.imgur.com/CAlO95H.png")
pokemart_info = ImageInfo([352 / 2, 264 / 2], [352, 264], pokemart_map)

littleroot_theme = simplegui.load_sound("https://www.dropbox.com/s/jus36w1y0sfjukr/Littleroot.ogg?dl=1")

background_image = map_image
background_info = map_info
current_sound = littleroot_theme
current_sound.play()

#Tracks the placement of the background image for map scrolling
latitude = background_info.center[0] + background_info.size[0]

#tracks location of the character while inside a building
outside_location = [latitude, WIDTH / 2, HEIGHT / 2]

class Character:
    """
    Enables character movement and proper image display
    """
    def __init__(self, tiled_image, image_info):
        self.tiled_image = tiled_image
        self.image_info = image_info
        self.row_number = 0
        self.image_center = image_info.get_center()
        self.image_size = image_info.get_size()
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.vel = [0, 0]
        self.col = 0
        
    def walk_down(self):
            self.row_number = 0
            self.vel[1] = 1

    def walk_left(self):
        self.row_number = 1
        self.vel[0] = -1
        
    def walk_right(self):
        self.row_number = 2
        self.vel[0] = 1
        
    def walk_up(self):
        if self.pos[1] >= BORDERS[0]:
            self.row_number = 3
            self.vel[1] = -1
       
    def draw(self, canvas):
        #Ensures the proper subset of the tiled image is shown based on character direction
        canvas.draw_image(self.tiled_image, [self.image_center[0] + self.image_size[0] * self.col,
                                             self.image_center[1] + self.image_size[1] * self.row_number],
                          self.image_size,
                          self.pos, [self.image_size[0] / 1.5, self.image_size[1] / 1.5])

    def update(self):
        #Keeps track of map borders and updates character position
        """
        The map borders are hardcoded seperately from the 'Building' class because
        inversing the top and the bottom borders in the class to make up for the lack
        of box shape prevents the 'if' statements from finding longitudes at which the 
        character / moving object is BETWEEN. No choice but to hardcode.
        """
        global borders
        if self.pos[1] == BORDERS[0] or self.pos[1] == BORDERS[1]:
            self.vel[1] = 0
            if self.pos[1] == BORDERS[0]:
                self.pos[1] += 1
            elif self.pos[1] == BORDERS[1]:
                self.pos[1] -= 1
        if self.pos[0] == BORDERS[2] or self.pos[0] == BORDERS[3]:
            self.vel[1] = 0
            if self.pos[0] == BORDERS[2]:
                self.pos[0] += 1
            elif self.pos[0] == BORDERS[3]:
                self.pos[0] -= 1
                
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

class Building:
    """
    Prevents the character from walking on top of buildings, trees, etc.
    """
    def __init__(self, upper, lower, left, right, door = None, map_end = False, interactive = False, map = None, map_info = None, map_string = None):
        global character
        self.upper = upper
        self.lower = lower
        self.right = right
        self.left = left
        self.moving_object = character
        self.interactive = interactive
        self.map_end = map_end
        self.door = door
        self.map = map
        self.map_info = map_info
        self.map_string = map_string
        
    def left_border(self):
        global latitude
        if not self.map_end:
            if (latitude == self.left) and (self.moving_object.pos[1] >= self.upper and self.moving_object.pos[1] <= self.lower):
                self.moving_object.vel[0] = 0
                latitude -= 1
        else:
            if self.moving_object.pos[0] == self.left and (self.moving_object.pos[1] >= self.upper and self.moving_object.pos[1] <= self.lower):
                self.moving_object.vel[0] = 0
                self.moving_object.pos[0] -= 1
                
    def right_border(self):
        global latitude
        if not self.map_end:
            if (latitude == self.right) and (self.moving_object.pos[1] >= self.upper and self.moving_object.pos[1] <= self.lower):
                self.moving_object.vel[0] = 0
                latitude += 1
        else:
            if (self.moving_object.pos[0] == self.right) and (self.moving_object.pos[1] >= self.upper and self.moving_object.pos[1] <= self.lower):
                self.moving_object.vel[0] = 0
                self.moving_object.pos[0] += 1
                
    def upper_border(self):
        global latitude
        if not self.map_end:
            if (self.moving_object.pos[1] == self.upper) and (latitude >= self.left) and (latitude <= self.right):  
                self.moving_object.vel[1] = 0
                self.moving_object.pos[1] -= 1
        else:
            if (self.moving_object.pos[1] == self.upper) and (self.moving_object.pos[0] >= self.left) and (self.moving_object.pos[0] <= self.right):  
                self.moving_object.vel[1] = 0
                self.moving_object.pos[1] -= 1
                
    def lower_border(self):
        global latitude
        if not self.map_end:
            if (self.moving_object.pos[1] == self.lower) and (latitude >= self.left) and (latitude <= self.right):  
                self.moving_object.vel[1] = 0
                self.moving_object.pos[1] += 1
        else:
            if (self.moving_object.pos[1] == self.lower) and (self.moving_object.pos[0] >= self.left) and (self.moving_object.pos[0] <= self.right):  
                self.moving_object.vel[1] = 0
                self.moving_object.pos[1] += 1
                
    def doors(self):
        #Sets the doors of buildings to change maps
        global latitude, background_image, background_info, current_background
        if not self.map_end and self.door != None and self.interactive == False:
            if (self.moving_object.pos[1] == (self.lower + 1) or self.moving_object.pos[1] == (self.lower - 1)) and (latitude >= self.door[0]) and (latitude <= self.door[1]):  
                map_change(self.map, self.map_string, self.map_info, self.moving_object)
        
        elif self.door != None and self.interactive == False:
            if (self.moving_object.pos[1] == (self.lower + 1) or self.moving_object.pos[1] == (self.lower - 1)) and (self.moving_object.pos[0] >= self.door[0]) and (self.moving_object.pos[0] <= self.door[1]):  
                map_change(self.map, self.map_string, self.map_info, self.moving_object)
                
def border_control(building_set):
    #Recalls the four border controls in the Building Limits Class
    
    for item in building_set:
        item.left_border()
        item.right_border()
        item.lower_border()
        item.upper_border()
        item.doors()

def map_change(map, map_string, map_info, moving_object):
    #Changes the background map
    global outside_location, latitude, background_image, background_info, current_background, BORDERS
    current_background = map_string
    background_image = map
    background_info = map_info
    if map_string == "map":
        latitude = background_info.center[0] + background_info.size[0]
        if outside_location[1] == 240:
            latitude = outside_location[0]
            moving_object.pos[1] = outside_location[2]
        else:
            moving_object.pos[0] = outside_location[1]
            moving_object.pos[1] = outside_location[2]
    else:
        outside_location = [latitude, moving_object.pos[0], moving_object.pos[1]]
        moving_object.pos = [WIDTH / 2, background_info.center[1] + (HEIGHT / 2) - 20]
    
    BORDERS[0] = (HEIGHT / 2) - background_info.get_center()[1] + 80
    BORDERS[1] = background_info.get_center()[1] + (HEIGHT / 2)
    BORDERS[2] = (WIDTH / 2) - background_info.get_center()[0] + 3
    BORDERS[3] = (WIDTH / 2) + background_info.get_center()[0] - 3   
            
def key_down(key):
    #Key down handler; primarily controls movement.
    global latitude, moving_left, moving_right
    timer.start()
    if key == simplegui.KEY_MAP['left']:
        moving_left = True
    if key == simplegui.KEY_MAP['right']:
        moving_right = True
    if key == simplegui.KEY_MAP['up']:
        character.walk_up()
    if key == simplegui.KEY_MAP['down']:
        character.walk_down()   

def key_up(key):
    #Stops walking animation and stops movement.
    global moving_left, moving_right
    
    timer.stop()
    
    if key == simplegui.KEY_MAP['left']:
        moving_left = False
        character.vel[0] = 0
    if key == simplegui.KEY_MAP['right']:
        moving_right = False
        character.vel[0] = 0
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        character.vel[1] = 0
        
def timer_handler():
    #Controls walking animation
    character.col += 1
    if character.col == 4:
        character.col = 0

def change_volume(new_vol):
    global current_sound
    current_sound.set_volume(float(new_vol) / 10)

def draw(canvas):
    #Decides between map scrolling and character movement based on character position.
    #Also controls display of text and images
    global latitude, moving_left, moving_right, current_background
    
    #Displays the current map and coordinates
    if current_background == "map":    
        canvas.draw_image(background_image, [latitude, background_info.center[1]], 
                          background_info.get_size(), background_info.get_center(), background_info.get_size())
    else:
        background_info.draw(canvas, [WIDTH / 2, HEIGHT / 2])
    canvas.draw_text("Pos: (" + str(character.pos[0]) + ", " + str(character.pos[1]) + ") , Latitude: " + str(latitude), [125, 460], 28, "White")
    
    
    #Draws and updates the location and orientation of the character
    character.draw(canvas)
    character.update()
    
    #Controls whether the character moves itself or the map scrolls
    if moving_left and (latitude > background_info.center[0]) and (character.pos[0] == WIDTH / 2) and (current_background == "map"):
        latitude -= 1
        character.vel[0] = 0
        character.row_number = 1
    
    elif moving_right and (latitude < (background_info.center[0] + background_info.size[0])) and (character.pos[0] == WIDTH / 2) and (current_background == "map"):
        latitude += 1
        character.row_number = 2
        character.vel[0] = 0
    
    elif moving_left:
        character.walk_left()
    
    elif moving_right:
        character.walk_right()
        
    #Controls the borders of objects on screen
    if current_background == "map":    
        border_control(map_building_set)
    elif current_background == "center":
        border_control(center_building_set)
    elif current_background == "mart":
        border_control(mart_building_set)



#Creates the character
character = Character(character_image, character_info)

#Buildings on the main map
four_trees = Building(BORDERS[0], 138, 375, 490)
pokecenter = Building(69, 172, 541, 658, [587, 593], False, False, pokecenter_map, pkcmap_info, "center")
house = Building(236, 348, 541, 661, [616, 625])
gym = Building(247, 357, 265, 410, [342, 353], True)
pokemart = Building(81, 178, 277, 397, [321, 331], True, False, pokemart_map, pokemart_info, "mart")
sign = Building(196, 236, 108, 157, None, True, True)
map_building_set = set([four_trees, pokecenter, house, gym, pokemart, sign])

#Pokecenter Buildings
center_counter = Building(BORDERS[0], 214, 103, 345, [215, 232], True, True)
center_exit = Building(370, 370, 203, 243, [203, 243], True, False, map_image, map_info, "map")
center_building_set = set([center_counter, center_exit])

#Pokemart Buildings
mart_table = Building(274, 323, 87, 169, None, True)
mart_counter = Building(BORDERS[0], 258, BORDERS[2], 203, [137, 151], True, True)
mart_exit = Building(353, 353, 221, 259, [221, 259], True, False, map_image, map_info, "map")
mart_building_set = set([mart_table, mart_counter, mart_exit])

#Creates the window
frame = simplegui.create_frame("Pokemon Emerald", WIDTH, HEIGHT)

mute_text = "Mute"
#Creates the buttons
frame.add_input("Change Volume (0 to 10)", change_volume, 50)
#frame.add_button("Increase Volume", increase_volume)
#frame.add_button(mute_text, mute)

#Sets the handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

#Creates the timer
timer = simplegui.create_timer(150, timer_handler)

#Starts the frame
frame.start()
