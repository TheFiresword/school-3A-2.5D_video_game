from Services import servicesmMapSpriteToFile as mapping

"""
Un Element va être un objet contenu dans un layer
La relation entre un Element et un layer est une composition
Un Element ne peut exister qu'au sein d'un layer
Un Element ne peut donc être instancié directement par l'utilisateur
"""


class Element:
    # _type est le type de l'Element-- Ex: walker, grass,...
    # cells_number est le nombre de cases horizontales/verticales que l'Element occupe
    # version est la version du _type de l'Element-- Ex: yellow pour grass
    def __init__(self, layer, _type, version="normal"):
        self.type = _type
        # L'id et la position vont être calculés directement à partir du layer auquel l'Element appartient
        self.id = None
        self.position = (None, None)
        self.file_paths = None
        self.layer = layer
        self.dic = {"version": version, "cells_number": 0}
        self.set_file_infos()
        self.owner = None

    def set_file_infos(self):
        self.file_paths = mapping.mapping_function(self.type, self.dic['version'])
        # Here i suppose all levels of a building have the same size, but that is not correct.
        self.dic['cells_number'] = self.file_paths[0][1]
