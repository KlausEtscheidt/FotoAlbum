"""
menu_div.py
------------
Erzeugt Menus u.a. zum Anzeigen der Hilfe
"""

import wx
import wx.html
from config import conf


def init(parent, parent_menu):
    '''Menu-Items zum Menu erzeugen und Handler registrieren'''
    men_items = (
        (on_show_help, "Hilfe", "Hilfe anzeigen"),
    )
    for myitem in men_items:
        m = parent_menu.Append(-1, myitem[1], myitem[2])
        parent.Bind(wx.EVT_MENU, myitem[0], m)

## Help-Menu
def on_show_help(_event):
    '''Zeigt Html-Hilfe an'''

    helpctlr = wx.html.HtmlHelpController()
    fname = r"C:\Users\Klaus\Documents\_m\FotoAlbum\doku_help\build\htmlhelp\fotoalbumhilfedoc.hhp"
    if not helpctlr.AddBook(fname):
        wx.MessageBox('Konnte Hilfedatei nicht einlesen', 'Fehler')
    helpctlr.DisplayContents()

    conf.help = helpctlr
