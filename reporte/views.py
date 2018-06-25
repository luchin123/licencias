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
    def _header_footer(canvas, doc):
        canvas.saveState()

        # Cabecera
        header = Paragraph('MUNICIPALIDAD PROVINCIAL DE URUBAMBA', negrita_custom(10, TA_CENTER))
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin)

        # Footer
        footer = Paragraph(u'VÁLIDO A NIVEL NACIONAL', negrita_custom(10, TA_CENTER))
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, doc.topMargin)

        canvas.restoreState()

    def print_licencia(self, licencia):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer, pagesize = self.pagesize, topMargin = 3 * mm, leftMargin = 3 * mm, rightMargin = 3 * mm, bottomMargin = 3 * mm, showBoundary = 1)

        elements = []

        p = Paragraph('Nombres', negrita_custom(9, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.nombres, normal_custom(9, TA_LEFT))
        elements.append(p)

        doc.build(elements, onFirstPage = partial(self._header_footer),
            onLaterPages = partial(self._header_footer))


        pdf = buffer.getvalue()
        buffer.close()
        return pdf        


