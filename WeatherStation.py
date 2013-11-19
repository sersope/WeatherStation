#!/usr/bin/env python3


import os, sys
from gi.repository import Gtk, GObject, Gdk
import notify2
from get_pywws import Weather

ui_file='wstation.ui'

class MainWindow(object):
    """Clase manejadora de la ventana principal.

    """
    def __init__(self):
        
        builder=Gtk.Builder()
        builder.add_from_file(ui_file)
        builder.connect_signals(self)
        
        self.status_icon=builder.get_object('statusicon1')
        self.win=builder.get_object('window1')
        self.win.set_decorated(False)           #Don't show title bar and borders
        self.win.set_keep_above(True)           #Always on top
        self.win.set_skip_taskbar_hint(True)    #Don't show in taskbar
        self.lbl_temp_out=builder.get_object('lbl_temp_out')
        self.lbl_temp_in=builder.get_object('lbl_temp_in')
        self.lbl_hum_out=builder.get_object('lbl_hum_out')
        self.lbl_hum_in=builder.get_object('lbl_hum_in')
        self.lbl_rain=builder.get_object('lbl_rain')
        self.lbl_status=builder.get_object('lbl_status')

        notify2.init ("Weather Station")
        
        self.cont=0
        self.update_ui()
        GObject.timeout_add_seconds(60,self.update_ui)
        
        self.win.show_all()
        
    def update_ui(self):
        dic=Weather.now()
        self.lbl_temp_out.set_label('{:0.1f}'.format(dic['temp_out']))
        self.status_icon.set_tooltip_text('Weather Station\nT: {:0.1f}  H: {:d}'.format(dic['temp_out'],dic['hum_out']))
        self.lbl_hum_out.set_label('{:d}'.format(dic['hum_out']))
        self.lbl_rain.set_label('{:0.1f}'.format(dic['rain_interval']))
        self.lbl_temp_in.set_label('{:0.1f}'.format(dic['temp_in']))
        self.lbl_hum_in.set_label('{:d}'.format(dic['hum_in']))
        self.lbl_status.set_label('{} {:d}'.format(dic['idx'],self.cont))
        if dic['rain_interval'] > 0.0:
            self.notify_rain(dic['rain_interval'],dic['delay'])
        self.cont+=1
        w=self.win.get_size()[0]
        W=Gdk.Screen.get_default().get_width()
        self.win.move(W-w,0)
        return dic['delay']
    
    def notify_rain(self,rain,delay):
        body="It's raining. {:0.1f} in last {:d} minutes.".format(rain,delay)
        msg=notify2.Notification("Weather Station",body,"weather-showers")
        msg.show ()
        
    def on_statusicon1_button_press_event(self,win,arg):
        self.win.set_decorated(True)
        


    def on_window_destroy(self,win):
        Gtk.main_quit()

    def run(self):
        Gtk.main()

#set working directory
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

MainWindow().run()
