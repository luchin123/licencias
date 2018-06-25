# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import partial
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm, cm
from reportlab.graphics.barcode import code39

from base.models import Licencia

def normal_custom(size, alignment):
    return ParagraphStyle(
        name = 'normal_custom_%s' % str(size),
        fontName = 'Helvetica',
        fontSize = size,
        alignment = alignment
    )

def negrita_custom(size, alignment):
    return ParagraphStyle(
        name = 'negrita_custom_%s' % str(size),
        fontName = 'Helvetica-Bold',
        fontSize = size,
        alignment = alignment
    )

@login_required
def licencia_print(request, id):
    response = HttpResponse(content_type='application/pdf')
    
    buffer = BytesIO()
    try:
        licencia = get_object_or_404(Licencia, pk = id)
    except:
        raise Http404

    report = ImpresionLicencia(buffer)
    pdf = report.print_licencia(licencia)

    response.write(pdf)
    return response


class ImpresionLicencia:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pagesize = (8.4 * cm, 5.3 * cm)
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc, licencia):
        canvas.saveState()

        logo = 'fotos/captura.png'
        canvas.drawImage(logo, 7 * cm, 4 * cm, width = (1 * cm), height = (1 * cm))

        foto = str(licencia.persona.foto)
        canvas.drawImage(foto, 3 * mm, 2 * cm, width = (1 * cm), height = (1 * cm))

        # Cabecera
        header = Paragraph('MUNICIPALIDAD PROVINCIAL DE URUBAMBA', negrita_custom(7, TA_CENTER))
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, 47 * mm)

        header = Paragraph('BLABLA', negrita_custom(7, TA_CENTER))
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, 44 * mm)

        barcode = code39.Extended39(licencia.persona.dni, barWidth = 0.5 * mm, barHeight = 5 * mm)
        w, h = barcode.wrap(doc.width, doc.topMargin)
        barcode.drawOn(canvas, doc.leftMargin, 44 * mm)

        # Footer
        footer = Paragraph(u'VÁLIDO A NIVEL NACIONAL', negrita_custom(10, TA_CENTER))
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, 0)


        canvas.restoreState()

    def print_licencia(self, licencia):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer, pagesize = self.pagesize, topMargin = 7 * mm, leftMargin = 10 * mm, rightMargin = 3 * mm, bottomMargin = 3 * mm, showBoundary = 1)

        elements = []

        p = Paragraph('Nombres', negrita_custom(9, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.nombres, normal_custom(9, TA_LEFT))
        elements.append(p)

        p = Paragraph('Apellidos', negrita_custom(9, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.apellidos, normal_custom(9, TA_LEFT))
        elements.append(p)

        doc.build(elements, onFirstPage = partial(self._header_footer, licencia =licencia),
            onLaterPages = partial(self._header_footer, licencia = licencia))


        pdf = buffer.getvalue()
        buffer.close()
        return pdf        


