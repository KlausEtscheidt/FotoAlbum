"""
alb_logging.py
----------------
Logging in ein wx.Panel
"""

import logging
import logging.handlers

from config import conf

#Get the root logger (muss in jedes Modul)
logger = logging.getLogger('album')

class KE_Handler(logging.Handler):
    def __init__(self):
        super(KE_Handler, self).__init__()

    def emit(self, record):
        msg = self.format(record)
        # conf.mainframe.logpanel.Output(msg)

def init():
    #set level
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)

    #Bildschirm-Handler
    #screen_hdlr = logging.StreamHandler(sys.stdout)
    screen_hdlr = KE_Handler()

    # Formatter zum Handler
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

    #Alles auf Schirm
    screen_hdlr.setFormatter(formatter)
    logger.addHandler(screen_hdlr)
