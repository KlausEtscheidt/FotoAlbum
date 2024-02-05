import wx
import wx.html
import config as conf

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

    # https://github.com/wxWidgets/wxWidgets/tree/master/samples/html/helpview
    
    #Display an About Dialog
    helpctlr = wx.html.HtmlHelpController()
    conf.help = helpctlr
    # pfad = r"C:\Users\Klaus\Documents\_m\FotoAlbum\doku\build\htmlhelp"
            
    url = r"file:///C:\Users\Klaus\Documents\_m\FotoAlbum\doku\build\htmlhelp\fotoalbumdoc.hhp"
    # # url = ''
    # data = wx.html.HtmlHelpData()
    # url = data.GetContentsArray()
    # erg = data.AddBook(url)
    #helpctlr.AddBook("help.zip")
    fname = r"C:\Users\Klaus\Documents\_m\FotoAlbum\test.zip"
    # erg = helpctlr.AddBook(fname)
    erg = helpctlr.AddBook(url)
    # helpctlr.CreateHelpDialog(data)
    helpctlr.DisplayContents()
    # helpctlr.Display('modules')
    # wx.MessageBox("Bedienung des Garten-Programmsystems",
    #               "Über Garten-Gui",
    #               wx.OK|wx.ICON_INFORMATION)
