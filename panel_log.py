import wx


class LogPanel(wx.Panel):
    def __init__(self, parent, page_id):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.id = page_id #id merken zum Umschalten per SetSelection

        self.txtctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)


        #font setzen fuer formatierte ausgabe
        myfont = wx.Font()
        myfont.SetFamily(wx.FONTFAMILY_MODERN)#fixed pitch
        self.txtctrl.SetFont(myfont)
        self.txtctrl.SetEditable(False)

        # Use some sizers to see layout options
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txtctrl, 1, wx.EXPAND)

        #Layout sizers
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)

    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------
    # ------------------------------------------------------
    # High-level funktionen
    # ------------------------------------------------------
    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------

    def Output(self, txt):
        self.txtctrl.SetValue(self.txtctrl.GetValue() + txt + '\n')

    def Clear(self):
        self.txtctrl.SetValue("")

    #Seite anzeigen
    def Activate(self):
        self.txtctrl.SetEditable(False)
        self.parent.SetSelection(self.id)

if __name__ == '__main__':
    pass
