import os
import io
import logging
import json
from datetime import datetime

from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import utils
import parameters

MIN_X = 0
MIN_Y = 0

NUMBER_MONTH_TO_NAME_MONTH = {
    '01':'Janeiro',
    '02':'Fevereiro',
    '03':'Março',
    '04':'Abril',
    '05':'Maio',
    '06':'Junho',
    '07':'Julho',
    '08':'Agosto',
    '09':'Setembro',
    '10':'Outubro',
    '11':'Novembro',
    '12':'Dezembro',
}

def process_dict_template(dict_json_input, dict_template = parameters.DICT_TEMPLATE_MAIL):
    dict_template['NAME']['VALUE'] = dict_json_input['NAME']
    dict_template['TITLE']['VALUE'] = dict_json_input['TITLE']
    dict_template['CODE']['VALUE'] = dict_json_input['CODE']
    dict_template['DATE']['VALUE'] = dict_json_input['DATE']
    return dict_template


def process_name_city_actual_date(name_city : str):
    from datetime import datetime
    today = datetime.today()
    value = f'{str(name_city).strip().title()}, {str(today.day).zfill(2)} De {NUMBER_MONTH_TO_NAME_MONTH[str(today.month).zfill(2)]} De {str(today.year).zfill(4)}'
    return value


def read_input_json(path : str, filename : str):
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    with open(full_path + '.json', 'r', encoding='utf-8') as file:
        try:
            dict_infos = json.load(file)
        except:
            dict_infos = None
            logging.warning('Json Invalido')
    return dict_infos


def register_font(font_name : str):
    actual_path = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(actual_path, 'fonts', font_name + '.ttf')
    
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    return True


def save_input_in_ram(dict_values : dict, height : int, weight : int):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(weight, height))

    register_font('Poppins-Bold')

    for item in dict_values.values():
        if item['STYLE'] == '1':
            can.setFillColorRGB(r=255, g=255, b=255)
            can.setFont(psfontname='Poppins-Bold', size=60) 
        elif item['STYLE'] == '2':
            can.setFillColorRGB(r=255, g=255, b=255)
            can.setFont(psfontname='Poppins-Bold', size=40) 
        
        
        if 'SPECIAL' in item:
            if item['SPECIAL'] == 'DATE_TODAY':
                item['VALUE'] = str(datetime.today().strftime('%d/%m/%Y'))
                text_width = stringWidth(item['VALUE'], 'Poppins-Bold', 60)
                item['CORD_X'] = (weight - text_width) / 2.0
            elif item['SPECIAL'] == 'HUMAN_READABLE':
                text_width = stringWidth(item['VALUE'], 'Poppins-Bold', 60)
                item['CORD_X'] = (weight - text_width) / 2.0
        can.drawString(float(item['CORD_X']), float(item['CORD_Y']), item['VALUE'])

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    return new_pdf


def read_template(full_path : str):
    existing_pdf = PdfFileReader(open(full_path, "rb"))
    page = existing_pdf.getPage(0)
    height = int(page.mediaBox.getHeight())
    weight = int(page.mediaBox.getWidth())
    
    return page, height, weight


def merge_pdfs(page, new_pdf, output):
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return output


def save_fill_template(full_path : str, output):
    outputStream = open(full_path, "wb")
    output.write(outputStream)
    outputStream.close()


def generate_direct_mail(path_template, dict_values):
    output = PdfFileWriter()
    page, height, weight = read_template(full_path=path_template)
    new_pdf = save_input_in_ram(dict_values=dict_values, height=height, weight=weight)
    output = merge_pdfs(page=page, new_pdf=new_pdf, output=output)
    return output


def generate_certificate(dict_input, path_template, path_output):

    dict_template_mail = process_dict_template(dict_json_input=dict_input)
    output = generate_direct_mail(path_template=path_template, dict_values=dict_template_mail)
    save_fill_template(full_path=path_output, output=output)