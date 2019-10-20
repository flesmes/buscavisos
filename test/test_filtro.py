import sys
from paths import src_path

sys.path.append(src_path)

from avisos_parser import Aviso
from buscavisos import get_fechas

def test_get_fecha1():
    aviso = Aviso(None, None, '01/01/2019', '00:00', '01/01/2019', '12:00') 
    assert get_fechas(aviso) == ['2019-01-01']

def test_get_fecha2():
    aviso = Aviso(None, None, '01/01/2019', '00:00', '02/01/2019', '00:00') 
    assert get_fechas(aviso) == ['2019-01-01']

def test_get_fecha3():
    aviso = Aviso(None, None, '01/01/2019', '00:00', '02/01/2019', '12:00') 
    assert get_fechas(aviso) == ['2019-01-01','2019-01-02']

def test_get_fecha4():
    aviso = Aviso(None, None, '01/01/2019', '00:00', '03/01/2019', '00:00') 
    assert get_fechas(aviso) == ['2019-01-01','2019-01-02']

def test_get_fecha5():
    aviso = Aviso(None, None, '01/01/2019', '00:00', '03/01/2019', '12:00') 
    assert get_fechas(aviso) == ['2019-01-01','2019-01-02','2019-01-03']

