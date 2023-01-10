from Services import servicesGlobalVariables as const
lower_case = "abcdefghijklmnopqrstuvwxyzäàâëéèêïìîöòôüùûçñæœå" 
upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
special = "!%()-+=:;'?" + "\\" + "/,._^°"
digit = "1234567890"

class Font():

    def __init__(self,char,color):
        self.char = char
        self.color = color
        self.type = None
        self.numero = 0 
        self.path = None
        self.setup()
        pass

    def setup(self):
        self.type,self.numero = self.string_to_type_folder()
        self.get_font_path()

    def string_to_type_folder(self):
        if self.char in lower_case  :
            return "lower_case",(lower_case.index(self.char))+1
        if self.char in upper_case :
            return "upper_case",(upper_case.index(self.char))+1
        if self.char in digit :
            return "digits",(digit.index(self.char))+1
        if self.char in special:
            return "special",(special.index(self.char))+1

    def get_font_path(self):
        self.path = const.SPRITE_PATH + "Fonts/" + self.type +"/"+self.color+"/"+str(self.numero)+".png"
        pass