import arcade
from Services import servicesGlobalVariables as constantes

tuples_buttons = [(155,240,13,"000",79),(78,240,14,"000",82),
                  (117,274,16,"000",88),(78,274,17,"000",91),(40,274,18,"000",94),
                  (155,200,24,"00",119),(155,200,25,"00",123),(155,200,26,"00",127),
                  (155,200,27,"00",131),(155,200,28,"00",135),(155,200,29,"00",139),
                  (155,200,30,"00",143),(155,200,31,"00",147),(155,200,32,"00",151),
                  (155,200,33,"00",155),(155,200,34,"00",159),(155,200,35,"00",163),
                  (155,200,23,"00",115),(155,200,36,"00",167),(155,200,37,"00",171)


                 ]

buttons = [(constantes.DEFAULT_SCREEN_WIDTH - x,
            constantes.DEFAULT_SCREEN_HEIGHT - y,
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number) +".png"),
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number+1) +".png"),
            arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel" + str(folder)+"/paneling_" +zero+ str(number+2) +".png"))
            for (x,y,folder,zero,number) in tuples_buttons]