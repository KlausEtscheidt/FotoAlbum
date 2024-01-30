import logging
#import time
#import glob 
import os

import wx

from wand.image import Image as wandImage
from wand.display import display
import zeichenfabrik

import config as conf

from fotos import KEImage, Foto

logger = logging.getLogger('album')

#####################################################################################
#
# Seite
#
#####################################################################################

class Seite():

    #inneres panel
    imagepanel = None
    
    base_scale = conf.SCALE_SEITE

    d_aussen = 200
    d_innen = 1400

    def __init__(self, fullpath2pic):
        
        self.fullpath2pic = fullpath2pic
        self.path, self.picname = os.path.split(self.fullpath2pic)
        self.basename, self.typ = os.path.splitext(self.picname)

        # Origbild wird bei der 1. Verwendung erzeugt und behalten
        # Muss beim Verlassen der Seite entfernt werden               
        self.__origbild = None
        self.fotos = [] # Liste der Fotos auf Seite Typ KEImage
        self.akt_foto = None

        Foto.imagepanel = self.imagepanel

    # Properties
    #############################################################################
    @property
    def targetname(self):
        new_name = self.basename + f'_{len(self.fotos):02d}' + self.typ
        fname = os.path.join(self.path, conf.pic_output, new_name)
        return fname

    @property
    def origbild(self):
        if not self.__origbild: 
            # Image von Platte laden
            # myimage = KEImage.load_from_file(self.fullpath2pic)
            # Instanz erzeugen
            self.__origbild = KEImage(self.fullpath2pic)
        return self.__origbild

    # @origbild.setter
    # def origbild(self, x):
    #     self.origbild = x


    #############################################################################
    #
    # Ablauf
    #
    #############################################################################

    def show_origbild(self):
        image_bmp = self.origbild.bitmap
        zeichenfabrik.zeichne_rahmen(image_bmp, self)
        self.imagepanel.show_pic(image_bmp, zeichenfabrik.zbmp , conf.SCALE_SEITE)
        #self.imagepanel.innerpanel.show_pic

    # Teilfoto in Liste aufnehmen
    def foto_dazu(self, p1, p2):
        # Erzeuge KEImage und lege in Liste ab
        foto = Foto(self, p1, p2)
        self.fotos.append(foto)
        self.akt_foto = foto
        
    def zeige_ecke1(self):
        x = self.akt_foto.p1.x
        y = self.akt_foto.p1.y
        p1 = wx.Point(x - self.d_aussen, y - self.d_aussen)
        p2 = wx.Point(x + self.d_innen, y + self.d_innen)
        self.__zeige_ecke(p1, p2, 1)

    def zeige_ecke2(self):
        x = self.akt_foto.p2.x
        y = self.akt_foto.p1.y
        p1 = wx.Point(x - self.d_innen, y - self.d_aussen)
        p2 = wx.Point(x + self.d_aussen, y + self.d_innen)
        # lage von ecke1.y zu p1
        ecke1_y = self.akt_foto.ecke1.y -y + self.d_aussen
        
        self.__zeige_ecke(p1, p2, 2, ecke1_y)

    def zeige_ecke3(self):
        x = self.akt_foto.p2.x
        y = self.akt_foto.p2.y
        p1 = wx.Point(x - self.d_innen, y - self.d_innen)
        p2 = wx.Point(x + self.d_aussen, y + self.d_aussen)
        # lage von ecke2.x zu p1
        ecke2_x = self.akt_foto.ecke2.x -x + self.d_innen
        self.__zeige_ecke(p1, p2, 3, ecke2_x)

    def __zeige_ecke(self, p1, p2, nr, linie=None):
        new_image = self.origbild.crop(p1, p2)
        image_bmp = new_image.ConvertToBitmap()
        # self.imagepanel.show_pic(bitmap, scale=conf.SCALE_ECKE)
        if nr == 1:
            zbmp = None
        if nr == 2:
            zeichenfabrik.zeichne_ecke(image_bmp,  linie, None)
            zbmp = zeichenfabrik.zbmp
        if nr == 3:
            zeichenfabrik.zeichne_ecke(image_bmp, None, linie)
            zbmp = zeichenfabrik.zbmp
        self.imagepanel.show_pic(image_bmp, zbmp , scale=conf.SCALE_ECKE)

    def speichere_ecke1(self, p):
        # p = self.unscale(p, conf.SCALE_ECKE)
        # x0 war p1.x - self.d_aussen => x_absolut
        x_abs = p.x + self.akt_foto.p1.x - self.d_aussen
        # y0 war p1.y - self.d_aussen => y_absolut
        y_abs = p.y + self.akt_foto.p1.y - self.d_aussen
        self.akt_foto.ecke1 = wx.Point(x_abs, y_abs)
        logger.debug(f'speichere Ecke 1 x: {x_abs} y: {y_abs}')

    def speichere_ecke2(self, p):
        # p = self.unscale(p, conf.SCALE_ECKE)
        # x0 war p2.x - self.d_innen => x_absolut
        x_abs = p.x + self.akt_foto.p2.x - self.d_innen
        # y0 war p1.y - self.d_aussen => y_absolut
        y_abs = p.y + self.akt_foto.p1.y - self.d_aussen
        self.akt_foto.ecke2 = wx.Point(x_abs, y_abs)
        logger.debug(f'speichere Ecke 2 x: {x_abs} y: {y_abs}')

    def speichere_ecke3(self, p):
        # p = self.unscale(p, conf.SCALE_ECKE)
        # x0 war p2.x - self.d_innen => x_absolut
        x_abs = p.x + self.akt_foto.p2.x - self.d_innen
        # y0 war p2.y - self.d_innen => y_absolut
        y_abs = p.y + self.akt_foto.p2.y - self.d_innen
        self.akt_foto.ecke3 = wx.Point(x_abs, y_abs)
        logger.debug(f'speichere Ecke 3 x: {x_abs} y: {y_abs}')

    def foto_anzeigen(self):

        foto = self.akt_foto
        rad, grad = foto.drehung
        orig = self.origbild
        logger.info(f'Foto {foto}')

        if abs(grad) > conf.MIN_WINKEL:
            neu_image, offset = orig.rotate(rad, foto.ecke1, False)
        else:
            neu_image = orig
            offset = wx.Point(0, 0)

        p1 = wx.Point(foto.ecke1.x - offset.x + conf.SHRINK, foto.ecke1.y - offset.y + conf.SHRINK)
        p2 = wx.Point(p1.x + foto.breite - 2*conf.SHRINK, p1.y + foto.hoehe - 2*conf.SHRINK)
        neu_image = neu_image.crop(p1, p2)
        self.save(neu_image, f'_{len(self.fotos):02d}')

        bitmap = neu_image.bitmap
        self.imagepanel.show_pic(bitmap, scale=conf.SCALE_KONTROLLBILD)

    def foto_speichern(self):
        foto = self.akt_foto
        rad, grad = foto.drehung

        with wandImage(filename=self.fullpath2pic) as img:
            if abs(grad) > conf.MIN_WINKEL:
                img.distort('scale_rotate_translate', (foto.ecke1.x, foto.ecke1.y, -grad,))
            x0 = foto.ecke1.x + conf.SHRINK
            y0 = max(0, foto.ecke1.y + conf.SHRINK) # nie <0
            breite = foto.breite - 2*conf.SHRINK
            hoehe = foto.hoehe - 2*conf.SHRINK
            img.crop(x0, y0, x0 + breite, y0 + hoehe)
            tname = self.get_target_w_appendixname('wand')
            img.save(filename=tname)
            # display(img)
        # foto.free_image()

    ###################################################################################
    #
    # Helper
    #
    ###################################################################################
    def free_origbild(self):
        self.__origbild = None

    def save(self, keimage, suffix):
        new_name = self.basename + suffix + self.typ
        fname = os.path.join(self.path, conf.pic_output, new_name)
        keimage.SaveFile(fname)

    def get_target_w_appendixname(self, apdx):
        new_name = self.basename + f'_{len(self.fotos):02d}_{apdx}' + self.typ
        fname = os.path.join(self.path, conf.pic_output, new_name)
        return fname

#####################################################################################
#
# Seiten
#
#####################################################################################

class Seiten(list):

    seiten_nr = 0

    def __init__(self):
        
        super().__init__()


        # Suche Bilder    
        self.myFileList = glob.glob(conf.pic_path + "\*" + conf.pic_type)
        
        # Fuer jeden gefundenen Pfad, Seitenobjekt erzeugen und merken
        for fullpath in self.myFileList:
            seite = Seite(fullpath)
            self.append(seite)
        
        msg = f'Liste mit {len(self):d} Bildern geladen.'
        if conf.mainframe:
            conf.mainframe.SetStatusText(msg)
        logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')
    
