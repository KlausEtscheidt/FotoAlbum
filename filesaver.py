"""
filesaver.py
------------
Abspeichern von Bild-Dateien im thread.

Im Workerthread werden das Kontrollbild (jpg) und das Tiff abgespeichert.
Der Thread sendet per Event (ResultEvent) seinen Status und evtl. Fehler ans Hauptprogramm.
"""

import logging
from threading import Thread

import wx

from wand.image import Image as wandImage
import zeichenfabrik

from config import conf

from fotos import KEImage


logger = logging.getLogger('album')

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

class ResultEvent(wx.PyEvent):
    '''Eventklasse'''

    def __init__(self, data, had_err = False):
        '''Event um den Status des Threads an das Hauptprogramm zu melden.

        Args:
            data (str): Meldung, die zurück gesendet werden soll
            had_err (bool, optional): True wenn ein Fehler auftrat. Defaults to False.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        self.had_err = had_err

class WorkerThread(Thread):
    '''Thread-Klasse zum Abspeichern von Images'''

    def __init__(self, notify_window, foto):
        '''Tread-Klasse zum Abspeichern

        Args:
            notify_window (wx.window): Window, das die Events erhält.
            foto (Foto): Foto-Objekt, das gespeichert werden soll.
        '''
        Thread.__init__(self)
        self._notify_window = notify_window #Fenster das Events bekommt
        self.foto = foto
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Führt das Abspeichern aus."""

        foto = self.foto

        # Erst Kontrollbild
        wx.PostEvent(self._notify_window, ResultEvent('Speichere Kontrollbild'))
        bmp = zeichenfabrik.zeichne_clip_rahmen_ins_bild(foto.seite.bild_gedreht.bitmap,
                                                         foto, conf.rand, foto.rahmen_plus)
        my_ke_image = KEImage(mybitmap=bmp)
        fname = foto.get_targetname('.jpg')
        my_ke_image.save_as_jpg(fname)

        _, grad = foto.drehung

        wx.PostEvent(self._notify_window, ResultEvent('Speichere Tiff'))
        try:
            fname = foto.seite.fullpath2pic
            with wandImage(filename=fname) as img:
                img = wandImage(filename=fname)
                #Falls im Tiff Leerraum ums Bild ist (Kontrolle z.b in Gimp)
                img.reset_coords()
                if abs(grad) > conf.min_winkel:
                    img.distort('scale_rotate_translate', (foto.ecke1.x, foto.ecke1.y, -grad,))
                # x0, y0, x1, y1 = foto.final_crop_frame
                crop_frame = foto.final_crop_frame
                # img.crop(x0, y0, x1, y1)
                img.crop(*crop_frame)
                fname = foto.get_targetname('.tif')
                foto.saved_in = fname
                img.save(filename=fname)
                wx.PostEvent(self._notify_window, ResultEvent('Tiff gespeichert'))
        except Exception as wand_err:
            wx.PostEvent(self._notify_window, ResultEvent(str(wand_err), True))

    def abort(self):
        """abort worker thread.
        Wird nicht benutzt und erfordert eine Abfrage von self._want_abort in run."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
