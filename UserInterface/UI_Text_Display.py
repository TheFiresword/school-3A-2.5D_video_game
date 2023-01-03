from Services import Service_Font_Sprite_To_File as fonts
from Services import servicesGlobalVariables as const

import arcade

class Sprite_char():

    def __init__(self,char,color,pos):
        self.char = char
        self.font = fonts.Font(self.char,color)
        self.sprite = arcade.Sprite(filename=self.font.path,center_x=pos[0],center_y= pos[1],scale=1/2)
        pass

class Sprite_word(): 
    
    def __init__(self,string,color,pos_first_char):
        self.string = string
        self.color = color
        self.pos_start_x,self.pos_start_y = pos_first_char
        self.word = [Sprite_char(self.string[i],self.color,(self.pos_start_x+ i*const.FONT_WIDTH/2,self.pos_start_y)) for i in range(0,len(self.string))]
        self.sprite_word = arcade.SpriteList()
        self.fill_sprite_word()
        pass
    
    def setup(self):
        pass

    def fill_sprite_word(self):
        for sprite_char in self.word:
            self.sprite_word.append(sprite_char.sprite)
    
    def draw_(self):
        self.sprite_word.draw()
            


class Sprite_sentence():

    def __init__(self,sentence: str, color, pos_first_char):
        self.sentence = sentence
        self.color = color
        self.words= self.sentence.split(" ")
        self.pos_start_x,self.pos_start_y = pos_first_char
        self.sprite_sentence= []
        self.fill_sprite_sentence()
        pass

    def fill_sprite_sentence(self):
        x_offset = 0
        for word in self.words:
            self.sprite_sentence.append(Sprite_word(word,self.color,(self.pos_start_x + x_offset ,self.pos_start_y)))
            x_offset += const.FONT_WIDTH*(len(word)+1)/2
    
    def draw_(self):
        for sprite_word in self.sprite_sentence:
            sprite_word.draw_()