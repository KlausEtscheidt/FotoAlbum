import logging
import os
from pathlib import Path
from threading import Thread

import wx

from wand.image import Image as wandImage
from wand.display import display
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

    #inneres panel
    imagepanel = None
    
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

        Foto.imagepanel = self.imagepanel

    # Properties
    #############################################################################
    @property
    def targetname(self):
        new_name = self.basename + f'_{len(self.fotos):02d}' + self.typ
        fname = os.path.join(self.path, conf.pic_output, new_name)
        return fname

    #############################################################################
    #
    # Allgemeine Funktionen

    def seite_drehen(self):
        if self.seitenbild:
            self.seitenbild = KEImage(aKEImage=self.seitenbild.Rotate90())
            self.seite_anzeigen()

    def seite_speichern(self):
        if self.seitenbild:
            thread = Thread(target=self.__seite_speichern)
            thread.start()
    
    def __seite_speichern(self):
        self.seitenbild.SaveFile(self.fullpath2pic)

    
    #############################################################################
    #
    # Ablauf (Funktionen, die der Reihe nach durch Mausklicks getriggert werden)
    #
    #############################################################################

    def seite_laden(self):
        # KEImage des Seiten-Tiffs erzeugen und als Klassenvariable merken
        self.seitenbild = KEImage(self.fullpath2pic)
        self.seite_anzeigen()

    def seite_anzeigen(self):
        image_bmp = self.seitenbild.bitmap
        zeichenfabrik.zeichne_rahmen(image_bmp, self)
        self.imagepanel.show_pic(image_bmp, zeichenfabrik.zbmp , conf.SCALE_SEITE)

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
        new_image = self.seitenbild.crop(p1, p2)
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

    # def foto_anzeigen(self):
    def foto_drehen(self):

        foto = self.akt_foto
        rad, grad = foto.drehung
        orig = self.seitenbild
        logger.info(f'Foto {foto}')

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
        # Anzeige
        foto = self.akt_foto
        image_bmp = self.bild_gedreht.bitmap
        zeichenfabrik.zeichne_clip_rahmen(image_bmp, foto, conf.RAND, foto.rahmen_plus)
        self.imagepanel.show_pic(image_bmp, zeichenfabrik.zbmp , scale=conf.SCALE_KONTROLLBILD)

    def foto_beschneiden(self, plusminus):
        foto = self.akt_foto
        if plusminus == '+':
            foto.rahmen_plus += conf.rahmen_plus
        else:
            foto.rahmen_plus -= conf.rahmen_plus
        self.foto_anzeigen()

    def __foto_speichern_im_thread(self):

        foto = self.akt_foto
        foto.fertig = True

        # Erst Kontrollbild
        bmp = zeichenfabrik.zeichne_clip_rahmen_ins_bild(self.bild_gedreht.bitmap, foto, conf.RAND, foto.rahmen_plus)
        aKEImage = KEImage(aBitmap=bmp)
        self.save(aKEImage, f'_{len(self.fotos):02d}', '.jpg')

        rad, grad = foto.drehung

        try:
            with wandImage(filename=self.fullpath2pic) as img:
                #Falls im Tiff Leerraum ums Bild ist (Kontrolle z.b in Gimp)
                img.reset_coords()
                if abs(grad) > conf.MIN_WINKEL:
                    img.distort('scale_rotate_translate', (foto.ecke1.x, foto.ecke1.y, -grad,))
                # tname = self.get_targetname_w_appendix('rot')
                # img.save(filename=tname)
                x0 = max(0, foto.ecke1.x - foto.rahmen_plus)
                y0 = max(0, foto.ecke1.y - foto.rahmen_plus) # nie <0
                x1 = min(self.seitenbild.Width, x0 + foto.breite + 2*foto.rahmen_plus)
                y1 = min(self.seitenbild.Height, y0 + foto.hoehe + 2*foto.rahmen_plus)
                logger.debug(f'final crop x0: {x0} y0: {y0} x1: {x1} y1: {y1}')
                img.crop(x0, y0, x1, y1)
                tname = self.get_targetname_w_appendix('')
                foto.saved_in = tname
                img.save(filename=tname)
                # display(img)
        except Exception as wand_err:
            logger.exception('Fehler in wand')

    def foto_speichern(self):

        thread = Thread(target=self.__foto_speichern_im_thread)
        thread.start()


    ###################################################################################
    #
    # Helper
    #
    ###################################################################################
    def save(self, keimage, suffix, typ):
        new_name = self.basename + suffix + typ
        path = os.path.join(self.path, conf.pic_output)
        fname = os.path.join(path, new_name)
        #Pfad anlegen, wenn nicht vorhanden
        Path(path).mkdir(parents=True, exist_ok=True)
        if typ == '.tif':
            keimage.SaveFile(fname)
        if typ == '.jpg':
            keimage.bitmap.SaveFile (fname, wx.BITMAP_TYPE_JPEG)

    def get_targetname_w_appendix(self, apdx):
        new_name = self.basename + f'_{len(self.fotos):02d}_{apdx}' + self.typ
        path = os.path.join(self.path, conf.pic_output)
        fname = os.path.join(path, new_name)
        #Pfad anlegen, wenn nicht vorhanden
        Path(path).mkdir(parents=True, exist_ok=True)
        return fname

