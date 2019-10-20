import sys
from paths import src_path, avisos_path

sys.path.append(src_path)

from avisos_parser import AvisosParser, parse_file

file1 = avisos_path + '/2018/20180101095147_692501CTL_Z_C_AM_VI.txt'
file2 = avisos_path + '/2007/20070121093701_80ECA.txt'
file3 = avisos_path + '/2018/20180220074237_692501CTL_Z_C_AM_VI.txt'

def test_end():
    parser = AvisosParser(file1)
    assert parser.end() == False
    parser.lines = []
    assert parser.end() == True

def test_next_get_line():
    parser = AvisosParser(file1)
    assert parser.get_line() == 'AGENCIA ESTATAL DE METEOROLOGÍA'
    parser.next()
    assert parser.get_line() == 'INFORMACIÓN SOBRE FENÓMENOS ADVERSOS DE NIVEL AMARILLO'
    
def test_get_fenomeno():
    parser = AvisosParser(file1)
    parser.iline = 10
    (fenomeno,) = parser.get_item(AvisosParser.pat_fenomeno)
    assert fenomeno == 'Vientos'
    
def test_parse_fenomeno1():
    parser = AvisosParser(file1)
    feno = parser.parse_fenomeno()
    assert  feno == 'Vientos'
    line = parser.get_line()
    assert line[:6] == 'Nivel:'

def test_parse_fenomeno2():
    parser = AvisosParser(file2)
    feno = parser.parse_fenomeno()
    assert  feno == 'Costeros'
    line = parser.get_line()
    assert line[:7] == 'Almería'

def test_listar_zonas1():
    provincia = 'Málaga'
    zonas = 'Axarquía'
    assert (AvisosParser.listar_zonas(provincia, zonas) ==
           ['Málaga - Axarquía'])

def test_listar_zonas2():
    provincia = 'Almería'
    zonas = 'Poniente y Almería Capital'
    assert (AvisosParser.listar_zonas(provincia, zonas) ==
           ['Almería - Poniente', 'Almería - Almería Capital'])

def test_listar_zonas3():
    provincia = 'Almería'
    zonas = 'Poniente, Alpujarras y Almería Capital'
    assert (AvisosParser.listar_zonas(provincia, zonas) ==
           ['Almería - Poniente',
            'Almería - Alpujarras',
            'Almería - Almería Capital'])

def test_separar_zonas1():
    assert AvisosParser.separar_zonas('Almería') == ['Almería']

def test_separar_zonas2():
    provincia = 'Almería (Poniente y Almería Capital)'
    esperado = ['Almería - Poniente', 'Almería - Almería Capital']
    assert AvisosParser.separar_zonas(provincia) == esperado

def test_separar_ambitos():
    #parser = AvisosParser(file2)
    line = 'Almería (Poniente, Alpujarras y Almería Capital); Granada; Málaga (Axarquía); Lleida (Valle de Arán y Depresión Central)'
    print(AvisosParser.separar_ambitos(line))
    assert (AvisosParser.separar_ambitos(line) ==
           ['Almería - Poniente',
            'Almería - Alpujarras',
            'Almería - Almería Capital',
            'Granada',
            'Málaga - Axarquía',
            'Lleida - Valle de Arán',
            'Lleida - Depresión Central'])
    
def test_parse_file_1():
    avisos = parse_file(file1)
    assert len(avisos) == 1
    aviso = avisos[0]
    assert aviso.fenomeno == 'Vientos'
    assert aviso.ambitos == ['Lleida - Valle de Arán']
    assert aviso.dia_comienzo == '01/01/2018'
    assert aviso.hora_comienzo == '12:00'
    assert aviso.dia_fin == '02/01/2018'
    assert aviso.hora_fin == '12:00'

def test_parse_file_2():
    avisos = parse_file(file2)
    assert len(avisos) == 27
    
    aviso = avisos[0]
    assert aviso.fenomeno == 'Costeros'
    assert aviso.ambitos == ['Almería - Poniente',
                             'Almería - Almería Capital',
                             'Granada',
                             'Málaga - Axarquía']
    assert aviso.dia_comienzo == '22/01/2007'
    assert aviso.hora_comienzo == '00:00'
    assert aviso.dia_fin == '23/01/2007'
    assert aviso.hora_fin == '00:00'
    
    aviso = avisos[26]
    assert aviso.fenomeno == 'Costeros'
    assert aviso.ambitos == ['Melilla']
    assert aviso.dia_comienzo == '22/01/2007'
    assert aviso.hora_comienzo == '00:00'
    assert aviso.dia_fin == '23/01/2007'
    assert aviso.hora_fin == '00:00'

def test_parse_file_3():
    avisos = parse_file(file3)
    assert len(avisos) == 0



#test_parse_fenomeno1()
