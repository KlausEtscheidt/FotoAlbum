import pathlib
import subprocess
import wx

import config as conf
import filedrop
# import FileClass
# import DiskImport
# import DiskTools

#from PopUpMenu_Files import FilePopupMenu

class ImagePanel(wx.Panel):
    def __init__(self, parent, page_id):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.id = page_id #id merken zum Umschalten per SetSelection

        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)

        #-----------------------
        # tif !!!
        # wxImage::AddHandler(new wxPNGHandler);

        # leere bitmap
        mybitmap = wx.Bitmap()
        # Haupt-Image-control
        self.imagectrl = wx.StaticBitmap(self, -1, mybitmap, (0,0), (10,10))
        self.imagectrl.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        
        #-------------------------------------------------------

        # Gesamt-Layout (Textctrl und searchbox)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.imagectrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        # ohne EXPAND für seacrh_sizer expandiert das SQL-Eingabefeld nicht
        #main_sizer.Add(search_sizer, flag=wx.ALIGN_CENTER|wx.BOTTOM|wx.EXPAND, border=5)
        #main_sizer.Add(filter_sizer, flag=wx.ALIGN_CENTER|wx.BOTTOM|wx.EXPAND, border=5)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(main_sizer)
        self.SetAutoLayout(1)
        main_sizer.Fit(self)

        #Handler binden
        #R-Maus in Anzeige für Popup Menu
        # self.txtctrl.Bind(wx.EVT_RIGHT_DOWN, self.OnRMouseClick)

    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------

    # def OnRMouseClick(self, event):
    #     m_pos = event.GetPosition()  # Pixel-Koordinaten
    #     _p, _x, y = self.txtctrl.HitTest(m_pos) #Text-Koord
    #     myfilepath = self.txtctrl.GetLineText(y)
    #     self.selected_file = myfilepath

    #     menu = self.MakePopUpMenu()
    #     self.PopupMenu(menu, m_pos)



        
    # ------------------------------------------------------
    # High-Level Funktionen
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------

    #Seite anzeigen
    def Activate(self):
        self.parent.SetSelection(self.id)
