import glob 
import os
import logging
import math

import wx

import config as conf

logger = logging.getLogger('album')

#######################################################################################
#
class KEImage():
    @classmethod
    def load_from_file(cls, fullpath2pic):
        # Image von Platte laden
        return wx.Image(fullpath2pic, wx.BITMAP_TYPE_ANY)

    def __init__(self, image):
        self.__image = image

    def scaled_bitmap(self, faktor):
        myimage = self.image
        new_w = int(myimage.Width * faktor)
        new_h = int(myimage.Height * faktor)
        # copy = self.image.Copy()
        new_image = self.image.Scale(new_w, new_h)
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
        logger.debug(f'crop x1 {pos1.x} y1 {pos1.y} x2 { pos2.x} y2 { pos2.y}')
        w = pos2.x - pos1.x
        h = pos2.y - pos1.y
        size = wx.Size(w,h)
        pkt = wx.Point(-pos1.x, -pos1.y)
        copy = self.image.Copy()
        return copy.Resize(size, pkt)

    def rotate(self, winkel, p0, interpol ):
        return self.image.Rotate(winkel, p0, interpol)

    def save(self, fname):
        self.image.SaveFile(fname)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, x):
        self.__image = x

    #Behelf, weil image.setter aus abgeleiteten Klassen nicht geht
    def set_image(self, x):
        self.__image = x

#######################################################################################
#
class Foto(KEImage):
    
    def __init__(self, parent, p1, p2):
        super(Foto,self).__init__(None)

        self.parent = parent # umgebenden Seite
        self.p1 = p1 # äußerer Rahmen links oben
        self.p2 = p2 # äußerer Rahmen rechts unten
        self.ecke1 = None
        self.ecke2 = None
        self.ecke3 = None
        self.__image = None

    @property
    def drehung(self):
        dy = self.ecke2.y - self.ecke1.y
        dx = self.ecke2.x - self.ecke1.x
        return math.atan2(dy, dx)

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
    def image(self):
        if self.__image == None:
            # Hole Bildausschnitt aus Gesamtseite
            new_image = self.parent.origbild.crop(self.p1, self.p2)
            self.image = new_image
        return self.__image

    @image.setter
    def image(self, x):
        self.__image = x
        # super(Foto,self).image = x
        super(Foto,self).set_image(x)
 
    def free_image(self):
        self.image = None

    def __str__(self):
        txt = f'x0 {self.x0} y0 {self.y0} breit {self.breite} hoch {self.hoehe}'
        txt += f' winkel {self.drehung:5.4f}'
        # txt += f'winkel {self.drehung*math.Pi/180.}'
        return txt
