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

class Config():
    '''Klasse zum Bereitstellen globaler Daten'''

    # Basis-Verzeichnis
    my_file = os.path.realpath(__file__) # Welcher File wird gerade durchlaufen
    my_dir = os.path.dirname(my_file)
    tomlfilename = os.path.join(my_dir,"album_zerlegen.toml")

    def __init__(self):
        '''Konstruktor

        Konfigurationsdaten werden z.T. aus einem toml-file eingelesen.
        Weitere Daten werden hier bestimmt, oder von externen Modulen gesetzt.
        '''
        # toml-Struktur aus Datei lesen und merken
        self.tml = tomlkit.toml_file.TOMLFile(self.tomlfilename).read()

        tml = self.tml

        # Pfade
        self.pic_subdir = tml['pfade']['pic_subdir']
        self.pic_output = tml['pfade']['pic_output']
        self.pic_type = tml['pfade']['pic_type']

        # Scales
        # Fuer erste Anzeige kompletter Seite
        self.scale_seite = tml['scale']['seite']
        # Fuers Setzen der Ecken
        self.scale_ecke = tml['scale']['ecke']
        # Fuer finale Kontrollanzeige
        self.scale_kontrollbild = tml['scale']['kontrollbild']

        # Ab wieviel Grad Schrägstellung wird ein Bild zurückgedreht
        self.min_winkel = tml['min_winkel']

        # Wie viele Pixel soll der Rand um Kontrollbilder größer sein,
        # als es den gewählten Bild-Ecken entsprechen würde.
        self.rand = tml['rand']

        # Definierten Rahmen um Bild um Wert vergrössern
        self.rahmen_plus =  tml['rahmen_plus']

        # Um wie viele Pixel soll bei Strg-Cursor das Bild verschoben werden.
        self.delta =  tml['delta_pfeiltasten']

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
        self.help = None

    def config_write(self):
        '''Speichert Konfigurationsdaten im toml-Format in Datei ab.

        Die Funktion wird automatisch beim Beenden des Programms ausgeführt.'''

        # Der Pfad kann durch Drop oder Benutzereingabe geändert worden sein
        # Er soll immer gespeichert werden.
        self.tml['pfade']['pic_path'] = self.pic_path
        tomlkit.toml_file.TOMLFile(self.tomlfilename).write(self.tml)

    def config2toml(self):
        '''Überträgt Daten aus dem conf-Objekt in die interne Toml-Struktur.

        Die Funktion muss per Menu aufgerufen werden, 
        da nicht generell alle Änderungen permanent sein sollen.'''
        self.tml['scale']['seite'] = self.scale_seite
        self.tml['scale']['kontrollbild'] = self.scale_kontrollbild
        self.tml['rahmen_plus'] = self.rahmen_plus
        self.tml['min_winkel'] = self.min_winkel
        self.tml['pfade']['pic_output'] = self.pic_output

    def settings(self):
        '''Abfrage von Einstellungen beim Benutzer über Dialog'''
        with  SettingsDlg(None, 'Einstellungen', self) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

        self.scale_seite = dlg.scale_seite
        self.scale_kontrollbild = dlg.scale_kontrollbild
        self.min_winkel = dlg.min_winkel
        self.pic_output = dlg.pic_output
        self.rahmen_plus = dlg.rahmen_plus

# conf als Globale
conf = Config()
