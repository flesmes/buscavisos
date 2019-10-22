from collections import namedtuple
import re

Aviso = namedtuple('Aviso', ['fenomeno', 'ambitos',
                             'dia_comienzo', 'hora_comienzo',
                             'dia_fin', 'hora_fin'])

def parse_file(filename):
    return AvisosParser(filename).parse()

def removed(l,v):
    return ''.join([e for e in l if e != v])

class AvisosParser:

    pat_fenomeno = re.compile(r'Fenómeno\(\d+\) - (.+)')
    pat_ambitos_nuevo = re.compile(r'Ámbito geográfico: (.+)')
    pat_ambitos_viejo = re.compile(r'(.+)')
    pat_zonas = re.compile(r'(\w+) \((.+)\)')
    pat_hora = r'(..:..) hora oficial del (..\/..\/....)'
    pat_hd2 = r'(..:..) del (..\/..\/....)'
    pat_inicio = re.compile(r'Hora de comienzo: ' + pat_hora)
    pat_fin = re.compile(r'Hora de finalización: ' + pat_hora)
    pat_fecha2 = re.compile(pat_hd2 + ' a ' + pat_hd2 + r' hora oficial')

    def __init__(self, filename):
        
        self.get_lines(filename)
        self.iline = 0
        self.tipo_nuevo = True
        
    def get_lines(self, filename):
        self.lines = []
        file = open(filename, encoding = 'latin1')
        on_header = True
        for content_item in file:
            content_line = content_item[:-1]
            if on_header:
                if len(content_line) == 0 or content_line[-1] != '.':
                    self.lines.append(content_line)
                else:
                    on_header = False
                    line = content_line[:-1]
                    self.lines.append(line)
                    line = ''
            else:
                if len(content_line) != 0 and content_line[-1] != '.':
                    line += content_line + ' '
                else:
                    if len(content_line) != 0:
                        line += content_line[:-1]
                    self.lines.append(line)
                    line = ''
        file.close()

    def end(self):
        return self.iline >= len(self.lines)

    def next(self):
        self.iline += 1

    def get_line(self):
        return self.lines[self.iline]

    def parse(self):
        avisos = []
        while not self.end():
            aviso = self.parse_aviso()
            if aviso:
                avisos.append(aviso)
        return avisos

    def parse_aviso(self):
        fenomeno = self.parse_fenomeno()
        ambitos = self.parse_ambitos()
        tup_fechas = self.parse_fechas()
        if tup_fechas:
            hora_inicio, dia_inicio = tup_fechas[0]
            hora_fin, dia_fin = tup_fechas[1]
            return Aviso(fenomeno, ambitos,
                         dia_inicio, hora_inicio,
                         dia_fin, hora_fin)
        else:
            return None

    def parse_fenomeno(self):
        tup_fenomeno = self.parse_pattern(self.pat_fenomeno)
        self.go_after_fenomeno()
        if tup_fenomeno:
            return tup_fenomeno[0]
        else:
            return None

    def go_after_fenomeno(self):
        while not self.end():
            line = self.get_line()
            if len(line) > 0 and line[0].isspace():
                self.next()
            else:
                break

    def parse_ambitos(self):
        if not self.end():
            self.tipo_nuevo = self.check_tipo_nuevo()
        if self.tipo_nuevo:
            pat_ambitos = self.pat_ambitos_nuevo
        else:
            pat_ambitos = self.pat_ambitos_viejo
        tup_ambitos = self.parse_pattern(pat_ambitos)
        if tup_ambitos:
            return self.separar_ambitos(tup_ambitos[0])
        else:
            return None

    def check_tipo_nuevo(self):
        line = self.get_line()
        return line[:6] == 'Nivel:'

    def parse_fechas(self):
        if self.tipo_nuevo:
            tup_inicio = self.parse_pattern(self.pat_inicio)
            tup_fin = self.parse_pattern(self.pat_fin)
            if tup_fin:
                return tup_inicio, tup_fin
            else:
                return None
        else:
            tup_fecha = self.parse_pattern(self.pat_fecha2)
            if tup_fecha:
                hora_ini, fecha_ini, hora_fin, fecha_fin = tup_fecha
                return (hora_ini, fecha_ini), (hora_fin, fecha_fin)
            else:
                return None

    def parse_pattern(self, pattern):
        while not self.end():
            item = self.get_item(pattern)
            self.next()
            if item:
                return item
        else:
            return None

    def get_item(self, pattern):
        line = self.get_line()
        match = pattern.match(line)
        if match:
            return match.groups()
        else:
            return None

    @staticmethod
    def separar_ambitos(line):
        ambitos = line.split('; ')
        return sum([AvisosParser.separar_zonas(ambito)
                    for ambito in ambitos],
                   [])
    
    @staticmethod
    def separar_zonas(ambito):
        zonas_match = AvisosParser.pat_zonas.match(ambito)
        if zonas_match:
            provincia = zonas_match.group(1)
            zonas = zonas_match.group(2)
            return AvisosParser.listar_zonas(provincia, zonas)
        else:
            return [ambito]

    @staticmethod
    def listar_zonas(provincia, zonas_str):
        
        if zonas_str.find(' y ') >= 0:
            zonas_list = zonas_str.split(' y ')
            zonas_str = zonas_list[0]
            zonas_fin = [zonas_list[1]]
        else:
            zonas_fin = []

        zonas = zonas_str.split(', ') + zonas_fin

        return [provincia + ' - ' + zona for zona in zonas]

        
        
        
            
        
    
