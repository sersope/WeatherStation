#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division,absolute_import,print_function,unicode_literals

import os, gettext
from gi.repository import Gtk, GObject
from pywws import DataStore,TimeZone
from datetime import datetime,timedelta
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import dates
from matplotlib.ticker import MultipleLocator

gettext.install('wstation','locale',unicode=True)

ui_file = 'wstation.ui'
param_file='wstation.ini'

labels = ['a_temp_out','a_hum_out','a_rel_pressure','a_wind_gust','a_wind_dir','a_temp_in',
    'a_hum_in','d_temp_out_max','d_temp_out_min','d_hum_out_max','d_hum_out_min','d_rel_pressure_max',
    'd_rel_pressure_min','d_wind_gust','d_rain','d_temp_in_max','d_temp_in_min','d_hum_in_max',
    'd_hum_in_min','m_temp_out_max_hi','m_temp_out_min_lo','m_hum_out_max','m_hum_out_min',
    'm_rel_pressure_max','m_rel_pressure_min','m_wind_gust','m_rain','m_temp_in_max_hi',
    'm_temp_in_min_lo','m_hum_in_max','m_hum_in_min','y_temp_out_max_hi','y_temp_out_min_lo',
    'y_hum_out_max','y_hum_out_min','y_rel_pressure_max','y_rel_pressure_min','y_wind_gust',
    'y_rain','y_temp_in_max_hi','y_temp_in_min_lo','y_hum_in_max','y_hum_in_min']

formatos = {'temp':'{:.1f}ᴼC','hum':'{:2d}%','rel_pressure':'{:.1f}mb','wind_gust':'{:.1f}km/h',
    'wind_dir':'{0}','rain':'{:.1f}mm'}

def _parse_label(label):
    for k in formatos.keys():
        if k in label:
            tk,pk = label.split('_',1)
            return tk,pk,formatos[k]

def get_pywws_data(dir_data):
    ydat = {'temp_out_max_hi':float('-inf'),'temp_out_min_lo':float('inf'),
        'hum_out_max':float('-inf'),'hum_out_min':float('inf'),'rel_pressure_max':float('-inf'),
        'rel_pressure_min':float('inf'),'wind_gust':float('-inf'),'rain':0.0,
        'temp_in_max_hi':float('-inf'),'temp_in_min_lo':float('inf'),'hum_in_max':float('-inf'),
        'hum_in_min':float('inf')}

    ahora = datetime.utcnow()
    try:
        dat = DataStore.calib_store(dir_data)
        adat = dat[dat.nearest(ahora)]
        dat = DataStore.hourly_store(dir_data)
        hdat = dat[dat.nearest(ahora)-timedelta(hours=24):]
        dat = DataStore.daily_store(dir_data)
        ddat = dat[dat.nearest(ahora)]
        dat = DataStore.monthly_store(dir_data)
        mdat = dat[dat.nearest(ahora)]
        f1=datetime(ahora.year,1,1,0,0,0)#primer momento del año
        for d in dat[dat.after(f1):]:
            for k in ydat.keys():
                if 'min' in k:
                    ydat[k] = min(ydat[k],d[k])
                elif 'rain' in k:
                    ydat[k] = ydat[k]+d[k]
                else:
                    ydat[k] = max(ydat[k],d[k])
    except:
        return None
    return {'a':adat,'h':hdat,'d':ddat,'m':mdat,'y':ydat}


class MainWindow(object):
    """Clase manejadora de la ventana principal.

    """
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(app_dir,ui_file))
        self.builder.connect_signals(self)
        self.win=self.builder.get_object('window1')
        self.graf_box=self.builder.get_object('graf_box')
        self.statusbar = self.builder.get_object('statusbar')
        self.statusbar.push(1,_('Último acceso:'))
        self.ui_label={}
        for label in labels:
            self.ui_label[label]=self.builder.get_object(label)

        fig = Figure()
        self.plot1 = fig.add_subplot(111)
        self.plot2 = fig.add_subplot(212)
        self.plot3 = fig.add_subplot(313)
        self.plot3.set_position([0.055,0.06,0.93,0.24])
        self.plot2.set_position([0.055,0.38,0.93,0.24])
        self.plot1.set_position([0.055,0.69,0.93,0.24])
        self.canvas = FigureCanvas(fig)
        self.graf_box.pack_start(self.canvas,True,True,0)

        self.win.show_all()
        if self.get_params():
            self.update_ui()
            GObject.timeout_add_seconds(10,self.update_ui)

    def get_params(self):
        #Obtener parametros de programa
        params=DataStore.ParamStore(app_dir,param_file)
        self.dir_data=params.get('paths','dir_data')
        if self.dir_data==None:
            dialog = Gtk.FileChooserDialog(_("Seleccione carpeta de datos pywws:"), self.win,
                     Gtk.FileChooserAction.SELECT_FOLDER,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OK, Gtk.ResponseType.OK))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.dir_data = dialog.get_filename()
                params.set('paths','dir_data',self.dir_data)
                params.flush()
            else:
                self.dir_data=''
            dialog.destroy()
        if not os.path.exists(self.dir_data):
            dialog = Gtk.MessageDialog(self.win,0, Gtk.MessageType.ERROR,Gtk.ButtonsType.CANCEL,
                     _("La carpeta de datos pywws no existe."))
            dialog.run()
            dialog.destroy()
            return False
        return True

    def update_ui(self):
        self.statusbar.pop(1)
        pywws_data=get_pywws_data(self.dir_data)
        if pywws_data==None:
            self.statusbar.push(1,_('Problema de acceso a datos de pywws.'))
            return True
        idx=pywws_data['a']['idx'].replace(tzinfo=TimeZone.utc).astimezone(TimeZone.Local)
        self.statusbar.push(1,_('Último acceso: ')+idx.strftime('%c').decode('utf-8'))
        for label in labels:
            tipo_k,pywws_k,strfmt=_parse_label(label)
            self.ui_label[label].set_label(strfmt.format(pywws_data[tipo_k][pywws_k]))
        #plotting
        val=[],[],[],[],[],[]
        for d in pywws_data['h']:
            val[0].append(d['idx'])
            val[1].append(d['temp_out'])
            val[2].append(d['temp_in'])
            val[3].append(d['hum_out'])
            val[4].append(d['hum_in'])
            val[5].append(d['rain'])
        self.plot1.clear()
        self.plot2.clear()
        self.plot3.clear()
        self.plot1.plot(val[0],val[1],label=_('T. exterior'))
        self.plot1.plot(val[0],val[2],label=_('T. interior'))
        self.plot2.plot(val[0],val[3],label=_('H. exterior'),color='red')
        self.plot2.plot(val[0],val[4],label=_('H. interior'),color='magenta')
        self.plot3.plot(val[0],val[5],label=_('Lluvia'))
        self.plot1.set_title(_('Últimas 24 horas.'),fontsize=10)
        self.plot1.set_ylabel(_('ᴼC'),fontsize=10)
        self.plot2.set_ylabel(_('%'),fontsize=10)
        self.plot3.set_ylabel(_('mm'),fontsize=10)
        for plot in (self.plot1,self.plot2,self.plot3):
            plot.tick_params(labelsize=9)
            plot.xaxis.set_major_formatter(dates.DateFormatter('%H:%M',TimeZone.Local))
            plot.xaxis.set_major_locator(dates.HourLocator())
            plot.grid(True)
            plot.legend(loc='best',prop={'size':10})
        self.canvas.draw()
        return True

    def on_window_destroy(self,win):
        Gtk.main_quit()

    def run(self):
        Gtk.main()

app_dir=os.path.dirname(os.path.realpath(__file__))
MainWindow().run()
