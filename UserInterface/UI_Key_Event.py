from Services import servicesGlobalVariables as constantes
{112:game_pause()}

class KeyEvent(current_view):
    def __init__(self,current_view):
        super().__init__()
        super.type = ""
        super.cam_mvt_key = []
        match type(current_view):
            case "<class 'UserInterface.UI_View_Map.MapView'>":
                super.type = "Game"
            case "<class 'UserInterface.UI_View_Load.LoadView'>":
                super.type = "Load"



        return


