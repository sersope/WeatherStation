#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, sys
from gi.repository import Gtk, GObject
from pywws import DataStore,TimeZone
from datetime import datetime,timedelta
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

ui_file='wstation.ui'

labels=['a_temp_out','a_hum_out','a_rel_pressure','a_wind_gust','a_wind_dir','a_temp_in','a_hum_in',
    'd_temp_out_max','d_temp_out_min','d_hum_out_max','d_hum_out_min','d_rel_pressure_max',
    'd_rel_pressure_min','d_wind_gust','d_rain','d_temp_in_max','d_temp_in_min','d_hum_in_max',
    'd_hum_in_min','m_temp_out_max_hi','m_temp_out_min_lo','m_hum_out_max','m_hum_out_min',
    'm_rel_pressure_max','m_rel_pressure_min','m_wind_gust','m_rain','m_temp_in_max_hi',
    'm_temp_in_min_lo','m_hum_in_max','m_hum_in_min','y_temp_out_max_hi','y_temp_out_min_lo',
    'y_hum_out_max','y_hum_out_min','y_rel_pressure_max','y_rel_pressure_min','y_wind_gust',
    'y_rain','y_temp_in_max_hi','y_temp_in_min_lo','y_hum_in_max','y_hum_in_min']

formatos={'temp':'{:.1f}ᴼC','hum':'{:2d}%','rel_pressure':'{:.1f}mb','wind_gust':'{:.1f}km/h',
    'wind_dir':'{0}','rain':'{:.1f}mm'}

def _parse_label(label):
    for k in formatos.keys():
        if k in label:
            tk,pk=label.split('_',1)
            return tk,pk,formatos[k]

def get_pywws_data():
    ydat={'temp_out_max_hi':float('-inf'),'temp_out_min_lo':float('inf'),
    'hum_out_max':float('-inf'),'hum_out_min':float('inf'),'rel_pressure_max':float('-inf'),
    'rel_pressure_min':float('inf'),'wind_gust':float('-inf'),'rain':0.0,
    'temp_in_max_hi':float('-inf'),'temp_in_min_lo':float('inf'),'hum_in_max':float('-inf'),
    'hum_in_min':float('inf')}

    fec=datetime.utcnow()
    #Valores actuales
    dat=DataStore.calib_store(dir_data)
    adat=dat[dat.nearest(fec)]
    gdat=dat[dat.nearest(fec)-timedelta(hours=24):]

    #Valores diario
    dat=DataStore.daily_store(dir_data)
    ddat=dat[dat.nearest(fec)]
    #Valores diario
    dat=DataStore.monthly_store(dir_data)
    mdat=dat[dat.nearest(fec)]
    #Valores anuales
    for d in dat[:]:
        for k in ydat.keys():
            if 'min' in k:
                ydat[k]=min(ydat[k],d[k])
            elif 'rain' in k:
                ydat[k]=ydat[k]+d[k]
            else:
                ydat[k]=max(ydat[k],d[k])
    #Graficos

    return {'a':adat,'d':ddat,'m':mdat,'y':ydat,'g':gdat}


class MainWindow(object):
    """Clase manejadora de la ventana principal.

    """
    def __init__(self):

        self.builder=Gtk.Builder()
        self.builder.add_from_file(ui_file)
        self.builder.connect_signals(self)
        self.win=self.builder.get_object('window1')
        self.last_act=self.builder.get_object('last_act')

        self.graf_box=self.builder.get_object('graf_box')
        fig = Figure(figsize=(12,4))    #,dpi=72
        self.plot1 = fig.add_subplot(111)
        #~ self.plot2 = fig.add_subplot(212)
        #~ self.plot2.set_position([0.05,0.08,0.90,0.38])
        self.plot1.set_position([0.05,0.54,0.90,0.38])
        self.canvas = FigureCanvas(fig)
        self.graf_box.pack_start(self.canvas,True,True,0)

        self.win.show_all()
        #~ self.i=0 #TEST
        self.update_ui()
        GObject.timeout_add_seconds(60,self.update_ui)

    def update_ui(self):
        self.update_labels()
        #~ self.last_act.set_label(str(self.i)) #TEST
        #~ self.i+=1 #TEST
        return True

    def update_labels(self):
        pywws_data=get_pywws_data()
        idx=pywws_data['a']['idx'].replace(tzinfo=TimeZone.utc).astimezone(TimeZone.Local)
        self.last_act.set_label(idx.strftime('%c'))
        for label in labels:
            tipo_k,pywws_k,formato=_parse_label(label)
            ui_lbl=self.builder.get_object(label)
            ui_lbl.set_label(formato.format(pywws_data[tipo_k][pywws_k]))
        #plotting
        val=[],[],[]
        for d in pywws_data['g']:
            val[0].append(d['idx'].replace(tzinfo=TimeZone.utc).astimezone(TimeZone.Local))
            val[1].append(d['temp_out'])
            val[2].append(d['temp_in'])
        self.plot1.clear()
        self.plot1.set_title(u'Últimas 24 horas.')
        self.plot1.set_xlabel('Hora')
        self.plot1.set_ylabel(u'Temperatura (ᴼC)')
        self.plot1.plot(val[0],val[1],label='T. exterior')
        self.plot1.plot(val[0],val[2],label='T. interior')
        self.plot1.grid(True)
        self.plot1.minorticks_on()
        self.plot1.legend(loc=0)
        self.canvas.draw()

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
    dialog = Gtk.FileChooserDialog("Seleccione carpeta de datos pywws:", None,Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OK, Gtk.ResponseType.OK))
    dialog.set_default_size(800,800)
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        dir_data=dialog.get_filename()
        params.set('paths','dir_data',dir_data)
        params.flush()
    else:
        exit(0)
    dialog.destroy()

MainWindow().run()
