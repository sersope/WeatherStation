from tkinter import *
from tkinter import ttk

root=Tk()
root.title('Estación meteorológica')
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
#ttk.Sizegrip(root).grid(column=1, row=1, sticky=(S,E))

frm_ppal = ttk.Frame(root,borderwidth=2,relief='flat')
frm_ppal.grid(row=0,column=0,sticky='WENS')
frm_ppal.columnconfigure(1,weight=1)
frm_ppal.rowconfigure(1, weight=1)

# Marco temperatura
frm_temp=ttk.Frame(frm_ppal,borderwidth=1,relief='solid')
frm_temp.grid(row=0,column=0,padx=(0,5),pady=(0,5))
frm_temp.columnconfigure(0,pad=3)
frm_temp.columnconfigure(1,pad=3)
frm_temp.columnconfigure(2,pad=3)
frm_temp.rowconfigure(1,pad=5)
frm_temp.rowconfigure(3,pad=3)
frm_temp.rowconfigure(4,pad=3)
frm_temp.rowconfigure(5,pad=3)
ttk.Label(frm_temp,text='Temperatura').grid(column=0,row=0,columnspan=3)
lbl_temp=ttk.Label(frm_temp,text='20.9 ᴼC',font='TkTextFont 12 bold')#TEST
lbl_temp.grid(row=1,column=0,columnspan=3)
ttk.Label(frm_temp,text='Máx.',foreground='red').grid(row=2,column=1)
ttk.Label(frm_temp,text='Mín.',foreground='blue').grid(row=2,column=2)
ttk.Label(frm_temp,text='Hoy:').grid(row=3,column=0)
ttk.Label(frm_temp,text='Mes:').grid(row=4,column=0)
ttk.Label(frm_temp,text='Año:').grid(row=5,column=0)

ttk.Label(frm_temp,text='32.3ᴼC',foreground='red').grid(row=3,column=1)#TEST
ttk.Label(frm_temp,text='11.3ᴼC',foreground='blue').grid(row=3,column=2)#TEST
ttk.Label(frm_temp,text='42.3ᴼC',foreground='red').grid(row=4,column=1)#TEST
ttk.Label(frm_temp,text='8.3ᴼC',foreground='blue').grid(row=4,column=2)#TEST
ttk.Label(frm_temp,text='44.3ᴼC',foreground='red').grid(row=5,column=1)#TEST
ttk.Label(frm_temp,text='1.3ᴼC',foreground='blue').grid(row=5,column=2)#TEST
# Marco humedad
frm_hum=ttk.Frame(frm_ppal,borderwidth=1,relief='solid')
frm_hum.grid(row=0,column=1,pady=(0,5),sticky='w')
frm_hum.columnconfigure(0,pad=3)
frm_hum.columnconfigure(1,pad=3)
frm_hum.columnconfigure(2,pad=3)
frm_hum.rowconfigure(1,pad=5)
frm_hum.rowconfigure(3,pad=3)
frm_hum.rowconfigure(4,pad=3)
frm_hum.rowconfigure(5,pad=3)
ttk.Label(frm_hum,text='Humedad').grid(column=0,row=0,columnspan=3)
lbl_temp=ttk.Label(frm_hum,text='38 %',font='TkTextFont 12 bold')#TEST
lbl_temp.grid(row=1,column=0,columnspan=3)
ttk.Label(frm_hum,text='Máx.',foreground='red').grid(row=2,column=1)
ttk.Label(frm_hum,text='Mín.',foreground='blue').grid(row=2,column=2)
ttk.Label(frm_hum,text='Hoy:').grid(row=3,column=0)
ttk.Label(frm_hum,text='Mes:').grid(row=4,column=0)
ttk.Label(frm_hum,text='Año:').grid(row=5,column=0)

ttk.Label(frm_hum,text='68%',foreground='red').grid(row=3,column=1)#TEST
ttk.Label(frm_hum,text='25%',foreground='blue').grid(row=3,column=2)#TEST
ttk.Label(frm_hum,text='72%',foreground='red').grid(row=4,column=1)#TEST
ttk.Label(frm_hum,text='18%',foreground='blue').grid(row=4,column=2)#TEST
ttk.Label(frm_hum,text='96%',foreground='red').grid(row=5,column=1)#TEST
ttk.Label(frm_hum,text='5%',foreground='blue').grid(row=5,column=2)#TEST

#Marco graficos
frm_graf=ttk.Frame(frm_ppal,borderwidth=1,relief='solid')
frm_graf.grid(row=1,column=0,columnspan=2,sticky='WENS')

lbl100=ttk.Label(frm_graf,text='Gráficos')
lbl100.grid(row=0,column=0)




root.mainloop()
