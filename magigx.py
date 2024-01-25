from wxPython import wx
import PythonMagick

ID_FILE_OPEN = wx.wxNewId()
ID_FILE_EXIT  = wx.wxNewId()
ID_THRESHOLD = wx.wxNewId()

class ImagePanel(wx.wxPanel):
    def __init__(self, parent, id):
        wx.wxPanel.__init__(self, parent, id)
        self.image = None  # wxPython image
        wx.EVT_PAINT(self, self.OnPaint)

    def display(self, magickimage):
        self.image = self.convertMGtoWX(magickimage)
        self.Refresh(True)

    def OnPaint(self, evt):
        dc = wx.wxPaintDC(self)
        if self.image:
            dc.DrawBitmap(self.image.ConvertToBitmap(), 0,0)

    def convertMGtoWX(self, magickimage):
        img = PythonMagick.Image(magickimage)  # make copy
        img.depth = 8        #  change depth only for display
        img.magick = "RGB"
        data = img.data
        wximg = wx.wxEmptyImage(img.columns(), img.rows())
        wximg.SetData(data)
        return wximg


class mtFrame(wx.wxFrame):
    def __init__(self, parent, ID, title):
        wx.wxFrame.__init__(self, parent, ID, title, wx.wxDefaultPosition, wx.wxSize(500, 400))

        self.iPanel = ImagePanel(self, -1)
        self.im = None  # Magick image

        ## Construct "File" menu
        self.menuBar = wx.wxMenuBar()
        self.menuFile = wx.wxMenu()
        self.menuFile.Append(ID_FILE_OPEN, "&Open image","")
        wx.EVT_MENU(self, ID_FILE_OPEN, self.OnOpen)
        self.menuFile.AppendSeparator()
        self.menuFile.Append(ID_FILE_EXIT, "E&xit", "")
        wx.EVT_MENU(self, ID_FILE_EXIT,  self.OnExit)
        self.menuBar.Append(self.menuFile, "&File");

        ## Construct "Process" menu
        self.menuProcess = wx.wxMenu()
        self.menuProcess.Append(ID_THRESHOLD, "Threshold", "")
        wx.EVT_MENU(self, ID_THRESHOLD,  self.OnThreshold)

        self.menuBar.Append(self.menuProcess, "&Process")
        self.SetMenuBar(self.menuBar)

    def OnOpen(self, event):
        fd = wx.wxFileDialog(self, "Open Image", "", "", "*.*", wx.wxOPEN)

        if fd.ShowModal() == wx.wxID_OK:
            self.loadImage(fd.GetPath())
        fd.Destroy()

    def loadImage(self, path):
        try:
            self.im = PythonMagick.Image(path)
            self.iPanel.display(self.im)
        except IOError:
            print "can't open the file"

    ##-------------- Process ------------------------

    def OnThreshold(self, event):
        self.im = self.Threshold(self.im, 0.5)
        self.iPanel.display(self.im)
        #self.im.write('d:/threshold.tif')

    def Threshold(self, image, threshold):
        """
        Threshold image. Input threshold is normalized (0-1.0)
        """
        img = PythonMagick.Image(image) # copy
        img.threshold(threshold *65535.0)
        return img

    ##-----------------------------------------------

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnExit(self, event):
        self.Close(True)

#---------------------------------------------------------------------------

class mtApp(wx.wxApp):
    def OnInit(self):
        frame = mtFrame(wx.NULL, -1, "MagickSimple1")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = mtApp(0)
app.MainLoop()