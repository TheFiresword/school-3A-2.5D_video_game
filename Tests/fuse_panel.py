from PIL import Image
import os

print()
count = 0
def get_files_line_by_line(path,per_line):
    temp_files = os.listdir(path)
    files = [path+"/"+k for k in temp_files]
    lines = []
    line = []
    compteur = 1
    for k in files:
        if compteur == per_line:
            compteur = 1
            line.append(Image.open(k))
            real_line = line.copy()
            lines.append(real_line)
            line.clear()
        else:
            line.append(Image.open(k))
            compteur +=1
    return lines

def fuse_horizontally(line):
    largeur = sum([k.size[0] for k in line])
    hauteur = max([k.size[1] for k in line])
    image_ligne = Image.new('RGB',(largeur,hauteur),(250,250,250))
    buffer_size = 0
    for k in line:
        image_ligne.paste(k,(buffer_size,0))
        buffer_size += k.size[0]
    return image_ligne

def fuse_2_sprites_by_center(path1, path2, merged_name):
    global count
    im1 = Image.open(path1)
    im2 = Image.open(path2)

    largeur1, hauteur1 = im1.size[0], im1.size[1]
    largeur2, hauteur2 = im2.size[0], im2.size[1]


    left_corner_x = 60
    left_corner_y = 90

    fused_image = Image.new('RGBA',(largeur1, hauteur1))
    fused_image.paste(im1, (0, 0))
    fused_image.paste(im2, (left_corner_x, left_corner_y))


    if count == 0:
        fused_image.show()
    count += 1
    prefixe = "C:/Users/Junior/Documents/3A/Programmation_Python/Projet_python/PythonProject/Assets/sprites/C32/tmp"
    if os.getcwd() != prefixe:
        os.chdir(prefixe)
    _name = merged_name.replace('Commerce', 'bof')
    fused_image.save(_name)
    pass

def fuse_vertically(lines):
    largeur=max([k.size[0] for k in lines])
    hauteur= sum([k.size[1] for k in lines])
    image_totale = Image.new('RGB',(largeur,hauteur),(250,250,250))
    buffer_height = 0
    for k in lines:
        image_totale.paste(k,(0,buffer_height))
        buffer_height += k.size[1]
    return image_totale


def process(folder,per_line,output):
    lines_images = get_files_line_by_line(folder,per_line)
    lines_fused = [fuse_horizontally(k) for k in lines_images]
    total_fused = fuse_vertically(lines_fused)
    total_fused.save(output)


"""process("Assets/sprites/C32/Panel/Panel1",12,"panel1.png")
process("Assets/sprites/C32/Panel/Panel2",12,"panel2.png")
process("Assets/sprites/C32/Panel/Panel3",3,"panel3.png")
process("Assets/sprites/C32/Panel/Panel4",3,"panel4.png")
process("Assets/sprites/C32/Panel/Panel5",3,"panel5.png")
process("Assets/sprites/C32/Panel/Panel6",3,"panel6.png")
process("Assets/sprites/C32/Panel/Panel4",3,"panel4.png")
process("Assets/sprites/C32/Panel/Panel9",3,"panel9.png")
process("Assets/sprites/C32/Panel/Panel10",3,"panel10.png")
process("Assets/sprites/C32/Panel/Panel11",3,"panel11.png")
process("Assets/sprites/C32/Panel/Panel12",2,"panel12.png")
process("Assets/sprites/C32/Panel/Panel9",3,"panel9.png")
process("Assets/sprites/C32/Panel/Panel46",7,"panel46.png")
process("Assets/sprites/C32/Panel/Panel47",3,"panel47.png")
process("Assets/sprites/C32/Panel/Panel48",3,"panel48.png")
"""
#process("Assets/sprites/C32/Panel/Panel0",6,"panel0.png")
engineer = "C:/Users/Junior/Documents/3A/Programmation_Python/Projet_python/PythonProject/Assets/sprites/C32/tmp/"
prefixe = "C:/Users/Junior/Documents/3A/Programmation_Python/Projet_python/PythonProject/Assets/sprites/C32/tmp/"
paths = ["Commerce_00"+str(k)+".png" for k in range(142, 146)]

#for image_path in paths:
fuse_2_sprites_by_center(engineer+"bof_00142.png", engineer+"Commerce_00143.png", "Commerce_00142.png")