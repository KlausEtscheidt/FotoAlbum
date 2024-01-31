import glob 
import os
import logging
import math

import wx

import config as conf

logger = logging.getLogger('album')

#######################################################################################
#
class KEImage(wx.Image):
    @classmethod
    def load_from_file(cls, fullpath2pic):
        # Image von Platte laden
        return wx.Image(fullpath2pic, wx.BITMAP_TYPE_ANY)

    def __init__(self, fullpath2pic=None, aKEImage=None, aBitmap=None):
        if fullpath2pic:
            wx.Image.__init__(self, fullpath2pic, wx.BITMAP_TYPE_ANY)
        elif aKEImage:
            wx.Image.__init__(self,aKEImage)
            # self = aKEImage.Copy()
        elif aBitmap:
            wx.Image.__init__(self, aBitmap.ConvertToImage())    
        else:
            wx.Image.__init__(self)

    def scaled_bitmap(self, faktor):
        new_w = int(self.Width * faktor)
        new_h = int(self.Height * faktor)
        # copy = self.image.Copy()
        new_image = self.Scale(new_w, new_h)
        logger.debug(f'\nnew size: br {new_w} h: {new_h}\n')
        return new_image.ConvertToBitmap()

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
        # copy = self.Copy()
        copy = KEImage(aKEImage=self.Copy())

        return copy.Resize(size, pkt)

    def rotate(self, winkel, p0, interpol ):
        # Bild wird beim Drehen umm offset verschoben => offset zurück liefern und beachten
        offset = wx.Point()
        newimg = self.Rotate(winkel, p0, interpol, offset)
        return KEImage(aKEImage=newimg), offset
    
    @property
    def bitmap(self):
        return self.ConvertToBitmap()


#######################################################################################
#
class Foto():
    
    def __init__(self, parent, p1, p2):

        self.parent = parent # umgebenden Seite
        self.p1 = p1 # äußerer Rahmen links oben
        self.p2 = p2 # äußerer Rahmen rechts unten
        self.ecke1 = None
        self.ecke2 = None
        self.ecke3 = None
        self.rahmen_plus = -5 # Rahmen gegenüber Daten aus Ecken 1-3 vergrössern (wenn >0)
        self.fertig = False # wird True wenn Foto vollständig definiert

        # Bildausschnitt aus Origbild entsprechend des Grob-Rahmens ums Foto
        # Wird nach Definition des Rahmens erzeugt und behalten
        # Muss nach Abspeichern der Seite entfernt werden               
        # self.__image = None

    def pos_ist_innen(self, x, y):
        return x>=self.p1.x and x<=self.p2.x and y>=self.p1.y and y<=self.p2.y
    
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

    # @property
    # def image(self):
    #     # if self.__image == None:
    #     #     # Hole Bildausschnitt aus Gesamtseite
    #     #     new_image = self.parent.origbild.crop(self.p1, self.p2)
    #     #     self.image = new_image
    #     # return self.__image

    #     # Hole Bildausschnitt aus Gesamtseite
    #     new_image = self.parent.origbild.crop(self.p1, self.p2)
    #     return new_image

    # @image.setter
    # def image(self, x):
    #     self.__image = x
 
    # def free_image(self):
    #     self.image = None

    def __str__(self):
        _, grad = self.drehung
        txt = f'x0 {self.x0} y0 {self.y0} breit {self.breite} hoch {self.hoehe}'
        txt += f' winkel {grad:5.4f}° rahmen plus {self.rahmen_plus}'
        return txt
