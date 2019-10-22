from datetime import date, timedelta
import glob
import re

from avisos_parser import parse_file

def filtrado():
    path_avisos = '../avisos/*/*'
    for file in glob.glob(path_avisos):
        for aviso in parse_file(file):
            if (aviso.fenomeno == 'Vientos' and
                ('Lleida' in aviso.ambitos or
                 'Lleida - Valle de Arán' in aviso.ambitos)):
                yield aviso

def get_fechas(aviso):
    fecha1 = dia_to_fecha(aviso.dia_comienzo)
    fecha2 = dia_to_fecha(aviso.dia_fin)
    if aviso.hora_fin == '00:00':
        fecha2 -= timedelta(1)
    intervalo = (fecha2 - fecha1)
    rango = [fecha1 + timedelta(i) for i in range(intervalo.days+1)]
    return [fecha.strftime('%Y-%m-%d') for fecha in rango]

def dia_to_fecha(dia):
    dia,mes,year = dia.split(r'/')
    return date(int(year),int(mes),int(dia))
    
def main():
    fechas = set([])
    for aviso in filtrado():
        fechas.update(set(get_fechas(aviso)))
    resultado = sorted(list(fechas))
    print(len(resultado))
    file = open('dias_aviso_aran.txt','w')
    file.write('\n'.join(resultado))
    file.write('\n')
    print('\n'.join(resultado))

if __name__ == '__main__':    
    main()

