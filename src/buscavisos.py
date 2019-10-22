from datetime import date, timedelta
import glob
import re

from avisos_parser import parse_file

pat_dia = re.compile(r'(..)/(..)/(....)')

def filtrado():
    path_avisos = '../avisos/*/*'
    for file in glob.glob(path_avisos):
        avisos = parse_file(file)
        for aviso in avisos:
            if (aviso.fenomeno == 'Vientos' and
                ('Lleida' in aviso.ambitos or
                 'Lleida - Valle de Arán' in aviso.ambitos)):
                yield aviso

def get_fechas(aviso):
    d1,m1,a1 = pat_dia.match(aviso.dia_comienzo).groups()
    fecha1 = date(int(a1),int(m1),int(d1))
    d2,m2,a2 = pat_dia.match(aviso.dia_fin).groups()
    fecha2 = date(int(a2),int(m2),int(d2))
    if aviso.hora_fin == '00:00':
        fecha2 -= timedelta(1)
    delta = (fecha2 - fecha1)
    days = delta.days + 1
    rango = [fecha1 + timedelta(i) for i in range(days)]
    return [fecha.strftime('%Y-%m-%d') for fecha in rango]

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

