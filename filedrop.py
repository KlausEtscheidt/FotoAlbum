import os
import wx

import config

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, x, y, filenames):
        #x,y sind drop-koordinaten, filenames liste der gedroppten files
        myfile = filenames[0]
        if os.path.isdir(myfile):
            config.pic_path = myfile
            config.thisapp.seiten_laden()

        return True