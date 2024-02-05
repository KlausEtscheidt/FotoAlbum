'''
config.py
----------------

Konfigurationsparameter und globale Variable speichern
'''

import os
import platform
import tomlkit.toml_file
#import tomlkit.toml_document
#https://tomlkit.readthedocs.io/en/latest/

import wx

from settings_dialog import SettingsDlg
##Pfade
# Basis-Verzeichnis
my_file = os.path.realpath(__file__) # Welcher File wird gerade durchlaufen
my_dir = os.path.dirname(my_file)

class Config():
    '''Klasse zum Bereitstellen globaler Daten'''
    
    global my_dir
    tomlfilename = os.path.join(my_dir,"album_zerlegen.toml")

    def __init__(self):
        '''Konstruktor

        Konfigurationsdaten werden z.T. aus einem toml-file eingelesen.
        Weitere Daten werden hier bestimmt, oder von externen Modulen gesetzt.
        '''
        # toml-Struktur aus Datei lesen und merken
        self.tml = tomlkit.toml_file.TOMLFile(self.tomlfilename).read()

        tml = self.tml
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

        # Definierten Rahmen um Bild um Wert vergrössern
        self.rahmen_plus =  tml['rahmen_plus']

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
        '''Speichert wesentliche Konfigurationsdaten im toml-Format in Datei ab.'''
        self.tml['pfade']['pic_path'] = self.pic_path
        tomlkit.toml_file.TOMLFile(self.tomlfilename).write(self.tml)

    def savesettings(self):
        '''Überträgt Daten in die interne Toml-Struktur der Klasse'''
        self.tml['scale']['seite'] = self.SCALE_SEITE
        self.tml['scale']['kontrollbild'] = self.SCALE_KONTROLLBILD
        self.tml['rahmen_plus'] = self.rahmen_plus
        self.tml['min_winkel'] = self.MIN_WINKEL
        self.tml['pfade']['pic_output'] = self.pic_output

    def settings(self):
        '''Abfrage von Einstellungen beim Benutzer über Dialog'''
        with  SettingsDlg(None, 'Einstellungen', self) as Dlg:
            if Dlg.ShowModal() == wx.ID_CANCEL:
                return
        
        self.SCALE_SEITE = Dlg.scale_seite
        self.SCALE_KONTROLLBILD = Dlg.scale_kontrollbild
        self.MIN_WINKEL = Dlg.min_winkel
        self.pic_output = Dlg.pic_output
        self.rahmen_plus = Dlg.rahmen_plus
        

# conf als Globale
conf = Config()
