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
    d_innen = 1400

    def __init__(self, fullpath2pic):
        
        self.fullpath2pic = fullpath2pic
        self.path, self.picname = os.path.split(self.fullpath2pic)
        self.basename, self.typ = os.path.splitext(self.picname)
               
        self.__origbild = None
        self.fotos = [] # Liste der Fotos auf Seite Typ KEImage
        self.akt_foto = None

        Foto.imagepanel = self.imagepanel

    def show_origbild(self):
        bitmap = self.origbild.scaled_bitmap(conf.SCALE_SEITE)
        self.imagepanel.show_pic(bitmap)

    # Teilfoto in Liste aufnehmen
    def foto_dazu(self, p1, p2):
        p1 = self.unscale(p1, conf.SCALE_SEITE)
        p2 = self.unscale(p2, conf.SCALE_SEITE)
        # Erzeuge KEImage und lege in Liste ab
        foto = Foto(self, p1, p2)
        self.fotos.append(foto)
        # bitmap = foto.scaled_bitmap(.5)
        # self.imagepanel.show_pic(bitmap)       
        self.akt_foto = foto
        # self.save(foto, '_1')
        
    def save(self, foto, suffix):
        new_name = self.basename + suffix + self.typ
        fname = os.path.join(self.path, conf.pic_output, new_name)
        foto.save(fname)

    def zeige_ecke1(self):
        x = self.akt_foto.p1.x
        y = self.akt_foto.p1.y
        p1 = wx.Point(x - self.d_aussen, y - self.d_aussen)
        p2 = wx.Point(x + self.d_innen, y + self.d_innen)
        self.__zeige_ecke(p1, p2)

    def zeige_ecke2(self):
        x = self.akt_foto.p2.x
        y = self.akt_foto.p1.y
        p1 = wx.Point(x - self.d_innen, y - self.d_aussen)
        p2 = wx.Point(x + self.d_aussen, y + self.d_innen)
        self.__zeige_ecke(p1, p2)

    def zeige_ecke3(self):
        x = self.akt_foto.p2.x
        y = self.akt_foto.p2.y
        p1 = wx.Point(x - self.d_innen, y - self.d_innen)
        p2 = wx.Point(x + self.d_aussen, y + self.d_aussen)
        self.__zeige_ecke(p1, p2)

    def __zeige_ecke(self, p1, p2):
        new_image = KEImage(self.origbild.crop(p1, p2))
        # self.save(new_image, '_2')
        bitmap = new_image.scaled_bitmap(conf.SCALE_ECKE)
        self.imagepanel.show_pic(bitmap)

    def speichere_ecke1(self, p):
        p = self.unscale(p, conf.SCALE_ECKE)
        # x0 war p1.x - self.d_aussen => x_absolut
        x_abs = p.x + self.akt_foto.p1.x - self.d_aussen
        # y0 war p1.y - self.d_aussen => y_absolut
        y_abs = p.y + self.akt_foto.p1.y - self.d_aussen
        self.akt_foto.ecke1 = wx.Point(x_abs, y_abs)

    def speichere_ecke2(self, p):
        p = self.unscale(p, conf.SCALE_ECKE)
        # x0 war p2.x - self.d_innen => x_absolut
        x_abs = p.x + self.akt_foto.p2.x - self.d_innen
        # y0 war p1.y - self.d_aussen => y_absolut
        y_abs = p.y + self.akt_foto.p1.y - self.d_aussen
        self.akt_foto.ecke2 = wx.Point(x_abs, y_abs)

    def speichere_ecke3(self, p):
        p = self.unscale(p, conf.SCALE_ECKE)
        # x0 war p2.x - self.d_innen => x_absolut
        x_abs = p.x + self.akt_foto.p2.x - self.d_innen
        # y0 war p2.y - self.d_innen => y_absolut
        y_abs = p.y + self.akt_foto.p2.y - self.d_innen
        self.akt_foto.ecke3 = wx.Point(x_abs, y_abs)

    def ausgeben(self):
        foto = self.akt_foto
        orig = self.origbild
        logger.info(f'Foto {foto}')
        neu = orig.rotate(foto.drehung, foto.ecke1, True)
        self.save(KEImage(neu), '_100')
        p2 = wx.Point(foto.ecke1.x + foto.breite, foto.ecke1.y + foto.hoehe)
        neu = KEImage(neu).crop(foto.ecke1, p2)
        self.save(KEImage(neu), '_200')

    def unscale(self, p,  scale):
        p.x = int( p.x / scale)
        p.y = int( p.y / scale)
        return(p)

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
    
