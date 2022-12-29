
import arcade
import arcade.gui

from Services import servicesGlobalVariables as cst

from UserInterface import UI_Text_Display as txt 

MIN_WIDHT = 400
NEXT_TEXTURE = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel39/paneling_00180.png")
QUESTION_TEXTURE = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel49/paneling_00528.png")


class PoP_Up_Text_Section():

    def __init__(self,top_left_x,top_left_y ,text ="", carved = False, automatic = False):
        self.width = 0
        self.height = 0
        self.pos = (top_left_x,top_left_y-5)
        self.text = text
        self.texts = []
        self.carved = carved
        self.carved_sprite = None
        if automatic:
            self.color = "white"
        else:
            self.color = "black"
        self.setup()

    def setup(self):
        self.treat_text()
        pass


    def treat_text(self):
        for line in self.text.split('\n'):
            self.texts.append(txt.Sprite_sentence(line,self.color,(self.pos[0]+25,self.pos[1] - len(self.texts)*cst.FONT_HEIGHT)))
            self.height += cst.FONT_HEIGHT + 5
            if len(line)*cst.FONT_WIDTH/2 > self.width:
                self.width = len(line)*cst.FONT_WIDTH/2

    def draw_(self):
        if self.carved:
            arcade.draw_texture_rectangle(center_x = 15+ self.pos[0] + self.width/2, center_y=self.pos[1] ,width= self.width,height=self.height,texture=arcade.load_texture(cst.SPRITE_PATH + "Panel/panel46.png"))
        for line in self.texts:
            line.draw_()
            
class PoP_Up_Image_Section():

    def __init__(self,image,width,height,top_left_x,top_left_y):
        self.width = width
        self.height = height
        self.image = image
        self.pos= (top_left_x,top_left_y)
        self.sprite = arcade.Sprite(self.image)
        self.setup()
        pass

    def setup(self):
        self.sprite.left(self.pos[0]+5)
        self.sprite.top(self.pos[0]+5)
        self.sprite.width = self.width
        self.sprite.height = self.height
    
    def draw_(self):
        self.sprite.draw()

class PoP_Up_Button_Section():

    def __init__(self,top_left_x,top_left_y, width):
        self.manager = arcade.gui.UIManager()
        self.width = width
        self.height = QUESTION_TEXTURE.image.size[1]
        self.pos = (top_left_x,top_left_y)
        self.question_button = arcade.gui.UITextureButton(top_left_x+5,top_left_y-self.height,texture=QUESTION_TEXTURE)
        self.next_button = arcade.gui.UITextureButton(top_left_x + width - QUESTION_TEXTURE.image.size[0],top_left_y-self.height,texture=NEXT_TEXTURE)
        
        self.manager.add(self.question_button)
        self.manager.add(self.next_button)
        pass

    def draw_(self):
        self.manager.draw()


class Full_PoP_Up():
    
    def __init__(self,title:PoP_Up_Text_Section = None,buttons:PoP_Up_Button_Section = None,normal_text:PoP_Up_Text_Section = None,carved_text:PoP_Up_Text_Section = None,order:list = [],top_left_corner = (0,cst.DEFAULT_SCREEN_HEIGHT),width = MIN_WIDHT):
        self.type = None
        self.zones = {
            "title_zone" : title,
            "button_zone" : buttons,
            "carved_text_zone": carved_text,
            "normal_text_zone":normal_text,
        }
        self.appear_order = order
        self.width = width
        self.height = 0
        self.pos=top_left_corner
        self.visible = False
        self.setup()
    
    def setup(self):
        for k in self.zones:
            if self.zones[k] != None:
                self.height += self.zones[k].height
        if self.zones["button_zone"] != None:
            self.zones["button_zone"].next_button.on_click = self.on_click_next
            self.zones["button_zone"].question_button.on_click = self.on_click_question

    def draw_(self):
        arcade.draw_texture_rectangle(width=self.width+10,height=self.height+10,
                                      texture=arcade.load_texture(cst.SPRITE_PATH + "Panel/panel1.png"),
                                      center_x=self.pos[0] + self.width/2,
                                      center_y=self.pos[1]- self.height/2)
        
        for k in self.appear_order:
            self.zones[k].draw_()
        pass 

    def on_click_next(self):
        self.visible = False
    
    def on_click_question(self):
        pass


def create_PoP_Up(title,normal_text="",carved_text="",top_left_corner=(0,cst.DEFAULT_SCREEN_HEIGHT),order=["title_zone","normal_text_zone","carved_text_zone"]):
    y_counter = 0
    width = 0
    title_section= None
    button_section = None
    carved_text_section = None
    normal_text_section = None
    for k in order:
        if k == "title_zone":
            title_section = PoP_Up_Text_Section(top_left_corner[0],top_left_corner[1]-y_counter,title)
            y_counter += title_section.height
            if title_section.width > width:
                width =  title_section.width
        if k == "button_zone":
            button_section = PoP_Up_Button_Section(top_left_corner[0],top_left_corner[1]-y_counter,max(MIN_WIDHT,width))
            y_counter += button_section.height
            if button_section.width > width:
                width =  button_section.width
        if k == "carved_text_zone":
           carved_text_section = PoP_Up_Text_Section(top_left_corner[0],top_left_corner[1]-y_counter,carved_text,True)
           y_counter += carved_text_section.height
           if carved_text_section.width > width:
                width = carved_text_section.width     
        if k == "normal_text_zone":
           normal_text_section = PoP_Up_Text_Section(top_left_corner[0],top_left_corner[1]-y_counter,normal_text)
           y_counter += normal_text_section.height
           if normal_text_section.width > width:
                width =  normal_text_section.width
    width = max(MIN_WIDHT,width)
    return Full_PoP_Up(title_section,button_section,normal_text_section,carved_text_section,order,top_left_corner,width)