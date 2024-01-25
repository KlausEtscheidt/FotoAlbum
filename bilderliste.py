import glob 
import os
import logging

import wx

import config as conf

logger = logging.getLogger('album')

#######################################################################################
#
class Bild():
    def __init__(self, fullpath2pic):
        self.fullpath2pic = fullpath2pic
        self.path, self.picname = os.path.split(self.fullpath2pic)
        self.basename, self.typ = os.path.splitext(self.picname)
        self.__image = None

    def show(self):
        myimage = self.image#.Scale(500, 500)
        mybitmap = myimage.ConvertToBitmap()
        # imagectrl.SetBitmap(mybitmap)
        # conf.mainframe.imagepanel.center_bitmap()
        conf.mainframe.imagepanel.bitmap=mybitmap
    
    def scale_percent(self, faktor):
        myimage = self.image
        new_w = int(myimage.Width * faktor)
        new_h = int(myimage.Height * faktor)
        self.image = myimage.Scale(new_w, new_h)
        logger.debug(f'\nnew size: br {new_w} h: {new_h}\n')


    @property
    def image(self):
        if not self.__image: 
            self.__image = wx.Image(self.fullpath2pic, wx.BITMAP_TYPE_ANY)
        return self.__image
        
    @image.setter
    def image(self, x):
        self.__image = x

#######################################################################################
#
class BilderListe(list):
    def __init__(self, srcPath, src_type):
        super().__init__()
        myFileList=[]
        # self.Liste=[]

        # Suche Bilder    
        myFileList = glob.glob(srcPath + "\*" + src_type)
        
        #Fuer jeden gefundenen Pfad, Bildobjekt erzeugen und merken
        for fullpath in myFileList:
            mBild = Bild(fullpath)
            self.append (mBild)
