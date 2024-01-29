import logging

import wx

import config as conf
from seite import Seiten, Seite

logger = logging.getLogger('album')


class Ablauf:

    def __init__(self, imagepanel):
        # Klassenvar setzen
        Seite.imagepanel = imagepanel
        # Seite.imagectrl = imagepanel.imagectrl
        self.imagepanel = imagepanel
        self.imagectrl = imagepanel.imagectrl

        self.__status = 'Start Seite'
        self.__seiten_nr = -1
        self.__seiten = None
        self.__seite = None

        self.__rahmen_lo = (0, 0)
        self.__rahmen_ru = (0, 0)
    
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, x):
        self.__status = x

    @property
    def rahmen_lo(self):
        return self.__rahmen_lo

    @rahmen_lo.setter
    def rahmen_lo(self, x):
        self.__rahmen_lo = x
        self.__status = 'Rahmen ru'

    @property
    def rahmen_ru(self):
        return self.__rahmen_ru

    @rahmen_ru.setter
    def rahmen_ru(self, x):
        self.__rahmen_ru = x

    ############################################################################
    #
    # Aktionen übergeordnet
    #
    ############################################################################

    def dateiliste_erstellen(self):
        # Filenamen der Seiten-Tiffs einlesen
        # Seiten erzeugen (ohne image) und in Liste merken
        self.__seiten = Seiten()

    ############################################################################
    #
    # Aktionen je Seite
    #
    ############################################################################

    def seite_bearbeiten(self, seiten_nr):
        """seite_bearbeiten Seite eines Fotoalbums bearbeiten

        Fragt vom Benutzer die Daten (Ecken) aller Fotos auf der Seite ab
        und speichert die Fotos als tiff-Datei.
        Durch die Anzeige des Original-Bilds wird für dieses ein Image erzeugt.
        Es sollte beim Verlassen der Seite freigegeben werden.

        :param seiten_nr: index der zu bearbeitenden Seite in self.__seiten
        :type seiten_nr: int
        """        
        self.imagectrl.SetFocus()
        self.__seiten_nr = seiten_nr # merken f next
        # Status auf Anfang Seite bearbeiten
        self.__status = 'Start Seite'
        # Seite als aktiv merken
        self.__seite = self.__seiten[seiten_nr]
        # Anzeigen
        self.__seite.show_origbild()

    def seite_bearbeiten_next(self):
        if self.__seiten_nr < len(self.__seiten)-1:
            # Speicher freigeben
            self.__seiten[self.__seiten_nr].free_origbild()
            self.__seiten_nr += 1
            self.seite_bearbeiten(self.__seiten_nr)

    def seite_bearbeiten_prev(self):
        if self.__seiten_nr > 0:
            # Speicher freigeben
            self.__seiten[self.__seiten_nr].free_origbild()
            self.__seiten_nr -= 1
            self.seite_bearbeiten(self.__seiten_nr)

    ############################################################################
    #
    # Aktionen je Foto
    #
    ############################################################################

    # 1. Aktion je Foto:
    # Foto anhand Rahmen erzeugen und ablegen
    def foto_rahmen_ablegen(self):
        self.__seite.foto_dazu(self.rahmen_lo, self.rahmen_ru)
        # Weiter mit exakter Eckendefinition
        self.__status = 'Ecke1'
        self.__seite.zeige_ecke1()

    # 2. Aktion je Foto:
    # Ecke 1 abspeichern und Ecke 2 anzeigen
    def ecke1(self, p):
        self.__seite.speichere_ecke1(p)
        self.__status = 'Ecke2'
        self.__seite.zeige_ecke2()

    # 3. Aktion je Foto:
    # Ecke 2 abspeichern und Ecke 3 anzeigen
    def ecke2(self, p):
        self.__seite.speichere_ecke2(p)
        self.__status = 'Ecke3'
        self.__seite.zeige_ecke3()

    # 3. Aktion je Foto:
    # Ecke 3 abspeichern und beschnittenes Foto anzeigen
    def ecke3(self, p):
        self.__seite.speichere_ecke3(p)
        self.__status = 'Foto definiert'
        self.__seite.foto_anzeigen()

    # 4. Aktion je Foto:
    # Beschnittenes Foto speichern und n. Seite bearbeiten
    def foto_speichern(self, p):
        self.__seite.foto_speichern()
        self.__status = 'Foto fertig'
        self.seite_bearbeiten(self.__seiten_nr)

