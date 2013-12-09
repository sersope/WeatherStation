from tkinter import *
from tkinter import ttk,filedialog
from pywws import DataStore
from datetime import datetime,timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def build_frame(parent,text,row,column,double=True):

    #frame
    frm=ttk.Labelframe(parent,text=text,borderwidth=1,relief='solid')
    frm.grid(row=row,column=column,padx=(2,2),pady=(0,5),sticky='WN')
    frm.columnconfigure(0,pad=5)
    frm.columnconfigure(1,pad=5)
    if double:
        frm.columnconfigure(2,pad=5)
    frm.rowconfigure(1,pad=10)
    frm.rowconfigure(3,pad=5)
    frm.rowconfigure(4,pad=5)
    frm.rowconfigure(5,pad=5)

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

def timer(root):

    fecha=datetime.utcnow()
    #Valores actuales
    datos=DataStore.calib_store(dir_data)
    a=datos[datos.nearest(fecha)]
    last_act.set('Ultima actualización:\n'+str(a['idx']))
    te['act'].set('{:.1f} ᴼC'.format(a['temp_out']))
    he['act'].set('{:2d} %'.format(a['hum_out']))
    pr['act'].set('{:.1f} mb'.format(a['rel_pressure']))
    vt['act'].set('{:.1f} km/h'.format(a['wind_gust']))
    ti['act'].set('{:.1f} ᴼC'.format(a['temp_in']))
    hi['act'].set('{:2d} %'.format(a['hum_in']))
    #Valores diarios
    datos=DataStore.daily_store(dir_data)
    d=datos[datos.nearest(fecha)]
    te['maxd'].set('{:.1f} ᴼC'.format(d['temp_out_max']))
    te['mind'].set('{:.1f} ᴼC'.format(d['temp_out_min']))
    he['maxd'].set('{:2d} %'.format(d['hum_out_max']))
    he['mind'].set('{:2d} %'.format(d['hum_out_min']))
    pr['maxd'].set('{:.1f} mb'.format(d['rel_pressure_max']))
    pr['mind'].set('{:.1f} mb'.format(d['rel_pressure_min']))
    vt['maxd'].set('{:.1f} km/h'.format(d['wind_gust']))
    ll['maxd'].set('{:.1f} mm'.format(d['rain']))
    ti['maxd'].set('{:.1f} ᴼC'.format(d['temp_in_max']))
    ti['mind'].set('{:.1f} ᴼC'.format(d['temp_in_min']))
    hi['maxd'].set('{:2d} %'.format(d['hum_in_max']))
    hi['mind'].set('{:2d} %'.format(d['hum_in_min']))
    #Valores mensuales
    datos=DataStore.monthly_store(dir_data)
    m=datos[datos.nearest(fecha)]
    te['maxm'].set('{:.1f} ᴼC'.format(m['temp_out_max_hi']))
    te['minm'].set('{:.1f} ᴼC'.format(m['temp_out_min_lo']))
    he['maxm'].set('{:2d} %'.format(m['hum_out_max']))
    he['minm'].set('{:2d} %'.format(m['hum_out_min']))
    pr['maxm'].set('{:.1f} mb'.format(m['rel_pressure_max']))
    pr['minm'].set('{:.1f} mb'.format(m['rel_pressure_min']))
    vt['maxm'].set('{:.1f} km/h'.format(m['wind_gust']))
    ll['maxm'].set('{:.1f} mm'.format(m['rain']))
    ti['maxm'].set('{:.1f} ᴼC'.format(m['temp_in_max_hi']))
    ti['minm'].set('{:.1f} ᴼC'.format(m['temp_in_min_lo']))
    hi['maxm'].set('{:2d} %'.format(m['hum_in_max']))
    hi['minm'].set('{:2d} %'.format(m['hum_in_min']))
    #Procesar y mostrar valores anuales
    te_max=[]
    te_min=[]
    he_max=[]
    he_min=[]
    pr_max=[]
    pr_min=[]
    vt_max=[]
    ll_tot=[]
    ti_max=[]
    ti_min=[]
    hi_max=[]
    hi_min=[]
    for d in datos[:]:
        te_max.append(d['temp_out_max_hi'])
        te_min.append(d['temp_out_min_lo'])
        he_max.append(d['hum_out_max'])
        he_min.append(d['hum_out_min'])
        pr_max.append(d['rel_pressure_max'])
        pr_min.append(d['rel_pressure_min'])
        vt_max.append(d['wind_gust'])
        ll_tot.append(d['rain'])
        ti_max.append(d['temp_in_max_hi'])
        ti_min.append(d['temp_in_min_lo'])
        hi_max.append(d['hum_in_max'])
        hi_min.append(d['hum_in_min'])
    te['maxy'].set('{:.1f} ᴼC'.format(max(te_max)))
    te['miny'].set('{:.1f} ᴼC'.format(min(te_min)))
    he['maxy'].set('{:2d} %'.format(max(he_max)))
    he['miny'].set('{:2d} %'.format(min(he_min)))
    pr['maxy'].set('{:.1f} mb'.format(max(pr_max)))
    pr['miny'].set('{:.1f} mb'.format(min(pr_min)))
    vt['maxy'].set('{:.1f} km/h'.format(max(vt_max)))
    ll['maxy'].set('{:.1f} mm'.format(sum(ll_tot)))
    ti['maxy'].set('{:.1f} ᴼC'.format(max(ti_max)))
    ti['miny'].set('{:.1f} ᴼC'.format(min(ti_min)))
    hi['maxy'].set('{:2d} %'.format(max(hi_max)))
    hi['miny'].set('{:2d} %'.format(min(hi_min)))
    #Graficos
    datos=DataStore.calib_store(dir_data)
    d_graf=datos[datos.nearest(fecha)-timedelta(hours=24):]
    val=[],[],[]
    for d in d_graf:
        val[0].append(d['idx'])
        val[1].append(d['temp_out'])
        val[2].append(d['temp_in'])
    subp.clear()
    subp.set_title('Últimas 24 horas.')
    subp.set_xlabel('Hora')
    subp.set_ylabel('Temperatura (ᴼC)')
    subp.plot(val[0],val[1],label='T. exterior')
    subp.plot(val[0],val[2],label='T. interior')
    subp.legend(loc=0)
    subp.grid(True)
    # a tk.DrawingArea
    canvas.show()

    root.after(600000,timer,root)

#Ventana y frame ppal
wnd=Tk()
wnd.title('Estación meteorológica')
#~ wnd.rowconfigure(0,weight=1)
#~ wnd.columnconfigure(0,weight=1)
wnd.minsize(935,180)
frm_ppal = ttk.Frame(wnd,padding=5)
frm_ppal.grid(row=0,column=0)   #,sticky='WENS'
#~ frm_ppal.columnconfigure(2,weight=1)
#~ frm_ppal.rowconfigure(2, weight=1)

#Nombre de la estacion
lbl_station=ttk.Label(frm_ppal,text='Benifayó\nFrancisco Climent',font='TkTextFont 12 italic')
lbl_station.grid(row=0,column=0,columnspan=5,sticky='WN')
last_act=StringVar()
lbl_last_act=ttk.Label(frm_ppal,textvariable=last_act)
lbl_last_act.grid(row=0,column=5,columnspan=2,sticky='E',padx=2)
# Frames de variables
te=build_frame(frm_ppal,'Temp.exterior',1,0)
he=build_frame(frm_ppal,'Hum. exterior',1,1)
pr=build_frame(frm_ppal,'Presión',1,2)
vt=build_frame(frm_ppal,'Viento',1,3,False)
ll=build_frame(frm_ppal,'Lluvia',1,4,False)
ti=build_frame(frm_ppal,'Temp. interior',1,5)
hi=build_frame(frm_ppal,'Hum. interior',1,6)

#Frame para graficos
frm_graf=ttk.Frame(frm_ppal,borderwidth=1,relief='flat')
frm_graf.grid(row=2,column=0,columnspan=999,sticky='WENS')
fig = Figure(figsize=(12,3))    #figsize=(12,3),dpi=76
subp = fig.add_subplot(111)
#~ subp2=subp.twinx()
canvas = FigureCanvasTkAgg(fig, master=frm_graf)
canvas._tkcanvas.grid(row=0,column=0,sticky='WENS')
#.ini
params=DataStore.ParamStore('.','wstation.ini')
dir_data=params.get('paths','dir_data')
if dir_data==None:
    dir_data=filedialog.askdirectory(title='Seleccione directorio con datos de pywws')
    params.set('paths','dir_data',dir_data)
    params.flush()


timer(wnd)
wnd.mainloop()
