import arcade
import arcade.gui
from Services import Service_Game_Data as gdata
from Services import servicesGlobalVariables as constantes
from UserInterface import UI_Text_Display as txt 


texture_panel1 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel1.png")
texture_panel2 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel2.png")
texture_panel3 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel3.png")
texture_panel4 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel4.png")
texture_panel5 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel5.png")
texture_panel6 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel6.png")
texture_panel9 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel9.png")
texture_panel10 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel10.png")
texture_panel11 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel11.png")
texture_panel12 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel12.png")
texture_panel46 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel46.png")
texture_panel47 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel47.png")
texture_panel48 = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel48.png")




class Text_Button_background(arcade.gui.UITextureButton):

    def __init__(self,x,y,width,height,texture,my_text,color):
        super().__init__(x, y, width, height, texture)
        self.color = color
        self.my_text = my_text
        self.text_sprite = None
        self.center_text()
    
    def center_text(self):
        mid_box_x = self.x + self.width/2
        mid_box_y = self.y + self.height/2
        n = len(self.my_text)/2
        pos_x = mid_box_x - constantes.FONT_WIDTH/2 * n   
        pos_y = mid_box_y
        self.text_sprite = txt.Sprite_sentence(self.my_text,self.color,(pos_x,pos_y))
    
    def draw_(self):
        self.text_sprite.draw_()

class QuitButton(Text_Button_background):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class SettingButton(Text_Button_background):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.settingscreen.setup()
        window.show_view(window.settingscreen)





class NewGameButton(Text_Button_background):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.hide_view()
        window.show_view(window.gamescreen)

class LoadGameButton(Text_Button_background):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.show_view(window.loadscreen)
        window.loadscreen.fromview = "welcome"



# ============================
# Info to build right panel mains buttons
# ============================

tuples_buttons = [(155,240,13,"000",79),(78,240,14,"000",82),
                  (116,267,16,"000",88),(78,267,17,"000",91),(39,267,18,"000",94),
                  (149,362,25,"00",123),(99,362,27,"00",131),(49,362,28,"00",135),
                  (149,396,26,"00",127),(99,396,35,"00",163),(49,396,32,"00",151),
                  (149,429,31,"00",147),(99,429,30,"00",143),(49,429,29,"00",139),
                  (149,464,36,"00",167),(99,464,34,"00",159),(49,464,33,"00",155),
                  (149,494,37,"00",171),(99,494,23,"00",115),(49,494,24,"00",119)


                 ]

buttons = [(constantes.DEFAULT_SCREEN_WIDTH - x,
            constantes.DEFAULT_SCREEN_HEIGHT - y +47 ,
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number) +".png"),
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number+1) +".png"),
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number+2) +".png"))
            for (x,y,folder,zero,number) in tuples_buttons]

# =============================================
# Buttons that appears through the click on the previous buttons
# =============================================



def get_tuples(words):
    maxi = max([len(k) for k in words])
    button_heigh = constantes.FONT_HEIGHT/2 +10
    button_width = maxi*constantes.FONT_WIDTH
    x = constantes.DEFAULT_SCREEN_WIDTH - 163 - maxi*constantes.FONT_WIDTH
    y = constantes.DEFAULT_SCREEN_HEIGHT - 362
    color = "black"
    counter = 0
    tuples = []
    for k in words:
        mini_k = k.lower()
        if mini_k in gdata.building_dico:
            k_modif = k + ": " +str(gdata.building_dico[mini_k].cost) + " Dn"
            tuples.append((x,y-counter*button_heigh,button_width,button_heigh,texture_panel2,k_modif,color))
        else:
            tuples.append((x,y-counter*button_heigh,button_width,button_heigh,texture_panel2,k +"         +",color))
        counter += 1
    return tuples

def define_on_click_build(gameview,button_text):
    def on_click_button(event,game_view = gameview,but = button_text):
        game_view.builder_content = but.lower()
        game_view.builder_mode = True
    return on_click_button


def button_list(text_manager):
    tuples = get_tuples(text_manager)
    buttons_list = []
    for (my_x,my_y,my_width,my_height,my_texture,my_content,my_color) in tuples:
        button = Text_Button_background(my_x,my_y,my_width,my_height,my_texture,my_content,my_color)
        buttons_list.append(button)   
    return buttons_list

def define_on_click_button_manager(gameview,manager):
    def on_click_button(event,game_view = gameview,mana = manager):
        game_view.hide_all_manager()
        game_view.right_panel_manager_depth_one[mana].enable()
        game_view.manager_state[mana] = True
    return on_click_button

def define_on_click_button_selected(loadview,my_button):
    def on_click_button(event,load_view = loadview,button = my_button):
        load_view.selected_game = button.my_text
    return on_click_button





