import arcade
from UserInterface import UI_buttons as but
from UserInterface import UI_View_Game as rgv
from Services import servicesGlobalVariables as constantes
from Services import Service_Save_and_Load as saveload
from Services import Service_Static_functions as static
import struct
import arcade.gui
from CoreModules.NetworkManagement.Echange import echanger, dict_demon, encode_update_packets, decode_update_packets, decode_ponctual_packets, find_key, Packet, PacketTypes


class ReseauLoginScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = arcade.load_texture(
            constantes.SPRITE_PATH + "Screens/0_fired_00001.png")

        self.x = constantes.DEFAULT_SCREEN_WIDTH / 2 - 100
        self.y = constantes.DEFAULT_SCREEN_HEIGHT / 2 + 100

        self.title = arcade.gui.UILabel(
            text="Enter Networking informations",
            font_size=18,
            text_color=arcade.color.BLACK,
            font_name="Arial",
            bold=True,
            width=400)

        self.title_box = arcade.gui.UIBoxLayout(
            children=[self.title]).with_border()

        self.ip_label = arcade.gui.UILabel(
            text="IP:",
            width=100,
            text_color=arcade.csscolor.ROYAL_BLUE,
            font_size=22,
            font_name="Arial",
            bold=True)

        self.ip_field = arcade.gui.UIInputText(
            text_color=arcade.color.RED,
            font_size=22,
            width=300,
            font_name="Arial",
            text='192.168.1.158',
        )

        self.first = arcade.gui.UIBoxLayout(vertical=False,
                                            children=[self.ip_label, self.ip_field.with_space_around(left=50)])

        self.port_label = arcade.gui.UILabel(
            text="Port:",
            width=100,
            text_color=arcade.csscolor.ROYAL_BLUE,
            font_size=22,
            font_name="Arial")

        self.port_field = arcade.gui.UIInputText(
            text_color=arcade.color.RED,
            font_size=22,
            width=300,
            font_name="Arial",
            text='',
        )

        self.second = arcade.gui.UIBoxLayout(vertical=False,
                                             children=[self.port_label, self.port_field.with_space_around(left=50)])
        self.ip_field.cursor_index = len(self.ip_field.text)
        # self.port_field.cursor_index = len(self.port_field.text)

        self.button = arcade.gui.UITextureButton(
            texture=arcade.load_texture(
                constantes.SPRITE_PATH + "Panel/Panel40/paneling_00241.png"),
            texture_hovered=arcade.load_texture(
                constantes.SPRITE_PATH + "Panel/Panel40/paneling_00239.png"),
            texture_pressed=arcade.load_texture(
                constantes.SPRITE_PATH + "Panel/Panel40/paneling_00240.png"),
            scale=1 / 2)

        self.button.on_click = self.on_create_click

        self.box = arcade.gui.UIBoxLayout(x=self.x, y=self.y,
                                          children=[self.title_box.with_space_around(top=20),
                                                    self.first.with_space_around(
                                                        left=20),
                                                    self.second.with_space_around(
                                                        left=20),
                                                    self.button.with_space_around(top=50, bottom=20)]
                                          ).with_background(texture=but.texture_panel1)

        self.manager.add(self.box)

    def on_create_click(self, event):
        import random
        # IPC
        port = self.port_field.text
        ip = self.ip_field.text
        window = arcade.get_window()
        owner = window.gamescreen.game.owner
        

        if port != '':
            port = int(port)
            # connection to the dest
            # receive the game online
            # load that game
            # change the owner
            ip_port_body = struct.pack("IH", Packet.intAddressFromAdress(owner[0]),owner[1])
            print(ip_port_body)
            game = None
            echanger.send(Packet(ip_port_body,port, owner[0], ip, PacketTypes.Init))
            print("packet init envoyé")
            echanger.receive(type= PacketTypes.Send_IP,block=True)
            print("packet send_ip reçu")

            echanger.send(Packet(ip_port_body, port, owner[0],ip,PacketTypes.Sauvegarde_ask))
            print("packet sauvegarde_ask envoyé")
            echanger.receive(type=PacketTypes.Sauvegarde_send,block=True)
            print("packet sauvegarde_send reçu")
            game = saveload.load_game("to-send")
            game.players = []
            game.players.append((game.owner,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            game.owner = owner
            game.players.append((game.owner,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            print("game chargé, owner changé, players ajoutés")
            echanger.send(Packet(ip_port_body, port, owner[0],ip,PacketTypes.Ask_Broadcast))
            print("packet ask_broadcast envoyé")
            echanger.receive(type=PacketTypes.Broacast_new_player,block=True)
            print("packet send_broadcast reçu")
            window.gamescreen = rgv.GameView(_game=game)
        window.show_view(window.gamescreen)

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH / 2,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                      width=constantes.DEFAULT_SCREEN_WIDTH, height=constantes.DEFAULT_SCREEN_HEIGHT,
                                      texture=self.background)

        self.manager.draw()

    def on_hide(self):
        self.manager.disable()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()