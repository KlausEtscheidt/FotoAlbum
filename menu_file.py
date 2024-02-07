'''
menu_file
----------------

Definiert Untermenues des File-Menu
'''

import wx

from config import conf
import import_export as impex


def init(parent, parent_menu):
    '''Menu-Items zum Menu erzeugen und Handler registrieren'''

    # The "\t..." syntax defines an accelerator key that also triggers the same event
    men_items = (
        (OnStart, "Start", "Starte Bearbeitung aller Bilder."),
        (OnSettings, "Einstellungen", "Einstellungen ändern."),
        (OnSaveSettings, "Einstellungen speichern", "Einstellungen speichern."),
        (OnSaveHistory, "Verlauf speichern", "Bisher definierte Fotos in Toml speichern."),
        (OnSaveAll, "Alle Fotos exportieren", "Alle Fotos als JPF und TIFf speichern."),
        (OnExit, "Ende", "Programm beenden")
    )
    for m_item in men_items:
        m = parent_menu.Append(-1, m_item[1], m_item[2])
        parent.Bind(wx.EVT_MENU, m_item[0], m)

# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name

def OnStart(_event):
    conf.thisapp.seiten_laden()

def OnSettings(_event):
    conf.settings()

def OnSaveSettings(_event):
    conf.config2toml()

def OnSaveHistory(_event):
    impex.ausgeben(conf.thisapp.mainframe.seiten, conf.pic_path)

def OnSaveAll(_event):
    conf.thisapp.seiten.alle_speichern()

# #Öffne mit Rawtherapee
# def OnEdit(_event):
#     subprocess.Popen(config.editor)


## File-Menu Programm Ende
def OnExit(_event):
    # Close the frame, terminating the application.
    conf.mainframe.Close(True)
