"""
seite.py
=====================================================
Hält die bitmap einer Seite des Fotoalbums.

Dient zur Steuerung des Ablaufs (Div. Funktionen werden von den Evt-Handlern gerufen)
"""

import logging
import os
from threading import Thread

import wx

import filesaver


import zeichenfabrik

from config import conf

from fotos import KEImage, Foto

logger = logging.getLogger('album')

#####################################################################################
#
# Seite
#
#####################################################################################

class Seite():
    '''Verwaltet die Daten einer Seite.

    Speichert das Image der Gesamtseite und des aktuellen Fotos.
    Bearbeitet 

    '''

    # zum Anzeigen von Bitmaps
    mainframe = None


    base_scale = conf.SCALE_SEITE

    d_aussen = 200 # Rand zum Anzeigen der Ecken
    d_innen = 1400

    # temp Speicher (KEImage) des gedrehten Fotos mit Zusatzrand
    # dient zur Anzeige beim Verändern des Cipping-Randes in "foto_beschneiden"
    bild_gedreht = None
    # KEImage des Seiten-Tiffs. Da Klassenvariable wird nur einmal Speicher verbraucht.
    # Wird von seite_laden erzeugt und zugeordnet
    seitenbild = None

    def __init__(self, fullpath2pic):

        self.fullpath2pic = fullpath2pic
        self.path, self.picname = os.path.split(self.fullpath2pic)
        self.basename, self.typ = os.path.splitext(self.picname)

        self.fotos = [] # Liste der Fotos auf Seite Typ KEImage
        self.akt_foto = None

        # Foto.imagepanel = self.imagepanel

    # Properties
    #############################################################################
    @property
    def targetname(self):
        '''Zielpfad zum Speichern eines Bildes'''
        new_name = self.basename + f'_{len(self.fotos):02d}' + self.typ
        fname = os.path.join(self.path, conf.pic_output, new_name)
        return fname

    #############################################################################
    #
    # Allgemeine Funktionen

    def seite_drehen(self):
        '''Dreht die Gesamtseite um 90° und zeigt die Seite neu an.'''
        if self.seitenbild:
            self.seitenbild = KEImage(myimage=self.seitenbild).Rotate90()
            self.seite_anzeigen()

    def seite_speichern(self):
        '''Speichert die Seite auf Platte.'''
        if self.seitenbild:
            thread = Thread(target=self.__seite_speichern)
            thread.start()

    def __seite_speichern(self):
        '''Speichern im thread'''
        self.seitenbild.SaveFile(self.fullpath2pic)


    #############################################################################
    #
    # Ablauf (Funktionen, die der Reihe nach durch Mausklicks getriggert werden)
    #
    #############################################################################

    def seite_laden(self):
        '''Lädt Tif einer Seite und zeigt sie an

        KEImage des Seiten-Tiffs erzeugen und als Klassenvariable merken
        '''

        self.seitenbild = KEImage(self.fullpath2pic)
        self.seite_anzeigen()

    def seite_anzeigen(self):
        '''Stellt die Bitmap der Seite im mainframe dar'''
        image_bmp = self.seitenbild.bitmap
        zbmp = zeichenfabrik.zeichne_rahmen(image_bmp, self)
        self.mainframe.show_pic(image_bmp, zbmp , conf.SCALE_SEITE)

    def neues_foto_anlegen(self, pos):
        '''Legt neues unfertiges Foto an und legt es in self.fotos ab.'''
        foto = Foto(self, len(self.fotos)+1, pos)
        self.fotos.append(foto)
        self.akt_foto = foto


    # def foto_anzeigen(self):
    def foto_drehen(self):
        '''foto drehen, wenn nötig und neue Bitmap self.bild_gedreht erzeugen'''

        foto = self.akt_foto
        rad, grad = foto.drehung
        orig = self.seitenbild
        logger.info('Foto %s', foto)

        # Verdrehung korrigieren wenn nötig.
        # Funktion verschiebt Bild um offset 0 => korrigieren
        if abs(grad) > conf.MIN_WINKEL:
            neu_image, offset = orig.rotate(rad, foto.ecke1, False)
        else:
            neu_image = orig
            offset = wx.Point(0, 0)

        # Korrektur des Offsets und Rand dazu
        p1 = wx.Point(foto.ecke1.x - offset.x - conf.RAND, foto.ecke1.y - offset.y - conf.RAND)
        p2 = wx.Point(p1.x + foto.breite + 2*conf.RAND, p1.y + foto.hoehe + 2*conf.RAND)
        self.bild_gedreht = neu_image.crop(p1, p2)

        self.foto_anzeigen()

    def foto_anzeigen(self):
        '''Anzeige eines beschnittenen und gedrehten Fotos'''
        foto = self.akt_foto
        image_bmp = self.bild_gedreht.bitmap
        zbmp = zeichenfabrik.zeichne_clip_rahmen(image_bmp, foto, conf.RAND, foto.rahmen_plus)
        self.mainframe.show_pic(image_bmp, zbmp , scale=conf.SCALE_KONTROLLBILD)

    def foto_beschneiden(self, plusminus):
        '''Korrektur des Beschnitts mit neuer Anzeige.'''
        foto = self.akt_foto
        if plusminus == '+':
            foto.rahmen_plus -= conf.rahmen_plus
        else:
            foto.rahmen_plus += conf.rahmen_plus
        self.foto_anzeigen()

    def foto_speichern(self):
        '''Abspeichern des Ergebnisses im Thread'''
        foto = self.akt_foto
        foto.fertig = True
        filesaver.WorkerThread(self.mainframe, foto)
