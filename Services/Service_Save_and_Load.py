import pickle
import shutil
import os


def save_game(to_save, name):
    with open('Assets/games/'+name+'.pkl',"wb") as save_file:
        pickle.dump(to_save,save_file)

def load_game(name):
    with open('Assets/games/'+name+'.pkl',"rb") as save_file:
        load = pickle.load(save_file)
    return load

def delete_game(name):
    os.remove('Assets/games/'+name+'.pkl')

def list_saved_games():
    return os.listdir('Assets/games')
