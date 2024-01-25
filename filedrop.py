import os
import wx

import config
# import FileClass
# import DiskImport
# import database

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.parent = parent
        self.dropped_dir = None

    def OnDropFiles(self, x, y, filenames):
        #x,y sind drop-koordinaten, filenames liste der gedroppten files
        myfile = filenames[0]
        if os.path.isfile(myfile):
            pass
            # myfile = FileClass.Video(filenames[0])
            # if myfile.is_video:
            #     config.mainframe.editpanel.Activate()
            #     config.mainframe.editpanel.filedropped(myfile)
        else:
            self.dropped_dir = myfile
            menu = self.MakePopUpMenu()
            self.parent.PopupMenu(menu, (x, y))

        return True

    def MakePopUpMenu(self):
        menu = wx.Menu()
        m_readDir = menu.Append(-1, 'einlesen')
        self.parent.Bind(wx.EVT_MENU, self.OnReadDir, m_readDir)
        m_setTDir = menu.Append(-1, 'setze Zielverz.')
        self.parent.Bind(wx.EVT_MENU, self.OnSetTDir, m_setTDir)
        return menu

    def OnSetTDir(self, _event):
        """Merke Dir als aktuelles Ziel"""
        config.mainframe.SetStatusText('Ziel: ' + self.dropped_dir)
        config.targetdir_path = self.dropped_dir

    def OnReadDir(self, _ev):
        pass
        # database.video_del_path(self.dropped_dir)
        # DiskImport.scan_dir(self.dropped_dir)
