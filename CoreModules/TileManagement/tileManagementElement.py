import CoreModules.MapManagement.mapManagementLayer as Layer

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
    def __init__(self, layer, _type, cells_number, version="normal"):
        self.type = _type
        # L'id va être calculé directement à partir du layer auquel l'Element appartient
        self.id = None
        self.layer = layer
        self.dic = {"version": version, "cells_number": cells_number}
