import wx

# Menu-Items zum Menu erzeugen und Handler registrieren
def init(parent, pMenu):
    men_items = (
        (OnAbout, "Über", "Bla Bla Dummy"),
    )
    for mItem in men_items:
        m = pMenu.Append(-1, mItem[1], mItem[2])
        parent.Bind(wx.EVT_MENU, mItem[0], m)

## Help-Menu
def OnAbout(_event):
    """Display an About Dialog"""
    wx.MessageBox("Bedienung des Garten-Programmsystems",
                  "Über Garten-Gui",
                  wx.OK|wx.ICON_INFORMATION)
