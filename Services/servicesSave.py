import pickle
import shutil
import os


class save:
    def __init__(self):
        pass


    def load_buildings(self):
        with open('save_buildings.pkl',"rb") as save_file:
            load = pickle.load(save_file)

        return load


    def save_buildings(self,to_save):
        with open('save_buildings.pkl',"wb") as save_file:
            pickle.dump(to_save,save_file)

    def save_resources(self,to_save):
        with open('save_resources.pkl',"wb") as save_file:
            pickle.dump(to_save,save_file)

    def load_resources(self):
        with open('save_resources.pkl',"rb") as save_file:
            load = pickle.load(save_file)

        return load

    def save_entities(self,to_save):
        with open('save_entities.pkl',"wb") as save_file:
            pickle.dump(to_save,save_file)

    def load_entities(self):
        with open('save_entities.pkl',"rb") as save_file:
            load = pickle.load(save_file)

        return load

    def save_Map(self,to_save):
        with open('save_Map.pkl',"wb") as save_file:
            pickle.dump(to_save,save_file)

    def load_Map(self):
        with open('save_Map.pkl',"rb") as save_file:
            load = pickle.load(save_file)

        return load

    def load_back(self,save_num):

        current_directory = os.getcwd()
        save_directory = current_directory + "\\" + "saves"
        save1_directory = save_directory + "\\" + "save 1"
        save2_directory = save_directory + "\\" + "save 2"
        save3_directory = save_directory + "\\" + "save 3"
        print(save1_directory)
        if not os.listdir(save1_directory):
            print("vide wtf")
        if save_num == 1:
            if os.listdir(save1_directory):
                print("ok")
                os.remove(current_directory + "\\" + "save_buildings.pkl")
                os.remove(current_directory + "\\" + "save_resources.pkl")
                os.remove(current_directory + "\\" + "save_Map.pkl")
                shutil.copy(save1_directory + "\\" + "save_buildings.pkl", current_directory)
                shutil.copy(save1_directory + "\\" + "save_resources.pkl", current_directory)
                shutil.copy(save1_directory + "\\" + "save_Map.pkl", current_directory)

        if save_num == 2:
            if os.listdir(save2_directory):
                print("ok2")
                os.remove(current_directory + "\\" + "save_buildings.pkl")
                os.remove(current_directory + "\\" + "save_resources.pkl")
                os.remove(current_directory + "\\" + "save_Map.pkl")
                shutil.copy(save2_directory + "\\" + "save_buildings.pkl", current_directory)
                shutil.copy(save2_directory + "\\" + "save_resources.pkl", current_directory)
                shutil.copy(save1_directory + "\\" + "save_Map.pkl", current_directory)

        if save_num == 3:
            if os.listdir(save3_directory):
                print("ok3")
                os.remove(current_directory + "\\" + "save_buildings.pkl")
                os.remove(current_directory + "\\" + "save_resources.pkl")
                os.remove(current_directory + "\\" + "save_Map.pkl")
                shutil.copy(save3_directory + "\\" + "save_buildings.pkl", current_directory)
                shutil.copy(save3_directory + "\\" + "save_resources.pkl", current_directory)
                shutil.copy(save1_directory + "\\" + "save_Map.pkl", current_directory)

class file_manager:
    def __init__(self):
        pass

    def create_save(self):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\" + "saves"

        list_dir = os.listdir(save_directory)
        source = "save_buildings.pkl"
        source1 = "save_resources.pkl"
        source2 = "save_Map.pkl"

        if not os.listdir(save_directory + "\\" + "save 1"):
            shutil.copy(source,save_directory + "\\" + "save 1")
            shutil.copy(source1,save_directory + "\\" + "save 1")
            shutil.copy(source2,save_directory + "\\" + "save 1")
        elif not os.listdir(save_directory + "\\" + "save 2"):
            shutil.copy(source,save_directory + "\\" + "save 2")
            shutil.copy(source1,save_directory + "\\" + "save 2")
            shutil.copy(source2,save_directory + "\\" + "save 2")
        elif not os.listdir(save_directory + "\\" + "save 3"):
            shutil.copy(source,save_directory + "\\" + "save 3")
            shutil.copy(source1,save_directory + "\\" + "save 3")
            shutil.copy(source2,save_directory + "\\" + "save 3")

