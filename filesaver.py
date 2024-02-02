import logging
import os
import shutil
from threading import *
import wx

from wand.image import Image as wandImage
import zeichenfabrik

from config import conf

from fotos import KEImage, Foto


logger = logging.getLogger('album')

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

# def EVT_RESULT(win, func):
#     """Define Result Event."""
#     win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data, had_err = False):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        self.had_err = had_err

# Thread class that executes processing
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, foto):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window #Fenster das Events bekommt
        self.foto = foto
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Worker Thread."""

        foto = self.foto

        # Erst Kontrollbild
        wx.PostEvent(self._notify_window, ResultEvent('Speichere Kontrollbild'))
        bmp = zeichenfabrik.zeichne_clip_rahmen_ins_bild(foto.parent.bild_gedreht.bitmap, foto, conf.RAND, foto.rahmen_plus)
        aKEImage = KEImage(aBitmap=bmp)
        fname = foto.get_targetname('.jpg')
        aKEImage.SaveAsJpg(fname)

        _, grad = foto.drehung

        wx.PostEvent(self._notify_window, ResultEvent('Speichere Tiff'))
        try:
            # imagecopy_fname = self.seite.fullpath2pic+'.tif'
            # shutil.copy(self.seite.fullpath2pic, imagecopy_fname)
            fname = foto.parent.fullpath2pic
            with wandImage(filename=fname) as img:
                img = wandImage(filename=fname)
                #Falls im Tiff Leerraum ums Bild ist (Kontrolle z.b in Gimp)
                img.reset_coords()
                if abs(grad) > conf.MIN_WINKEL:
                    img.distort('scale_rotate_translate', (foto.ecke1.x, foto.ecke1.y, -grad,))
                x0, y0, x1, y1 = foto.final_crop
                # logger.debug(f'final crop x0: {x0} y0: {y0} x1: {x1} y1: {y1}')
                img.crop(x0, y0, x1, y1)
                fname = foto.get_targetname('.tif')
                foto.saved_in = fname
                img.save(filename=fname)
                # os.remove(imagecopy_fname)
                # display(img)
                wx.PostEvent(self._notify_window, ResultEvent('Tiff gespeichert'))
        except Exception as wand_err:
            wx.PostEvent(self._notify_window, ResultEvent(str(wand_err), True))
            # logger.exception('Fehler in wand')
            # wx.MessageBox('Fehler in wand')

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
