import arcade
import arcade.gui
from arcade import load_texture
from arcade.gui import UITextArea, UITexturePane


HEIGHT = 800
WIDTH = 600
PICTURE_SCALING = 0.3
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE_Generaltext = 20
DEFUALT_FONT_SIZE_DescriptionText = 15


class MyWindow(arcade.Window):

    def __init__(self):
        super().__init__(HEIGHT , WIDTH, "Popup Example", resizable=False)
        self.start_x = 250
        #photo d'incendie
        self.picture_list = None
        self.picture_sprite = None
        #photo d'effondrement
        self.picture_list1 = None
        self.picture_sprite1 = None
        #background
        self.background = arcade.load_texture("UI.png")

        self.T1 = True
        self.T2 = False
        self.T3 = False
        self.T4 = False

        #mangers des boutons et panels
        self.manager_suivant = arcade.gui.UIManager()
        self.manager_panel_home = arcade.gui.UIManager()
        self.manager_open = arcade.gui.UIManager()
        self.manager_Panel_incendie = arcade.gui.UIManager()
        self.manager_Panel_effondrement = arcade.gui.UIManager()
        self.manager_ok = arcade.gui.UIManager()

        self.manager_open.enable()

        self.sprite_list = None

        #buttons
        Ok = arcade.gui.UIFlatButton(text="Ok", width=60)
        Suivant = arcade.gui.UIFlatButton(text="Suivant", width=90)
        Open = arcade.gui.UIFlatButton(text="Open", width=200)
        Open2 = arcade.gui.UIFlatButton(text="Open2", width=200)
        Open3 = arcade.gui.UIFlatButton(text="Open3", width=200)

        #create vertical boxes for buttons
        self.v_box_Open = arcade.gui.UIBoxLayout()
        self.v_box_Ok = arcade.gui.UIBoxLayout()
        self.v_box_Suivant = arcade.gui.UIBoxLayout()

        #Add vertical buttons for vertical boxs
        self.v_box_Open.add(Open.with_space_around(bottom=20))
        self.v_box_Open.add(Open2.with_space_around(bottom=20))
        self.v_box_Open.add(Open3.with_space_around(bottom=20))
        self.v_box_Ok.add(Ok)
        self.v_box_Suivant.add(Suivant)

        #onaction
        Open3.on_click = self.on_click_open3
        Open2.on_click = self.on_click_open2
        Open.on_click = self.on_click_open
        Ok.on_click = self.on_click_ok
        Suivant.on_click = self.on_click_suivant

        #managers of buttons and panels
        self.manager_open.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box_Open)
        )


        self.manager_suivant.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                align_x=-180,
                anchor_y="bottom",
                align_y=90,
                child=self.v_box_Suivant)
        )
        self.start_y = 520
        self.start_x = 170
        self.Home_text = arcade.Text(
            "Nouveau gouverneur",
            self.start_x, self.start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE_Generaltext,
            font_name="Kenney Mini Square",
        )
        self.start_y = 500
        self.start_x = 170
        self.Home_text1 = arcade.Text(
            "Un village est né",
            self.start_x,
            self.start_y,
            arcade.color.BLACK,
            DEFUALT_FONT_SIZE_DescriptionText
        )
        self.start_y = 400
        self.start_x = 190
        self.Home_text2 = arcade.Text(
            "Objectifs :",
            self.start_x,
            self.start_y,
            arcade.color.WHITE,
            DEFUALT_FONT_SIZE_DescriptionText
        )
        self.start_y = 370
        self.start_x = 190
        self.Home_text3 = arcade.Text(
            "Population de 150 : \n"
            "\n"
            "Objectif premier : construisez des habitations.\n"
            "Ave citoyen ! que votre formation de gouverneur commence !\n"
            "Vous devez tous d'abord apprendre les bases de la construction d'une colonie romaine.\n"
            "Délimitez des zones d'habitations et vous verrez bientot des imigrants venir s'installer.\n",
            self.start_x,
            self.start_y,
            arcade.color.WHITE,
            DEFUALT_FONT_SIZE_DescriptionText,
            multiline=True,
            width = 450
        )
        self.start_y = 500
        self.start_x = 180
        self.Home_text4 = arcade.Text(
            "Information sur le batiment :\n"
            "\n"
            "5 occupants"
            ,
            self.start_x,
            self.start_y,
            arcade.color.BLACK,
            DEFUALT_FONT_SIZE_DescriptionText,
            multiline=True,
            width=450
        )


        bg_tex = load_texture("Window03.png")

        text_area = UITextArea(x=180,
                               y=70,
                               width=450,
                               height=480,
                               text_color=(254, 254, 250))
        self.manager_panel_home.add(
            UITexturePane(
                text_area,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        self.manager_ok.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                align_x=-160,
                anchor_y="bottom",
                align_y=60,
                child=self.v_box_Ok)
        )
        bg_tex = load_texture("PanelWindow.png")

        #Incendie
        self.text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget pellentesque velit. "
                     "Nam eu rhoncus nulla. Fusce ornare libero eget ex vulputate, vitae mattis orci eleifend. "
                     "Donec quis volutpat arcu. Proin lacinia velit id imperdiet ultrices. Fusce porta magna leo, "
                     "non maximus justo facilisis vel. Duis pretium sem ut eros scelerisque, a dignissim ante "
                     "pellentesque. Cras rutrum aliquam fermentum. Donec id mollis mi.\n"
                     "\n"
                     "Nullam vitae nunc aliquet, lobortis purus eget, porttitor purus. Curabitur feugiat purus sit "
                     "amet finibus accumsan. Proin varius, enim in pretium pulvinar, augue erat pellentesque ipsum, "
                     "sit amet varius leo risus quis tellus. Donec posuere ligula risus, et scelerisque nibh cursus "
                     "ac. Mauris feugiat tortor turpis, vitae imperdiet mi euismod aliquam. Fusce vel ligula volutpat, "
                     "finibus sapien in, lacinia lorem. Proin tincidunt gravida nisl in pellentesque. Aenean sed "
                     "arcu ipsum. Vivamus quam arcu, elementum nec auctor non, convallis non elit. Maecenas id "
                     "scelerisque lectus. Vivamus eget sem tristique, dictum lorem eget, maximus leo. Mauris lorem "
                     "tellus, molestie eu orci ut, porta aliquam est. Nullam lobortis tempor magna, egestas lacinia lectus.\n")


        self.start_y = 100
        self.General_text_incendie = arcade.Text(
            "Incendie dans la cité",
            self.start_x, self.start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE_Generaltext,
            font_name="Kenney Mini Square",
        )
        text_area = UITextArea(x=200,
                               y=140,
                               width=400,
                               height=150,
                               text=self.text,
                               text_color=(254, 254, 250))
        self.manager_Panel_incendie.add(
            UITexturePane(
                text_area,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        #Effondrement
        self.General_text_Effondrement = arcade.Text(
            "Effondrement d'un batiment",
            self.start_x, self.start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE_Generaltext,
            font_name="Kenney Mini Square",
        )


        #sprite d'incendie
        self.picture_list = arcade.SpriteList()
        self.picture_sprite = arcade.Sprite("10b_00001.png", PICTURE_SCALING)
        self.picture_sprite.center_x = HEIGHT / 2
        self.picture_sprite.center_y = WIDTH / 2 + 120
        self.picture_list.append(self.picture_sprite)

        #sprite effondrement
        self.picture_list1 = arcade.SpriteList()
        self.picture_sprite1 = arcade.Sprite("effondrement.jpg", PICTURE_SCALING)
        self.picture_sprite1.center_x = HEIGHT / 2
        self.picture_sprite1.center_y = WIDTH / 2 + 120
        self.picture_list1.append(self.picture_sprite1)




    def switch(self):

        if self.T1:
            self.manager_open.draw()
        if self.T2:
            #effondrement ou incendie
            self.Popup("effondrement")
        if self.T3:
            self.Popup_Acceuil()
        if self.T4:
            self.Popup_Info_Batiment()



    def Popup(self,case):
        if case == "Incendie":
            arcade.draw_rectangle_filled(HEIGHT / 2, WIDTH / 2, 500, 500, (251, 206, 177))
            self.manager_Panel_incendie.draw()
            self.manager_ok.draw()
            self.picture_list.draw()
            self.General_text_incendie.draw()
            self.surroundings()
        if case == "effondrement":
            arcade.draw_rectangle_filled(HEIGHT / 2, WIDTH / 2, 500, 500, (251, 206, 177))
            self.manager_Panel_incendie.draw()
            self.manager_ok.draw()
            self.picture_list1.draw()
            self.General_text_Effondrement.draw()
            self.surroundings()


    def Popup_Info_Batiment(self):
        arcade.draw_rectangle_filled(HEIGHT / 2, WIDTH / 2, 500, 500, (251, 206, 177))
        self.Home_text4.draw()
        self.manager_ok.draw()
        self.surroundings()


    def Popup_Acceuil(self):
        arcade.draw_rectangle_filled(HEIGHT / 2, WIDTH / 2, 500, 500, (251, 206, 177))
        self.Home_text.draw()
        self.Home_text1.draw()
        self.manager_panel_home.draw()
        self.Home_text2.draw()
        self.Home_text3.draw()
        self.manager_suivant.draw()
        self.manager_suivant.enable()
        self.surroundings()


    def on_click_open(self, event):

        self.T1 = False
        self.manager_Panel_incendie.enable()
        self.manager_ok.enable()
        self.T2 = True

    def on_click_open2(self, event):

        self.T1 = False
        self.manager_Panel_incendie.enable()
        self.manager_ok.enable()
        self.T3 = True

    def on_click_open3(self, event):

        self.T1 = False
        self.manager_ok.enable()
        self.T4 = True

    def on_click_ok(self, event):
        self.manager_open.enable()
        self.T1 = True
        self.T2 = False
        self.T4 = False


    def on_click_suivant(self, event):
        self.manager_open.enable()
        self.T1 = True
        self.T2 = False
        self.T3 = False



    def surroundings(self):
        arcade.draw_line(150, 550, 650, 550, (0, 0, 0), 3)
        arcade.draw_line(150, 50, 650, 50, (0, 0, 0), 3)
        arcade.draw_line(150, 50, 150, 550, (0, 0, 0), 3)
        arcade.draw_line(650, 50, 650, 550, (0, 0, 0), 3)


    def on_draw(self):
            self.clear()
            arcade.draw_lrwh_rectangle_textured(0, 0, HEIGHT, WIDTH, self.background)
            self.switch()
