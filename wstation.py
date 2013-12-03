#!/usr/bin/env python3


import os, sys
from gi.repository import Gtk, GObject, Gdk
#~ import notify2
from pywws import DataStore
from datetime import datetime,timedelta

ui_file='wstation.ui'

var=['a_temp_out','a_hum_out','a_rel_pressure','a_wind_gust','a_wind_dir','a_rain','a_temp_in','a_hum_in']
fmt={'temp':'{:.1f} ᴼC','hum':'{:2d} %','rel_pressure':'{:.1f} mb','wind_gust':'{:.1f} km/h','wind_dir':'{0}','rain':'{:.1f} mm'}

def get_tipo_var(var):
    for k in fmt.keys():
        if k in var:
            t,v=var.split('_',1)
            return t,v,fmt[k]
def get_pywws():
    fecha=datetime.utcnow()
    #Valores actuales
    datos=DataStore.calib_store(dir_data)
    a=datos[datos.nearest(fecha)]
    return {'a':a}

def update_var(win):
        pd=get_pywws()
        for v in var:
            t,pv,f=get_tipo_var(v)
            lbl=win.builder.get_object(v)
            lbl.set_label(f.format(pd[t][pv]))

class MainWindow(object):
    """Clase manejadora de la ventana principal.

    """
    def __init__(self):

        self.builder=Gtk.Builder()
        self.builder.add_from_file(ui_file)
        self.builder.connect_signals(self)

        self.win=self.builder.get_object('window1')
        #~ self.win.set_decorated(False)           #Don't show title bar and borders
        #~ self.win.set_keep_above(True)           #Always on top
        #~ self.win.set_skip_taskbar_hint(True)    #Don't show in taskbar

        self.update_ui()
        GObject.timeout_add_seconds(60,self.update_ui)

        self.win.show_all()

    def update_ui(self):
        update_var(self)
        return

    def on_window_destroy(self,win):
        Gtk.main_quit()

    def run(self):
        Gtk.main()

#set working directory
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
#.ini
params=DataStore.ParamStore('.','wstation.ini')
dir_data=params.get('paths','dir_data')
if dir_data==None:
    dir_data=filedialog.askdirectory(title='Seleccione directorio con datos de pywws')
    params.set('paths','dir_data',dir_data)
    params.flush()

MainWindow().run()
