

import arcade
import arcade.gui

from UserInterface import UI_View_Game as gv
from Services import servicesGlobalVariables as cst
from Services import servicesGlobalVariables as constantes
from UserInterface import UI_Text_Display as txt


MIN_WIDHT = 400
MAX_HEIGHT = 100
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
        if automatic:
            self.color = "white"
        else:
            self.color = "black"
        self.setup()

    def setup(self):
        self.treat_text()
        self.carved_panel = build_panel(2,(17+ self.pos[0],self.pos[1]+15),width= self.width,height=self.height)
        pass


    def treat_text(self):
        for line in self.text.split('\n'):
            self.texts.append(txt.Sprite_sentence(line,self.color,(self.pos[0]+30,self.pos[1] - len(self.texts)*cst.FONT_HEIGHT)))
            self.height += cst.FONT_HEIGHT
            if len(line)*cst.FONT_WIDTH/2 > self.width:
                self.width = len(line)*cst.FONT_WIDTH/2

    def draw_(self):
        if self.carved:
            self.carved_panel.draw()
            pass
        for line in self.texts:
            line.draw_()
            
class PoP_Up_Image_Section():

    def __init__(self,image,width,height,top_left_x,top_left_y):
        self.width = width
        self.image = arcade.load_texture(image)
        self.height = min(height,self.image.size[1])
        self.pos= (top_left_x,top_left_y)
        self.sprite = arcade.Sprite(center_x=self.pos[0]+self.width/2+24,center_y=self.pos[1] -self.height/2,texture=self.image)
        self.setup()
        pass

    def setup(self):
        self.sprite.width = self.width
        self.sprite.height= self.height
        pass
    
    def draw_(self):
        self.sprite.draw()

class PoP_Up_Button_Section():

    def __init__(self,top_left_x,top_left_y, width):
        self.manager = arcade.gui.UIManager()
        self.width = width
        self.height = QUESTION_TEXTURE.image.size[1]
        self.pos = (top_left_x,top_left_y)
        self.question_button = arcade.gui.UITextureButton(top_left_x+16,top_left_y-self.height,texture=QUESTION_TEXTURE,scale=1/2)
        self.next_button = arcade.gui.UITextureButton(top_left_x + width - 16 ,top_left_y-self.height,texture=NEXT_TEXTURE,scale=1/2)
        
        self.manager.add(self.question_button)
        self.manager.add(self.next_button)
        pass

    def draw_(self):
        self.manager.draw()


class Full_PoP_Up():
    
    def __init__(self,title:PoP_Up_Text_Section = None,buttons:PoP_Up_Button_Section = None,normal_text:PoP_Up_Text_Section = None,carved_text:PoP_Up_Text_Section = None,image:PoP_Up_Image_Section = None,order:list = [],top_left_corner = (0,cst.DEFAULT_SCREEN_HEIGHT),width = MIN_WIDHT):
        self.type = None
        self.zones = {
            "title_zone" : title,
            "button_zone" : buttons,
            "carved_text_zone": carved_text,
            "normal_text_zone":normal_text,
            "image_zone":image,
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
        self.panel = build_panel(1,self.pos,self.width,self.height)

    def draw_(self):
        self.zones["button_zone"].manager.enable()
        self.panel.draw()
        for k in self.appear_order:
            self.zones[k].draw_()
        pass 

    def on_click_next(self,event):
        self.visible = False
        self.zones["button_zone"].manager.disable()
    
    def on_click_question(self,event):
        pass
    
    
def create_PoP_Up(title,image = "",normal_text="",carved_text="",top_left_corner=(0,cst.DEFAULT_SCREEN_HEIGHT),order=["title_zone","normal_text_zone","carved_text_zone"]):
    y_counter = 0
    width = 0
    image_section=None
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
           carved_text_section = PoP_Up_Text_Section(top_left_corner[0]+4,top_left_corner[1]-y_counter,carved_text,True)
           y_counter += carved_text_section.height +10
           if carved_text_section.width > width:
                width = carved_text_section.width     
        if k == "normal_text_zone":
           normal_text_section = PoP_Up_Text_Section(top_left_corner[0],top_left_corner[1]-y_counter,normal_text)
           y_counter += normal_text_section.height
           if normal_text_section.width > width:
                width =  normal_text_section.width
        if k == "image_zone":
            image_section = PoP_Up_Image_Section(image,max(MIN_WIDHT,width),MAX_HEIGHT,top_left_corner[0],top_left_corner[1]-y_counter)
            y_counter += image_section.height+15
            if image_section.width > width:
                width =  image_section.width
    width = max(MIN_WIDHT,width)
    return Full_PoP_Up(title_section,button_section,normal_text_section,carved_text_section,image_section,order,top_left_corner,width)

def build_panel(panel,pos,width,height):
        width += 16
        first,last = True,False
        current_width = 0
        current_height = 0
        sprite_list = arcade.SpriteList()
        if panel == 1:
            top_left_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00335.png")
            bot_left_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00467.png")
            top_right_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00346.png")
            bot_right_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00478.png")
            top_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00336.png")
            bot_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00474.png")
            left_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00431.png")
            mid_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00432.png")
            right_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel1/paneling_00442.png")    
            bord = 0
            bord_haut=bot_left_angle.size[1]
            pos = pos[0],pos[1] + 20
            height +=16
        else:
            top_left_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00479.png")
            bot_left_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00521.png")
            top_right_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00485.png")
            bot_right_angle = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00527.png")
            top_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00480.png")
            bot_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00522.png")
            left_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00486.png")
            mid_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00488.png")
            right_mid = arcade.load_texture(cst.SPRITE_PATH + "Panel/Panel46/paneling_00499.png")
            bord = top_right_angle.size[0]
            bord_haut = 0
            height -= 16
        while current_height < height + bord_haut:
            current_width = 0
            if first:
                firstpart = top_left_angle
                lastpart = top_right_angle
                midpart = top_mid
                current_x = pos[0] + firstpart.size[0]/2
                current_y = pos[1]- firstpart.size[1]/2
            elif last:
                firstpart = bot_left_angle
                lastpart = bot_right_angle
                midpart = bot_mid
                current_x = pos[0] + firstpart.size[0]/2
                current_y -= firstpart.size[1]/2
            else:
                firstpart = left_mid
                lastpart = right_mid
                midpart = mid_mid
                current_x = pos[0] + firstpart.size[0]/2
                current_y -= firstpart.size[1]/2
            sprite_list.append(arcade.Sprite(texture=firstpart,center_x=current_x,center_y=current_y))
            if not first:
                current_height += firstpart.size[1]
            current_width += firstpart.size[0]
            current_x += firstpart.size[0]/2
            while current_width < width - bord:
                current_x += midpart.size[0]/2
                sprite_list.append(arcade.Sprite(
                                      texture=midpart,
                                      center_x=current_x,
                                      center_y=current_y))
                current_x += midpart.size[0]/2
                current_width += midpart.size[0]
            current_x += lastpart.size[0]/2
            sprite_list.append(arcade.Sprite(
                                      texture=lastpart,
                                      center_x=current_x,
                                      center_y=current_y))
            current_y -= lastpart.size[1]/2
            current_width += lastpart.size[0]
            if first:
                first = False
            if current_height + bot_left_angle.size[1] >= height + bord_haut:
                last = True
        return sprite_list

def info_building_pop_up(name, number_occupants, required_occupants):
        pop_up = None
        text = str(number_occupants) + " Employees" + "  " + str(required_occupants) + " " + "(required)"
        #Temples of gods POP_UPS
        if name == "mercure":
                pop_up =create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/panelwindows_00024.png", title="Temple of " + name,
                                normal_text="tchoupi", carved_text=text,
                                top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        elif name == "ceres":
                pop_up = create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/panelwindows_00022.png", title="Temple of " + name,
                                       normal_text="tchoupi", carved_text=text,
                                       top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                       order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        elif name == "neptune":
                pop_up = create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/panelwindows_00023.png", title="Temple of " + name,
                                       normal_text="tchoupi", carved_text=text,
                                       top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                       order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        elif name == "mars":
                pop_up = create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/panelwindows_00025.png", title="Temple of " + name,
                                       normal_text="tchoupi", carved_text=text,
                                       top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                       order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        elif name == "venus":
                pop_up = create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/panelwindows_00026.png", title="Temple of " + name,
                                       normal_text="tchoupi", carved_text=text,
                                       top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                       order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        #Engineering structures POP_UPS
        elif name == "engineer's_post":
                pop_up = create_PoP_Up(title="Engineer's_post\n"
                                             "Our engineers are always outside inspecting\n"
                                             "and repairing damaged buildings in the city.\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        elif name == "quai":
                pop_up = create_PoP_Up(title="Quai\n"
                                     "Our boat is heading towards the fishing area\n",
                               normal_text="tchoupi", carved_text=text,
                               top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                               order=["title_zone", "carved_text_zone", "button_zone"])
        #Education POP_UPS
        elif name == "school":
                pop_up = create_PoP_Up(title="School\n"
                                         "it is here that children are taught\n"
                                         "the basics of reading, writing and rhetoric\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])

        elif name == "university":
                pop_up = create_PoP_Up(title="University\n"
                                          "young people who aspire to become learned citizens come\n"
                                          "here to perfect their education in rhetoric and history\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        elif name == "library":
                pop_up = create_PoP_Up(title="Library\n"
                                         "Literary works from the four corners of the empire are brought\n"
                                         "together in this building for the attention of scholars and the curious.\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        #Water Equipments POP_UPS
        elif name == "fountain":
                pop_up = create_PoP_Up(title="Fountain\n"
                                         "The population draws all the water they need from the fountains,\n"
                                         "which must be located in the supply zone of a reservoir\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        elif name == "reservoir":
            pop_up = create_PoP_Up(title="Reservoir\n"
                                         "This giant cistern contains drinking water which is then\n"
                                         "distributed through clay pipes in a wide perimeter\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        elif name == "aqueduct":
            pop_up = create_PoP_Up(title="Aqueduct\n"
                                     "This aqueduct carries water between two reservoirs\n",
                               normal_text="tchoupi", carved_text=text,
                               top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                               order=["title_zone", "carved_text_zone", "button_zone"])

        #Security POP_UPS
        elif name == "prefecture":
            pop_up = create_PoP_Up(title="Prefecture\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])

        elif name == "military_academy":
            pop_up = create_PoP_Up(title="Military academy\n"
                                   "When new recruits come out of the barracks, they want to improve\n"
                                    "their fighting techniques at the academy\n",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        elif name == "barracks":
            pop_up = create_PoP_Up(title="Barracks\n"
                                   "",
                                   normal_text="tchoupi", carved_text=text,
                                   top_left_corner=(0, constantes.DEFAULT_SCREEN_HEIGHT - 50),
                                   order=["title_zone", "carved_text_zone", "button_zone"])
        #Entertainement POP_UPS


        return pop_up


        
    