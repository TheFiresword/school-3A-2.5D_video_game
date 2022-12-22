import arcade
from Services import servicesGlobalVariables as constantes

tuples_buttons = [(155,240,13,"000",79),(78,240,14,"000",82),
                  (116,267,16,"000",88),(78,267,17,"000",91),(39,267,18,"000",94),
                  (149,362,25,"00",123),(99,362,27,"00",131),(49,362,28,"00",135),
                  (149,396,26,"00",127),(99,396,35,"00",163),(49,396,32,"00",151),
                  (149,429,31,"00",147),(99,429,30,"00",143),(49,429,29,"00",139),
                  (149,464,36,"00",167),(99,464,34,"00",159),(49,464,33,"00",155),
                  (149,494,37,"00",171),(99,494,23,"00",115),(49,494,24,"00",119)


                 ]

buttons = [(constantes.DEFAULT_SCREEN_WIDTH - x,
            constantes.DEFAULT_SCREEN_HEIGHT - y,
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number) +".png"),
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number+1) +".png"),
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number+2) +".png"))
            for (x,y,folder,zero,number) in tuples_buttons]









