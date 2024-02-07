"""
zeichenfabrik.py
====================================
Funktionen zum Zeichnen in Bitmaps.

Die Funktionen liefern meist eine eigene Bitmap (zbmp) zurück,
die als Overlay über die angezeigten Bitmaps gelegt wird.
"""


import logging

import wx

logger = logging.getLogger('album')

def zeichne_rahmen(image_bmp, akt_seite):
    '''Zeichnet Rahmen für alle definierten Fotos einer Seite.

    Der Rahmen wird aus den gewählten Ecken der Fotos erzeugt und mit Diagonalen gezeichnet.
    Die Rahmen dienen zur Kennzeichnung bereits definierter Fotos.

    Args:
        image_bmp (wx.Bitmap): Bitmap über die gezeichnet wird (nur zur Größenbestimmung).
        akt_seite (seite): seite deren Fotos markiert werden sollen.

    Returns:
        wx.Bitmap: Bitmap mit Rahmen.
    '''
    dc, zbmp = __prepare_dc(image_bmp)
    for foto in akt_seite.fotos:
        p4 = wx.Point(foto.ecke1.x, foto.ecke3.y)
        punkte = [foto.ecke1, foto.ecke2, foto.ecke3, foto.ecke1, p4, foto.ecke3]
        dc.DrawPolygon(punkte)
        dc.DrawLine(p4, foto.ecke2)
    __release_dc(dc, zbmp)
    return zbmp

def zeichne_ecke(image_bmp, x1, y1, x2, y2):
    '''Linie von der Vorgänger-Ecke zu Ecke2 bzw Ecke3

    Args:
        image_bmp (wx.Bitmap): Bitmap über die gezeichnet wird (nur zur Größenbestimmung)
        linie_hor (Bool, optional): _description_. Defaults to None.
        linie_vert (Bool, optional): _description_. Defaults to None.

    Returns:
        wx.Bitmap: Bitmap mit Linien
    '''

    dc, zbmp = __prepare_dc(image_bmp)
    dc.SetPen(wx.Pen(wx.RED, 3))
    dc.DrawLine(x1, y1, x2, y2)
    __release_dc(dc, zbmp)
    return zbmp

def zeichne_clip_rahmen(image_bmp, foto, rand, rahmen_plus):
    '''Rahmen ins gedrehte Bild einzeichnen.

    Dient zur Korrektur des Beschnitts.
    Definition entsprechend Ecke1, Breite und Höhe des Fotos.
    image_bmp wurde um *rand* größer erzeugt, als es die Ecken des Fotos vorgeben würden.
    Der Beschnittrahmen der gezeichnet werden soll,
    ist um rahmen_plus grösser als die Ecken des Fotos.

    Args:
        image_bmp (wx.Bitmap): Bitmap eines Fotos
        foto (Foto): Fotodaten bstimmen den Rahmen
        rand (int): Die Bitmap ist um rand grösser als die Ecken des Fotos
        rahmen_plus (int): Der Beschnitt ist um rahmen_plus grösser als die Ecken des Fotos

    Returns:
        wx.Bitmap: zbmp mit eingezeichnetem Beschnitt-Rahmen
    '''
    p1 = wx.Point(rand - rahmen_plus, rand - rahmen_plus)
    p2 = wx.Point(p1.x + foto.breite + 2*rahmen_plus, p1.y)
    p3 = wx.Point(p2.x, p1.y + foto.hoehe + 2*rahmen_plus)
    p4 = wx.Point(p1.x, p3.y)
    dc, zbmp = __prepare_dc(image_bmp)
    dc.SetPen(wx.Pen(wx.RED, 5))
    punkte = [p1, p2, p3, p4]
    dc.DrawPolygon(punkte)
    __release_dc(dc, zbmp)
    return zbmp

def zeichne_clip_rahmen_ins_bild(image_bmp, foto, rand, rahmen_plus):
    '''Zeichnet Beschnittrahmen direkt in image_bmp.

    Wird beim Speichern des Kontrollbilds verwendet um den Beschnitt anzuzeigen.
    Es wird direkt ins Bild gezeichnet und nicht in eine Overlay-Bitmap (z.B zbmp).
    image_bmp wurde um *rand* größer erzeugt, als es die Ecken des Fotos vorgeben würden.
    Der Beschnittrahmen der gezeichnet werden soll,
    ist um rahmen_plus grösser als die Ecken des Fotos.

    Args:
        image_bmp (wx.Bitmap): Bitmap eines Fotos
        foto (Foto): Fotodaten bstimmen den Rahmen
        rand (int): Die Bitmap ist um rand grösser als die Ecken des Fotos
        rahmen_plus (int): Der Beschnitt ist um rahmen_plus grösser als die Ecken des Fotos

    Returns:
        wx.Bitmap: image_bmp mit eingezeichnetem Beschnitt-Rahmen
    '''

    p1 = wx.Point(rand - rahmen_plus, rand - rahmen_plus)
    p2 = wx.Point(p1.x + foto.breite + 2*rahmen_plus, p1.y)
    p3 = wx.Point(p2.x, p1.y + foto.hoehe + 2*rahmen_plus)
    p4 = wx.Point(p1.x, p3.y)

    dc = wx.MemoryDC()
    dc.SelectObject(image_bmp)
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetPen(wx.Pen(wx.RED, 5))
    punkte = [p1, p2, p3, p4]
    dc.DrawPolygon(punkte)
    # dc freigeben
    dc.SelectObject(wx.NullBitmap)
    dc = None
    return image_bmp


####################################################################################
# Helper

def __prepare_dc(image_bmp):
    '''Bereitet das Zeichnen vor.

    Erzeugt einen Memory-Device-Context und eine Bitmap der Größe von image_bmp.
    Setzt Background, Brush und Pen und löscht dann den DC

    Args:
        image_bmp (wx.Bitmap): Bitmap zur Größenbestimmung der Zeichen-Bitmap

    Returns:
        wx.MemoryDC: Device Context zum Zeichnen
        wx.Bitmap: Bitmap in die gezeichnet wird
    '''
    dc = wx.MemoryDC()
    h = image_bmp.Height
    w = image_bmp.Width
    zbmp = wx.Bitmap(w, h)

    dc.SelectObject(zbmp)
    dc.SetBackground(wx.Brush('black'))
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetPen(wx.Pen(wx.RED, 15))
    dc.Clear()
    return dc, zbmp

def __release_dc(dc, zbmp):
    '''Bendet das Zeichnen

    Setzt die Transparenzfabe der Bitmap auf black.
    Gibt den DC frei.

    Args:
        dc (wx.MemoryDC): Device Context zum Zeichnen
        zbmp (wx.Bitmap): Bitmap in die gezeichnet wurde
    '''
    # dc freigeben
    dc.SelectObject(wx.NullBitmap)
    # Transparenz setzen: Schwarz wird transparent
    zbmp.SetMaskColour('black')
    dc = None
