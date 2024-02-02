import os
import wx

from config import conf

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, x, y, filenames):
        #x,y sind drop-koordinaten, filenames liste der gedroppten files
        myfile = filenames[0]
        if os.path.isdir(myfile):
            conf.pic_path = myfile
            conf.thisapp.seiten_laden()

        if os.path.isfile(myfile):
            conf.thisapp.seiten.foto_neu_beschneiden(myfile)

        return True