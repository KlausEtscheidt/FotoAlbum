"""
filedrop.py
-----------
Ermöglicht drop von Verzeichnissen oder Dateien

Bei Verzeichnissen werden die vorhandenen Tiffs  eingelesen und angezeigt.
Bei Dateien wird die Ursprungsseite gesucht und das Foto wird zum resize angeboten.
"""

import os
import wx

from config import conf

class MyFileDropTarget(wx.FileDropTarget):
    '''Ermöglicht drop von Verzeichnissen oder Dateien.'''
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, _x, _y, filenames): # pylint: disable=invalid-name, missing-function-docstring
        #x,y sind drop-koordinaten, filenames liste der gedroppten files
        myfile = filenames[0]
        if os.path.isdir(myfile):
            conf.pic_path = myfile
            conf.thisapp.seiten_laden()

        if os.path.isfile(myfile):
            conf.thisapp.seiten.foto_neu_beschneiden(myfile)

        return True
