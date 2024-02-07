"""
alb_logging.py
----------------
Logging in ein wx.Panel
"""

import sys
import logging
import logging.handlers

# Get the root logger (muss in jedes Modul)
logger = logging.getLogger('album')

# class ke_handler(logging.Handler):
#     def __init__(self):
#         super(ke_handler, self).__init__()

#     def emit(self, record):
#         msg = self.format(record)
#         # conf.mainframe.logpanel.Output(msg)

def init():
    '''Setzt logging-level und Ausgabe ins Terminal'''
    #set level
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)

    #Bildschirm-Handler
    screen_hdlr = logging.StreamHandler(sys.stdout)
    # screen_hdlr = ke_handler()

    # Formatter zum Handler
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

    #Alles auf Schirm
    screen_hdlr.setFormatter(formatter)
    logger.addHandler(screen_hdlr)
