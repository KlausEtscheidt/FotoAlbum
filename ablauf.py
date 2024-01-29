import logging

import wx

import config as conf
from seite import Seiten, Seite

logger = logging.getLogger('album')


class Ablauf:

    def __init__(self, imagepanel):
        # Klassenvar setzen
        Seite.imagepanel = imagepanel
        Seite.imagectrl = imagepanel.imagectrl
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

    # Foto anhand Rahmen erzeugen und ablegen
    def foto_rahmen_ablegen(self):
        self.__seite.foto_dazu(self.rahmen_lo, self.rahmen_ru)
        # Weiter mit exakter Eckendefinition
        self.__status = 'Ecke1'
        self.__seite.zeige_ecke1()

    def ecke1(self, p):
        self.__seite.speichere_ecke1(p)
        self.__status = 'Ecke2'
        self.__seite.zeige_ecke2()

    def ecke2(self, p):
        self.__seite.speichere_ecke2(p)
        self.__status = 'Ecke3'
        self.__seite.zeige_ecke3()

    def ecke3(self, p):
        self.__seite.speichere_ecke3(p)
        self.__status = 'Ende Foto'
        self.__seite.ausgeben()
        self.seite_bearbeiten(self.__seiten_nr)

        # elif self.__status == 'Ende Seite':
        #     self.seite_bearbeiten_next()

    def dateiliste_erstellen(self):
        # Filenamen der Seiten-Tiffs einlesen
        # Seiten erzeugen (ohne image) und in Liste merken
        self.__seiten = Seiten()

    def seite_bearbeiten(self, seiten_nr):
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
            self.__seiten_nr += 1
            self.seite_bearbeiten(self.__seiten_nr)

    def seite_bearbeiten_prev(self):
        if self.__seiten_nr > 0:
            self.__seiten_nr -= 1
            self.seite_bearbeiten(self.__seiten_nr)



