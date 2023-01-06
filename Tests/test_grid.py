from PIL import Image
from Services import servicesGlobalVariables as cst

prefixe = 'C:/Users/Junior/Documents/3A/Programmation_Python/Projet_python/PythonProject/'
path1 = prefixe +cst.SPRITE_PATH + "WaterEquipments/WaterEquipments_00002.png"
path2 = prefixe+cst.SPRITE_PATH + "WaterEquipments/WaterEquipments_00003.png"

img1 = Image.open(path1)
img2 = Image.open(path2)
img2 = img2.resize(img1.size)

im3 = Image.alpha_composite(img2, img1)
im3.show()