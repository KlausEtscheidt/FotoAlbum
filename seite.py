import logging
#import time
import glob 
import os

import wx

import config as conf

from fotos import KEImage, Foto

logger = logging.getLogger('album')

class Seite():

    imagepanel = None
    # imagectrl = None
    base_scale = conf.SCALE_SEITE

    d_aussen = 200
    d_innen = 800

    def __init__(self, fullpath2pic):
        
        self.fullpath2pic = fullpath2pic
        self.path, self.picname = os.path.split(self.fullpath2pic)
        self.basename, self.typ = os.path.splitext(self.picname)
               
        self.__origbild = None
        self.fotos = [] # Liste der Fotos auf Seite Typ KEImage
        self.akt_foto = None

        Foto.imagepanel = self.imagepanel

    def show_origbild(self):
        bitmap = self.origbild.scaled_bitmap(self.base_scale)
        self.imagepanel.show_pic(bitmap)

    # Teilfoto in Liste aufnehmen
    def foto_dazu(self, p1, p2):
        # Erzeuge KEImage und lege in Liste ab
        foto = Foto(self, p1, p2)
        self.fotos.append(foto)
        # bitmap = foto.scaled_bitmap(.5)
        # self.imagepanel.show_pic(bitmap)       
        self.akt_foto = foto
        # self.save(foto, '_1')

    def save(self, foto, suffix):
        new_name = self.basename + suffix + self.typ
        fname = os.path.join(self.path, new_name)
        foto.save(fname)

    def zeige_ecke1(self):
        x = self.akt_foto.p1.x
        y = self.akt_foto.p1.y
        p1 = wx.Point(x - self.d_aussen, y - self.d_aussen)
        p2 = wx.Point(x + self.d_innen, y + self.d_innen)
        new_image = KEImage(self.origbild.crop(p1, p2))
        # self.save(new_image, '_2')
        bitmap = new_image.scaled_bitmap(1.)
        self.imagepanel.show_pic(bitmap)

    def zeige_ecke2(self):
        x = self.akt_foto.p2.x
        y = self.akt_foto.p1.y
        p1 = wx.Point(x - self.d_innen, y - self.d_aussen)
        p2 = wx.Point(x + self.d_aussen, y + self.d_innen)
        new_image = KEImage(self.origbild.crop(p1, p2))
        bitmap = new_image.scaled_bitmap(.5)
        self.imagepanel.show_pic(bitmap)

    def zeige_ecke3(self):
        x = self.akt_foto.p2.x
        y = self.akt_foto.p2.y
        p1 = wx.Point(x - self.d_innen, y - self.d_innen)
        p2 = wx.Point(x + self.d_aussen, y + self.d_aussen)
        new_image = KEImage(self.origbild.crop(p1, p2))
        bitmap = new_image.scaled_bitmap(1.)
        self.imagepanel.show_pic(bitmap)

   
    @property
    def origbild(self):
        if not self.__origbild: 
            # Image von Platte laden
            myimage = KEImage.load_from_file(self.fullpath2pic)
            # Instanz erzeugen
            self.__origbild = KEImage(myimage)
        return self.__origbild

    # @origbild.setter
    # def origbild(self, x):
    #     self.origbild = x


class Seiten(list):

    seiten_nr = 0

    def __init__(self, imagepanel):
        
        super().__init__()

        Seite.imagepanel = imagepanel
        Seite.imagectrl = imagepanel.imagectrl

        # Suche Bilder    
        self.myFileList = glob.glob(conf.pic_path + "\*" + conf.pic_type)
        
        # Fuer jeden gefundenen Pfad, Seitenobjekt erzeugen und merken
        for fullpath in self.myFileList:
            seite = Seite(fullpath)
            self.append(seite)
        
        msg = f'Liste mit {len(self):d} Bildern geladen.'
        conf.mainframe.SetStatusText(msg)
        logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')
    
