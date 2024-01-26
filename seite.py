import logging
import time

import wx

import config as conf

from bilderliste import BilderListe

logger = logging.getLogger('album')

class Seite():

    imagectrl = None

    def __init__(self, bild):
        self.__origbild = bild
        self.base_scale = 0.1

    def show_origbild(self):
        bitmap = self.__origbild.scaled_bitmap(0.1)
        conf.mainframe.imagepanel.show_pic(bitmap)

    def show_framed(self, pos1, pos2):
        #Skalierung beachten
        pos1.x = int(pos1.x  / self.base_scale)
        pos1.y = int(pos1.y  / self.base_scale)
        pos2.x = int(pos2.x  / self.base_scale)
        pos2.y = int(pos2.y  / self.base_scale)
        bitmap = self.__origbild.crop(pos1, pos2, self.base_scale)
        conf.mainframe.imagepanel.show_pic(bitmap)

class Seiten(BilderListe):

    seiten_nr = 0

    def __init__(self, imagectrl):
        
        super().__init__(conf.pic_path, conf.pic_type)

        Seite.imagectrl = imagectrl

        # self.seiten = BilderListe(conf.pic_path, conf.pic_type)
        msg = f'Liste mit {len(self):d} Bildern geladen.'
        conf.mainframe.SetStatusText(msg)
        logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')

