import wx
import wx.html
from config import conf

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

    helpctlr = wx.html.HtmlHelpController()
    # fname = r"C:\Users\Klaus\Documents\_m\FotoAlbum\doktest\testing.hhp"
    # erg = helpctlr.AddBook(fname)
    # fname = r"C:\Users\Klaus\Documents\_m\FotoAlbum\doktest\another.hhp"
    # erg = helpctlr.AddBook(fname)
    fname = r"C:\Users\Klaus\Documents\_m\FotoAlbum\doku_help\build\htmlhelp\fotoalbumhilfedoc.hhp"
    erg = helpctlr.AddBook(fname)
    # print(erg)
    helpctlr.DisplayContents()

    conf.help = helpctlr
