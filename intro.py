"""
I am having issues running this in normal python - the timers appear not to work. 
Please see http://www.codeskulptor.org/#user40_eSzMY579k7_5.py for the most recent working version.
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 480
HEIGHT = 480
dialog_place = 0  
l1_textscroller = 1
l2_textscroller = 0
name_choose = False
name = ""
class ImageInfo:
    """
    Processes image information
    """
    def __init__(self, center, size, image, animated = False, lifespan = 0):
        self.center = center
        self.size = size
        self.image = image

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size
                          
    def draw(self, canvas, location):
        canvas.draw_image(self.image, self.center, self.size, location, self.size)

class Dialog:
    def __init__(self, dialog_list):
        self.dialog = dialog_list
        self.drawing_text = ""
        for i in range(len(self.dialog)):
            if type(self.dialog[i]) == str:
                self.dialog[i] = self.dialog[i].upper()
    def dialog_handler(self, canvas):
        global dialog_place, l1_textscroller, l2_textscroller
        if dialog_place < len(self.dialog):
            canvas.draw_text(self.dialog[dialog_place][0:l1_textscroller], [30, 390], 14, "Black", "monospace")
        if dialog_place + 1 < len(self.dialog):
            if type(self.dialog[dialog_place + 1]) == str:
                canvas.draw_text(self.dialog[dialog_place + 1][0:l2_textscroller], [30, 415], 14, "Black", "monospace")
        if self.dialog[dialog_place] == 0:
            name_choose = True
intro_dialog = ["hi! sorry to keep you waiting.",
                'welcome to the world of pokemon!',
               'my name is professor birch.',
              'but everyone calls me the pokemon professor.',
               'this is what we call a "pokemon".',
               'this world is widely inhabited by creatures known',
               'as pokemon.',
               'it is my job to research them in order to uncover',
               'their secrets.',
               "and what about you?",
                "What's your name?",
               0]

introduction_image = simplegui.load_image("http://i.imgur.com/kMGRHzm.jpg")
introimg_info = ImageInfo([WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT], introduction_image)

textbox_image = simplegui.load_image("http://i.imgur.com/mCAOj2C.jpg")
textbox_info = ImageInfo([460 / 2, 83 / 2], [460, 83], textbox_image)

explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_info = ImageInfo([64, 64], [128, 128], explosion_image, True, 24)


def keydown(key):
    #Keydown Handler
    global dialog_place, l1_textscroller, l2_textscroller, name_choose, name
    if name_choose:
        name += key
        print name
    elif key == simplegui.KEY_MAP['space']:
        if dialog_place + 1 < len(current_dialog.dialog):
            if type(current_dialog.dialog[dialog_place + 1]) == str:
                if l1_textscroller < len(current_dialog.dialog[dialog_place]) or l2_textscroller <= len(current_dialog.dialog[dialog_place + 1]):
                    l1_textscroller = len(current_dialog.dialog[dialog_place]) - 1
                    l2_textscroller = len(current_dialog.dialog[dialog_place + 1]) - 1
                else:
                    dialog_place += 2
                    l1_textscroller = 0
                    l2_textscroller = 0
        else:
            dialog_place += 2
            l1_textscroller = 0
            l2_textscroller = 0
            
def text_timer():
    #every tick add another letter to animate the textboxes
    global l1_textscroller, dialog_place, l2_textscroller
    if dialog_place < len(current_dialog.dialog):
        if l1_textscroller <= len(current_dialog.dialog[dialog_place]):
            l1_textscroller += 1
            
    if dialog_place + 1 < len(current_dialog.dialog) and l1_textscroller >= len(current_dialog.dialog[dialog_place]):
        if type(current_dialog.dialog[dialog_place + 1]) == str:
            if l2_textscroller <= len(current_dialog.dialog[dialog_place + 1]):
                l2_textscroller += 1

def draw(canvas):
    # Handler to draw on canvas
    global intro_dialog
    introimg_info.draw(canvas, [WIDTH / 2, HEIGHT / 2])
    textbox_info.draw(canvas, [WIDTH / 2, 400])
    
    current_dialog.dialog_handler(canvas)
    
current_dialog = Dialog(intro_dialog)
    
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Introduction", WIDTH, HEIGHT)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

text_timer = simplegui.create_timer(20, text_timer)
text_timer.start

# Start the frame animation
frame.start()
