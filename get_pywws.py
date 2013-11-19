
#claves para los datos
key_datos_dia = [
        'idx', 'start',
        'hum_out_ave',
        'hum_out_min', 'hum_out_min_t', 'hum_out_max', 'hum_out_max_t',
        'temp_out_ave',
        'temp_out_min', 'temp_out_min_t', 'temp_out_max', 'temp_out_max_t',
        'hum_in_ave',
        'hum_in_min', 'hum_in_min_t', 'hum_in_max', 'hum_in_max_t',
        'temp_in_ave',
        'temp_in_min', 'temp_in_min_t', 'temp_in_max', 'temp_in_max_t',
        'abs_pressure_ave',
        'abs_pressure_min', 'abs_pressure_min_t',
        'abs_pressure_max', 'abs_pressure_max_t',
        'rel_pressure_ave',
        'rel_pressure_min', 'rel_pressure_min_t',
        'rel_pressure_max', 'rel_pressure_max_t',
        'wind_ave', 'wind_gust', 'wind_gust_t', 'wind_dir',
        'rain',
        'illuminance_ave', 'illuminance_max', 'illuminance_max_t',
        'uv_ave', 'uv_max', 'uv_max_t',
        ]
key_datos_mes = [
        'idx', 'start',
        'hum_out_ave',
        'hum_out_min', 'hum_out_min_t', 'hum_out_max', 'hum_out_max_t',
        'temp_out_ave',
        'temp_out_min_lo', 'temp_out_min_lo_t',
        'temp_out_min_hi', 'temp_out_min_hi_t', 'temp_out_min_ave',
        'temp_out_max_lo', 'temp_out_max_lo_t',
        'temp_out_max_hi', 'temp_out_max_hi_t', 'temp_out_max_ave',
        'hum_in_ave',
        'hum_in_min', 'hum_in_min_t', 'hum_in_max', 'hum_in_max_t',
        'temp_in_ave',
        'temp_in_min_lo', 'temp_in_min_lo_t',
        'temp_in_min_hi', 'temp_in_min_hi_t', 'temp_in_min_ave',
        'temp_in_max_lo', 'temp_in_max_lo_t',
        'temp_in_max_hi', 'temp_in_max_hi_t', 'temp_in_max_ave',
        'abs_pressure_ave',
        'abs_pressure_min', 'abs_pressure_min_t',
        'abs_pressure_max', 'abs_pressure_max_t',
        'rel_pressure_ave',
        'rel_pressure_min', 'rel_pressure_min_t',
        'rel_pressure_max', 'rel_pressure_max_t',
        'wind_ave', 'wind_gust', 'wind_gust_t', 'wind_dir',
        'rain',
        'illuminance_ave',
        'illuminance_max_lo', 'illuminance_max_lo_t',
        'illuminance_max_hi', 'illuminance_max_hi_t', 'illuminance_max_ave',
        'uv_ave',
        'uv_max_lo', 'uv_max_lo_t', 'uv_max_hi', 'uv_max_hi_t', 'uv_max_ave',
        ]
        
#ruta inicial para los ficheros de datos
data_dir='/home/sergio/weather/data'

def get_datos_dias_mes(year,month):
    """Obten datos de los días de un mes.
    
    Params: year  = año del mes
            month = mes del año
    Devuelve una diccionario con claves los dias del mes y con valores
    que son, a su vez, diccionarios con claves'key_datos_dia' y
    valores los datos del día.
    En caso de excepción se devuelve un diccionario vacío.
    """
    data={}
    try:
        fnom=data_dir+'/daily/{0}/{0}-{1:02d}-01.txt'.format(year,month)
        for l in open(fnom):
            v=l.split(',')
            d=dict(zip(key_datos_dia,v))
            for k in d:
                if k=='idx':
                    d[k]=d[k][8:10]     #solo el nº de dia
                elif k=='start':
                    d[k]=d['idx'][:10]  #solo la fecha
                elif k.endswith('_t'):
                    d[k]=d[k][-8:-3]    #solo la hora (hora UTC !)
                else:
                    d[k]=float(d[k])   
            #~ print(d['idx'],d)    
            data[int(d['idx'])]=d
    except Exception as e:
        print('Excepción ocurrida:',e)
        data={}
    return data

key_curr = ['idx', 'delay', 'hum_in', 'temp_in', 'hum_out', 'temp_out',
            'abs_pressure', 'rel_pressure', 'wind_ave', 'wind_gust',
            'wind_dir', 'rain', 'status', 'illuminance', 'uv']
conv = {
        'idx'          : str,
        'delay'        : int,
        'hum_in'       : int,
        'temp_in'      : float,
        'hum_out'      : int,
        'temp_out'     : float,
        'abs_pressure' : float,
        'rel_pressure' : float,
        'wind_ave'     : float,
        'wind_gust'    : float,
        'wind_dir'     : int,
        'rain'         : float,
        'status'       : int,
        'illuminance'  : float,
        'uv'           : int,
        }
import datetime

class Weather(object):

    data={}

    @classmethod
    def now(cls):
        hoy=datetime.date.today()
        fnom=data_dir+'/calib/{0}/{0}-{1:02d}/{0}-{1:02d}-{2:02d}.txt'.format(hoy.year,hoy.month,hoy.day)
        with open(fnom) as f:
            lineas=f.readlines()
        linea=lineas[len(lineas)-1].split(',')
        #print(linea,'\n')
        dic={}
        for k,v in zip(key_curr,linea):
            if v=='':
                dic[k]=v
            else:
                dic[k]=conv[k](v)
        #print(dic)
        if len(cls.data):
            if dic['idx']!=cls.data['idx']:
                dic['rain_interval']=dic['rain'] - cls.data['rain']
                print('rain_interval',dic['rain_interval'])
            else:
                dic['rain_interval']=cls.data['rain_interval']
        else:
            dic['rain_interval']=0.0
        cls.data=dic
        return cls.data

if __name__=='__main__':
    pass
