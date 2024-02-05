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
    @classmethod
    def load_from_file(cls, fullpath2pic):
        # Image von Platte laden
        return wx.Image(fullpath2pic, wx.BITMAP_TYPE_ANY)

    def __init__(self, fullpath2pic=None, aImage=None, aBitmap=None):
        if fullpath2pic:
             self.__image = wx.Image(fullpath2pic, wx.BITMAP_TYPE_ANY)
        elif aImage:
            self.__image = aImage
            # self = aKEImage.Copy()
        elif aBitmap:
            self.__image = aBitmap.ConvertToImage()
        # else:
        #     wx.Image.__init__(self)
        if not self.__image.IsOk:
            raise Exception('image in KEImage fehlerhaft')

    def crop(self, pos1, pos2):
        """crop erzeugt Bildausschnitt

        :param pos1: linke obere Ecke
        :type pos1: wx.Point
        :param pos2: rechte untere Ecke
        :type pos2: wx.Point
        :return: gecropptes Image
        :rtype: wx.Image
        """
        #logger.debug(f'crop x1 {pos1.x} y1 {pos1.y} x2 { pos2.x} y2 { pos2.y}')
        w = pos2.x - pos1.x
        h = pos2.y - pos1.y
        size = wx.Size(w,h)
        pkt = wx.Point(-pos1.x, -pos1.y)
        copy = self.__image.Copy()
        copy.Resize(size, pkt)

        return KEImage(aImage=copy)

    def rotate(self, winkel, p0, interpol ):
        # Bild wird beim Drehen umm offset verschoben => offset zurück liefern und beachten
        offset = wx.Point()
        newimg = self.__image.Rotate(winkel, p0, interpol, offset)
        return KEImage(aImage=newimg), offset

    def SaveFile(self, fullpath):
        self.__image.SaveFile(fullpath)
    
    def SaveAsJpg(self, fullpath):
        self.bitmap.SaveFile(fullpath, wx.BITMAP_TYPE_JPEG)

    @property
    def bitmap(self):
        return self.__image.ConvertToBitmap()

    @property
    def Width(self):
        return self.__image.Width

    @property
    def Height(self):
        return self.__image.Height


#######################################################################################
#
class Foto():
    '''Foto alle Daten um ein Teilfoto zu definieren'''
    
    def __init__(self, parent, nr, p1, p2):

        self.parent = parent # umgebenden Seite
        self.nr = nr # laufende Nr auf der Seite
        self.p1 = p1 # äußerer Rahmen links oben
        self.p2 = p2 # äußerer Rahmen rechts unten
        self.ecke1 = None
        self.ecke2 = None
        self.ecke3 = None
        self.rahmen_plus = conf.rahmen_plus # Rahmen gegenüber Daten aus Ecken 1-3 vergrössern (wenn >0)
        self.fertig = False # wird True wenn Foto vollständig definiert
        self.saved_in = '' # Pfad zur Ausgabedatei

        # Bildausschnitt aus Origbild entsprechend des Grob-Rahmens ums Foto
        # Wird nach Definition des Rahmens erzeugt und behalten
        # Muss nach Abspeichern der Seite entfernt werden               
        # self.__image = None

    def pos_ist_innen(self, x, y):
        return x>=self.p1.x and x<=self.p2.x and y>=self.p1.y and y<=self.p2.y

    def get_targetname(self, typ, appendix=''):
        new_name = self.parent.basename + f'_{self.nr:02d}{appendix}' + typ
        path = os.path.join(self.parent.path, conf.pic_output)
        fname = os.path.join(path, new_name)
        #Pfad anlegen, wenn nicht vorhanden
        Path(path).mkdir(parents=True, exist_ok=True)
        return fname

    @property
    def drehung(self):
        dy = self.ecke2.y - self.ecke1.y
        dx = self.ecke2.x - self.ecke1.x
        rad = math.atan2(dy, dx)
        return rad, math.degrees(rad)

    @property
    def breite(self):
        dy = self.ecke2.y - self.ecke1.y
        dx = self.ecke2.x - self.ecke1.x
        return int(math.sqrt(dx*dx + dy*dy))

    @property
    def hoehe(self):
        dy = self.ecke2.y - self.ecke3.y
        dx = self.ecke2.x - self.ecke3.x
        return int(math.sqrt(dx*dx + dy*dy))

    @property
    def x0(self):
        return self.ecke1.x

    @property
    def y0(self):
        return self.ecke1.y

    @property
    def final_crop(self):
        x0 = max(0, self.ecke1.x - self.rahmen_plus)
        y0 = max(0, self.ecke1.y - self.rahmen_plus) # nie <0
        x1 = min(self.parent.seitenbild.Width, x0 + self.breite + 2*self.rahmen_plus)
        y1 = min(self.parent.seitenbild.Height, y0 + self.hoehe + 2*self.rahmen_plus)
        return x0, y0, x1, y1

    def __str__(self):
        _, grad = self.drehung
        txt = f'x0 {self.x0} y0 {self.y0} breit {self.breite} hoch {self.hoehe}'
        txt += f' winkel {grad:5.4f}° rahmen plus {self.rahmen_plus}'
        return txt
