import sys
from tkinter import *
from tkinter import ttk,filedialog
from pywws import DataStore
from datetime import datetime
#~ from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#~ from matplotlib.figure import Figure

def build_frame(parent,text,row,column,double=True):

    #frame
    frm=ttk.Labelframe(parent,text=text,borderwidth=1,relief='solid')
    frm.grid(row=row,column=column,padx=(0,5),pady=(0,5),sticky='WN')
    frm.columnconfigure(0,pad=5)
    frm.columnconfigure(1,pad=5)
    if double:
        frm.columnconfigure(2,pad=5)
    frm.rowconfigure(1,pad=5)
    frm.rowconfigure(3,pad=3)
    frm.rowconfigure(4,pad=3)
    frm.rowconfigure(5,pad=3)

    #fixed labels
    #~ ttk.Label(frm,text=text).grid(column=0,row=0,columnspan=3)
    ttk.Label(frm,text='Máx.',foreground='red').grid(row=2,column=1)
    if double:
        ttk.Label(frm,text='Mín.',foreground='blue').grid(row=2,column=2)
    ttk.Label(frm,text='Hoy:').grid(row=3,column=0)
    ttk.Label(frm,text='Mes:').grid(row=4,column=0)
    ttk.Label(frm,text='Año:').grid(row=5,column=0)

    #var labels
    keys=['act','maxd','maxm','maxy','mind','minm','miny']
    lbl=[None]*7
    var=[None]*7

    var[0]=StringVar()
    lbl[0]=ttk.Label(frm,textvariable=var[0],font='TkTextFont 12',padding=(5,0))
    lbl[0].grid(row=1,column=0,columnspan=3)
    for r in range(3):
        var[r+1]=StringVar()
        lbl[r+1]=ttk.Label(frm,textvariable=var[r+1],foreground='red')
        lbl[r+1].grid(row=r+3,column=1)
        if double:
            var[r+4]=StringVar()
            lbl[r+4]=ttk.Label(frm,textvariable=var[r+4],foreground='blue')
            lbl[r+4].grid(row=r+3,column=2)
    return dict(zip(keys,var))

#TEST
i=0
def timer(root,lbl):
    global i
    i=i+1
    lbl.set(str(i))
    root.after(100,timer,root,lbl)

#Ventana y frame ppal
wnd=Tk()
wnd.title('Estación meteorológica')
wnd.rowconfigure(0,weight=1)
wnd.columnconfigure(0,weight=1)
wnd.minsize(710,170)
frm_ppal = ttk.Frame(wnd,padding=5)
frm_ppal.grid(row=0,column=0,sticky='WENS')
frm_ppal.columnconfigure(99,weight=1)
frm_ppal.rowconfigure(99, weight=1)

#Nombre de la estacion
lbl_station=ttk.Label(frm_ppal,text='Benifayó\nFrancisco Climent',font='TkTextFont 12 italic')
lbl_station.grid(row=0,column=0,columnspan=999,sticky='WN')

# Frames de variables
te=build_frame(frm_ppal,'Temp.exterior',1,0)
he=build_frame(frm_ppal,'Hum. exterior',1,1)
pr=build_frame(frm_ppal,'Presión',1,2)
vt=build_frame(frm_ppal,'Viento',1,3,False)
ll=build_frame(frm_ppal,'Lluvia',1,4,False)
ti=build_frame(frm_ppal,'Temp. interior',1,5)
hi=build_frame(frm_ppal,'Hum. interior',1,6)

#Frame para graficos
frm_graf=ttk.Frame(frm_ppal,borderwidth=1,relief='solid')
frm_graf.grid(row=99,column=0,columnspan=999,sticky='WENS')
#TEST
#~ f = Figure(figsize=(5,4), dpi=150)
#~ a = f.add_subplot(111)
#~ t = range(10)
#~ s = range(10)
#~ a.plot(t,s)
#~ a.set_title('Tk embedding')
#~ a.set_xlabel('X axis label')
#~ a.set_ylabel('Y label')
#~ # a tk.DrawingArea
#~ canvas = FigureCanvasTkAgg(f, master=frm_graf)
#~ canvas.show()
#~ canvas._tkcanvas.grid(row=0,column=0,sticky='WENS')

#.ini
params=DataStore.ParamStore('.','WeatherStation.ini')
dir_data=params.get('paths','dir_data')
if dir_data==None:
    dir_data=filedialog.askdirectory(title='Seleccione directorio con datos de pywws')
    params.set('paths','dir_data',dir_data)
    params.flush()

#Valores actuales
datos=DataStore.calib_store(dir_data)
d=datos[datos.nearest(datetime.utcnow())]
te['act'].set('{:.1f} ᴼC'.format(d['temp_out']))
he['act'].set('{:2d} %'.format(d['hum_out']))
pr['act'].set('{:.1f} mb'.format(d['rel_pressure']))
vt['act'].set('{:.1f} km/h'.format(d['wind_gust']))
ti['act'].set('{:.1f} ᴼC'.format(d['temp_in']))
hi['act'].set('{:2d} %'.format(d['hum_in']))

timer(wnd,ll['act'])
wnd.mainloop()
