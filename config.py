## @package config
# Konfigurationsparameter und globale Variable

import os
import platform
import tomlkit.toml_file
#import tomlkit.toml_document
#https://tomlkit.readthedocs.io/en/latest/


##Pfade
# Basis-Verzeichnis
# my_file = os.path.realpath(__file__) # Welcher File wird gerade durchlaufen
# my_dir = os.path.dirname(my_file)

class Config():

    tomlfile = "album_zerlegen.toml"

    def __init__(self):
        self.tomlfile = "album_zerlegen.toml"
        # toml_document lesen
        tml = tomlkit.toml_file.TOMLFile(self.tomlfile).read()
        self.tml = tml
        self.pic_subdir = tml['pfade']['pic_subdir']
        self.pic_output = tml['pfade']['pic_output']
        self.pic_type = tml['pfade']['pic_type']


        # Fuer erste Anzeige kompletter Seite
        self.SCALE_SEITE = tml['scale']['seite']
        # Fuers Setzen der Ecken
        self.SCALE_ECKE = tml['scale']['ecke']
        # Fuer finale Kontrollanzeige 
        self.SCALE_KONTROLLBILD = tml['scale']['kontrollbild']
        
        # Ab wieviel Grad Schrägstellung wird ein Bild zurückgedreht
        self.MIN_WINKEL = tml['min_winkel']

        # Rand um Kontrollbilder
        self.RAND = tml['rand']

        #Rechnername
        rechner = platform.node()
        # print(rechner )

        # --------- Bestimme pic_path: Das Verzeichnis mit den zu bearbeitenden Bildern (Seiten)
        #

        # User-Bilderverzeichnis als Basis des zu durchsuchenden LW
        if rechner == 'PC21-0018':
            self.pic_basispfad = r'C:\Users\Etscheidt\Pictures'  
        else:
            self.pic_basispfad = r'C:\Users\Klaus\Pictures'  

        # Zunächst prüfen, ob es das zuletzt benutzte Verzeichnis noch gibt
        self.pic_path = tml['pfade']['pic_path']

        # Wenn nicht, versuchen wir das Unterverzeichnis self.pic_subdir 
        # von self.pic_basispfad (Bilderverzeichnis des Users)
        if not os.path.isdir(self.pic_path):
            self.pic_path = os.path.join(self.pic_basispfad, self.pic_subdir) 

        # ----------------- globals
        # Hauptframe, wird vom Hauptprogramm gefüllt
        self.thisapp = None
        self.mainframe = None
        self.imagepanel = None

    def config_write(self):
        self.tml['pfade']['pic_path'] = self.pic_path
        tomlkit.toml_file.TOMLFile(self.tomlfile).write(self.tml)

# conf als Globale
conf = Config()
