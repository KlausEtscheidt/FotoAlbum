import wx

filenames = [r"C:\Users\Klaus\Pictures\xalb4\teil1\Bild001.jpg" ]
             
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Loading Images")
        p = wx.Panel(self)

        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        for name in filenames:
            img1 = wx.Image(name, wx.BITMAP_TYPE_ANY)

            w = int(img1.GetWidth()/4)
            h = int(img1.GetHeight()/4)
            img2 = img1.Scale(w, h)

            sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1))
            sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img2))

            #fgs.Add(sb1)
            fgs.Add(sb2)

        p.SetSizerAndFit(fgs)
        self.Fit()

app = wx.PySimpleApp()
frm = TestFrame()
frm.Show()
app.MainLoop()