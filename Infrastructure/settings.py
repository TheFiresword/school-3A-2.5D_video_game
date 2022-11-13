#MACRO

class Macro():
    def __init__(self,window):
        self.name = ""
        self.key = ''
        self.windows = window
    def action(self):
        match self.key:
            case 'p':  self.windows.set_update_rate(0)

