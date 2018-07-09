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
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code93, qr

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

        logo = 'fotos/prueba.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        foto = str(licencia.persona.foto)
        canvas.drawImage(foto, 3 * mm, 1.3 * cm, width = (2 * cm), height = (2.5 * cm))

        foto = str(licencia.persona.firma)
        canvas.drawImage(foto, 51 * mm, 2.5 * cm, width = (2.6 * cm), height = (1 * cm))

        categoria = Paragraph('Categoria', negrita_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 50 * mm, 16.9 * mm)

        categoria = Paragraph(licencia.clase, normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 53 * mm, 12.5 * mm)

        categoria = Paragraph(licencia.categoria, normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 50 * mm, 12.5 * mm)

        categoria = Paragraph('Fecha Revalidacion', negrita_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 52 * mm, 8.2 * mm)

        categoria = Paragraph(licencia.fecha_revalidacion.strftime('%d/%b/%Y'), normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 53 * mm, 4 * mm)

        barcode = code93.Standard93(licencia.persona.dni, barWidth = 0.55, barHeight = 7.5 * mm, stop=1)
        w, h = barcode.wrap(doc.width, doc.topMargin)
        barcode.drawOn(canvas, -4 * mm, 6 * mm)

        canvas.restoreState()

    def print_licencia(self, licencia):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer, pagesize = self.pagesize, topMargin = 13* mm, leftMargin = 23 * mm, rightMargin = 3 * mm, bottomMargin = 1 * mm, showBoundary = 0)

        elements = []

        p = Paragraph('Nombres', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.nombres, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Apellidos', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.apellidos, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('N° Licencia', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(str(licencia.numero_licencia), normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Fecha Expedicion', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.fecha_expedicion.strftime('%d/%b/%Y'), normal_custom(8.5, TA_LEFT))
        elements.append(p)
        
        

        doc.build(elements, onFirstPage = partial(self._header_footer, licencia =licencia),
            onLaterPages = partial(self._header_footer, licencia = licencia))


        pdf = buffer.getvalue()
        buffer.close()
        return pdf        

@login_required
def licencia_print2(request, id):
    response = HttpResponse(content_type='application/pdf')
    
    buffer = BytesIO()
    try:
        licencia = get_object_or_404(Licencia, pk = id)
    except:
        raise Http404

    report = ImpresionLicencia2(buffer)
    pdf = report.print_licencia2(licencia)

    response.write(pdf)
    return response


class ImpresionLicencia2:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pagesize = (8.4 * cm, 5.3 * cm)
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc, licencia):
        canvas.saveState()

        logo = 'fotos/prueba2.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        firma = str(licencia.autoridad.firma_autoridad)
        canvas.drawImage(firma, 52 * mm, 0.7 * cm, width = (2.6 * cm), height = (1 * cm))

        size = 65.
        qr_code = qr.QrCodeWidget(licencia.persona.dni)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(size, size, transform=[size/width,0,0,size/height,0,0])
        d.add(qr_code)
        renderPDF.draw(d, canvas, 54 * mm, 22 * mm)
        

        canvas.restoreState()

    def print_licencia2(self, licencia):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer, pagesize = self.pagesize, topMargin = 2* mm, leftMargin = 3 * mm, rightMargin = 3 * mm, bottomMargin = 1 * mm, showBoundary = 0)

        elements = []

        p = Paragraph('Documento de Indentidad', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.dni, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Fecha de Nacimiento', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.fecha_nacimiento.strftime('%d/%b/%Y'), normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Domicilio', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.persona.direccion, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Donacion de Organos', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Si' if licencia.persona.donacion else 'No', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Restricciones', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(licencia.restricciones, normal_custom(8.5, TA_LEFT))
        elements.append(p)
        
        

        doc.build(elements, onFirstPage = partial(self._header_footer, licencia =licencia),
            onLaterPages = partial(self._header_footer, licencia = licencia))


        pdf = buffer.getvalue()
        buffer.close()
        return pdf        


