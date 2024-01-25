## @package config
# Konfigurationsparameter und globale Variable

import os
import getpass
import platform

BILD_MIN = 0
BILD_MAX = 1

pic_type = '.tif'
pic_subdir = '1960'  

#Rechnername
rechner = platform.node()
print(rechner )

## zu durchsuchende LW
if rechner == 'PC21-0018':
    pic_basispfad = r'C:\Users\Etscheidt\Pictures'  
else:
    pic_basispfad = r'C:\Users\Etscheidt\Pictures'  

pic_path = os.path.join(pic_basispfad,pic_subdir) 

#Hauptframe, wird vom Hauptprogramm gefüllt
mainframe = None

# ----------------ab hier nur beispiel ----------------
#gueltige extensions
raw_pic_ext = ('.cr2', '.orf')
sidecar_ext = ('.pp3', '.xmp')
jpg_pic_ext = ('.jpg',)
pic_ext = raw_pic_ext + sidecar_ext + jpg_pic_ext
#pic_ext = ('.jpg', '.cr2', '.orf', '.pp3')

##Pfade
# Basis-Verzeichnis
my_file = os.path.realpath(__file__) # Welcher File wird gerade durchlaufen
my_dir = os.path.dirname(my_file)

#editor
editor = r'C:\Program Files\RawTherapee\5.7\rawtherapee.exe'

