import wx
# import subprocess

from config import conf
import import_export as impex


# Menu-Items zum Menu erzeugen und Handler registrieren
def init(parent, pMenu):
    # The "\t..." syntax defines an accelerator key that also triggers the same event
    men_items = (
        # (OnRefillTree, "Baum erneuern", "Baum neu lesen"),
        (OnStart, "Start", "Starte Bearbeitung aller Bilder."),
        (OnSettings, "Einstellungen", "Einstellungen ändern."),
        (OnSaveSettings, "Einstellungen speichern", "Einstellungen speichern."),
        (OnSaveHistory, "Verlauf speichern", "Bisher definierte Fotos in Toml speichern."),
        (OnSaveAll, "Alle Fotos exportieren", "Alle Fotos als JPF und TIFf speichern."),
        (OnResetLog, "Lösche Logpanel", "Logpanel leeren"),
        # (OnEdit, "Öffne RawTherapee", "Öffne RawTherapee"),
        (OnExit, "Ende", "Programm beenden"),
    )
    for mItem in men_items:
        m = pMenu.Append(-1, mItem[1], mItem[2])
        parent.Bind(wx.EVT_MENU, mItem[0], m)

def OnStart(_event):
    conf.thisapp.seiten_laden()

def OnSettings(_event):
    conf.settings()

def OnSaveSettings(_event):
    conf.savesettings()

def OnSaveHistory(_event):
    impex.ausgeben(conf.thisapp.seiten, conf.pic_path)

def OnSaveAll(_event):
    conf.thisapp.seiten.alle_speichern()

def OnResetLog(_event):
    conf.mainframe.logpanel.Clear()

# #Öffne mit Rawtherapee
# def OnEdit(_event):
#     subprocess.Popen(config.editor)


## File-Menu Programm Ende
def OnExit(_event):
    """Close the frame, terminating the application."""
    conf.mainframe.Close(True)
