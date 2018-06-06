from datetime import datetime

def crear_enlace(href, clase, titulo, icono):
    return '<a href="%s" class="btn btn-%s btn-xs" title="%s"><i class="fa fa-%s"></i></a> ' % (href, clase, titulo, icono)

def timestamp_a_fecha(timestamp, formato):
    timestamp = int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime(formato)
