import logging
import time

import wx

import config as conf

from bilderliste import BilderListe

logger = logging.getLogger('album')

class Seite():

    imagepanel = None
    imagectrl = None

    def __init__(self, bild):
        self.__origbild = bild
        self.base_scale = 0.1

    def show_origbild(self):
        bitmap = self.__origbild.scaled_bitmap(0.1)
        self.imagepanel.show_pic(bitmap)

    def show_framed(self, pos1, pos2):
        #Skalierung beachten
        p1 = self.koor_trans(pos1)
        p2 = self.koor_trans(pos2)
        bitmap = self.__origbild.crop(p1, p2, 10*self.base_scale)
        self.imagepanel.show_pic(bitmap)

    def koor_trans(self, p):
        p_trans = wx.Point(0,0)
        rand = self.imagepanel.rand
        p_trans.x = int( (p.x - rand) / self.base_scale)
        p_trans.y = int( (p.y - rand) / self.base_scale)
        return p_trans

class Seiten(BilderListe):

    seiten_nr = 0

    def __init__(self, imagepanel):
        
        super().__init__(conf.pic_path, conf.pic_type)

        Seite.imagepanel = imagepanel
        Seite.imagectrl = imagepanel.imagectrl

        # self.seiten = BilderListe(conf.pic_path, conf.pic_type)
        msg = f'Liste mit {len(self):d} Bildern geladen.'
        conf.mainframe.SetStatusText(msg)
        logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')

