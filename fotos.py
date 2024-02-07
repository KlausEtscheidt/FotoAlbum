"""
fotos.py
====================================
KEImage und FOTO-Klasse
"""

import os
import logging
import math
from pathlib import Path

import wx

from config import conf

logger = logging.getLogger('album')

#######################################################################################
#
class KEImage():
    '''Wrapper um wx.Image'''

    @classmethod
    def load_from_file(cls, fullpath2pic):
        '''Image von Platte laden'''
        return wx.Image(fullpath2pic, wx.BITMAP_TYPE_ANY)

    def __init__(self, fullpath2pic=None, myimage=None, mybitmap=None):
        if fullpath2pic:
            self.__image = wx.Image(fullpath2pic, wx.BITMAP_TYPE_ANY)
        elif myimage:
            self.__image = myimage
        elif mybitmap:
            self.__image = mybitmap.ConvertToImage()
        if not self.__image.IsOk:
            raise Exception('image in KEImage fehlerhaft') # pylint: disable=broad-except

    def crop(self, pos1, pos2):
        '''crop erzeugt Bildausschnitt

        Args:
            pos1 (wx.Point): linke obere Ecke
            pos2 (wx.Point): rechte untere Ecke

        Returns:
            wx.Image: gecropptes Image
        '''
        #logger.debug(f'crop x1 {pos1.x} y1 {pos1.y} x2 { pos2.x} y2 { pos2.y}')
        w = pos2.x - pos1.x
        h = pos2.y - pos1.y
        size = wx.Size(w,h)
        pkt = wx.Point(-pos1.x, -pos1.y)
        copy = self.__image.Copy()
        copy.Resize(size, pkt)

        return KEImage(myimage=copy)

    def rotate(self, winkel, p0, interpol ):
        ''' Bild wird beim Drehen umm offset verschoben => offset zurück liefern und beachten'''
        offset = wx.Point()
        newimg = self.__image.Rotate(winkel, p0, interpol, offset)
        return KEImage(myimage=newimg), offset

    def rotate90(self):
        '''Dreht Bild um 90°'''
        newimg = self.__image.Rotate90()
        return KEImage(myimage=newimg)

    def save_file(self, fullpath):
        '''Speichert Bild unter fullpath'''
        self.__image.SaveFile(fullpath)

    def save_as_jpg(self, fullpath):
        '''Speichert Bild als JPG unter fullpath'''
        self.bitmap.SaveFile(fullpath, wx.BITMAP_TYPE_JPEG)

    @property
    def bitmap(self):
        '''bitmap zum wx.Image'''
        return self.__image.ConvertToBitmap()

    @property
    def width(self):
        '''breite des Bildes'''
        return self.__image.Width

    @property
    def height(self):
        '''Höhe des Bildes'''
        return self.__image.Height


#######################################################################################
#
class Foto():
    '''Foto alle Daten um ein Teilfoto zu definieren'''

    def __init__(self, seite, nr, p1):

        self.seite = seite # umgebenden Seite
        self.nr = nr # laufende Nr auf der Seite
        self.p1 = p1 # äußerer Rahmen links oben
        self.p2 = None # äußerer Rahmen rechts unten
        self.ecke1 = None
        self.ecke2 = None
        self.ecke3 = None
        # Rahmen gegenüber Daten aus Ecken 1-3 vergrössern (wenn >0)
        self.rahmen_plus = conf.rahmen_plus
        self.fertig = False # wird True wenn Foto vollständig definiert
        self.saved_in = '' # Pfad zur Ausgabedatei

    def setze_rahmen_ecke_ru(self, pos):
        '''Speichert die rechte untere Ecke des Grobrahmens'''
        self.p2 = pos

    def pos_ist_innen(self, x, y):
        '''Testet ob ein Punkt innerhalb eines Bildes liegt'''
        return self.p1.x <= x <= self.p2.x and self.p1.y <= y <= self.p2.y

    def get_targetname(self, typ, appendix=''):
        '''Ermittelt den Zielnamen zum Speichern des Fotos

        An den Namen des Quellfotos (Seite) wird die laufende Nr des Fotos
        und ein evtl Appendix angehängt.'''
        new_name = self.seite.basename + f'_{self.nr:02d}{appendix}' + typ
        path = os.path.join(self.seite.path, conf.pic_output)
        fname = os.path.join(path, new_name)
        #Pfad anlegen, wenn nicht vorhanden
        Path(path).mkdir(parents=True, exist_ok=True)
        return fname

    @property
    def drehung(self):
        '''Ermittelt die Drehlage eines Fotos aus dem Vektor von Ecke1->Ecke2'''
        dy = self.ecke2.y - self.ecke1.y
        dx = self.ecke2.x - self.ecke1.x
        rad = math.atan2(dy, dx)
        return rad, math.degrees(rad)

    @property
    def breite(self):
        '''Breite des Image'''
        dy = self.ecke2.y - self.ecke1.y
        dx = self.ecke2.x - self.ecke1.x
        return int(math.sqrt(dx*dx + dy*dy))

    @property
    def hoehe(self):
        '''Höhe des Image'''
        dy = self.ecke2.y - self.ecke3.y
        dx = self.ecke2.x - self.ecke3.x
        return int(math.sqrt(dx*dx + dy*dy))

    # @property
    # def x0(self):
    #     return self.ecke1.x

    # @property
    # def y0(self):
    #     return self.ecke1.y

    @property
    def final_crop_frame(self):

        '''Finaler Beschnitt zum Speichern des Fotos als Tiff.

        Berücksichtigt die gewünschte Änderung des Beschnitts (**self.rahmen_plus**)
        die jedoch in den Grenzen der zugrunde liegenden Seite liegen müssen.

        Returns:
            int: x0, y0, x1, y1 linke obere und rechte untere Ecke des beschnittenen Fotos.
        '''

        # Den gewünschten Beschnitt auf die zugrunde liegenden Seite begrenzen
        x0 = max(0, self.ecke1.x - self.rahmen_plus)
        y0 = max(0, self.ecke1.y - self.rahmen_plus) # nie <0
        x1 = min(self.seite.seitenbild.width, x0 + self.breite + 2*self.rahmen_plus)
        y1 = min(self.seite.seitenbild.height, y0 + self.hoehe + 2*self.rahmen_plus)
        return (x0, y0, x1, y1)

    def __str__(self):
        _, grad = self.drehung
        txt = f'x0 {self.ecke1.x} y0 {self.ecke1.y} breit {self.breite} hoch {self.hoehe}'
        txt += f' winkel {grad:5.4f}° rahmen plus {self.rahmen_plus}'
        return txt
