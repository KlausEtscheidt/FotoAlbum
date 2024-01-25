import logging
import time

import wx

import config as conf

from bilderliste import BilderListe

logger = logging.getLogger('album')
imagectrl = None

def main_loop():
    imagectrl = conf.mainframe.imagepanel.imagectrl
    meine_bilder = BilderListe(conf.pic_path, conf.pic_type)
    msg = f'Liste mit {len(meine_bilder):d} Bildern geladen.'
    conf.mainframe.SetStatusText(msg)
    logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')

    for bild in meine_bilder[conf.BILD_MIN:conf.BILD_MAX]:
        bild.show(imagectrl)
        wx.Yield()
        time.sleep(.5)
