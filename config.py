## @package config
# Konfigurationsparameter und globale Variable

import os
import getpass
import platform

BILD_MIN = 0
BILD_MAX = 2 #None

pic_type = '.tif'
pic_subdir = 'testpics'
pic_output = 'zerlegt'

SCALE_SEITE = 0.1 # Fuer erste Anzeige kompletter Seite
SCALE_ECKE  = 0.5 #  Fuers Setzen der Ecken
SCALE_KONTROLLBILD  = 0.2 #  Fuer finale Kontrollanzeige
MIN_WINKEL = .25
RAND = 20

#Rechnername
rechner = platform.node()
print(rechner )

## zu durchsuchende LW
if rechner == 'PC21-0018':
    pic_basispfad = r'C:\Users\Etscheidt\Pictures'  
else:
    pic_basispfad = r'C:\Users\Klaus\Pictures'  

pic_path = os.path.join(pic_basispfad, pic_subdir) 

# ----------------- globals
#Hauptframe, wird vom Hauptprogramm gefüllt
thisapp = None
mainframe = None
imagepanel = None

##Pfade
# Basis-Verzeichnis
my_file = os.path.realpath(__file__) # Welcher File wird gerade durchlaufen
my_dir = os.path.dirname(my_file)

#editor
editor = r'C:\Program Files\RawTherapee\5.7\rawtherapee.exe'

