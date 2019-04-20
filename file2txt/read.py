# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import docx2txt
import subprocess
from io import StringIO
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage


# def doc2docx(docDir):
#     docxDir = './temp/'
#     text = subprocess.check_output(["soffice","--headless","--invisible","--convert-to","docx",\
#                                     docDir,"--outdir",docxDir])

def read_doc(file):
    text = subprocess.check_output(['antiword', file])
    text = text.decode(encoding='utf-8')

    return text

# 读取docx文件
def read_docx(file):
    '''
    :param file: 文件路径
    :return: str
    '''
    text = docx2txt.process(file)

    return text

# 读取doc文件
# def read_doc(docDir):
#     '''
#     :param docDir: doc文件的路径，eg：'../resume/4083.doc'
#     :param docxDir: docx文件的所在文件夹的路径，eg：'../resume/'
#     :return: str
#     '''
#     path = './temp/' + docDir.split('/')[-1].split('.')[0] + '.docx'
#     if not os.path.exists(path):
#         doc2docx(docDir)
#     text = readDocx(path)
#     return text

# 读取txt
def read_txt(file):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return text

# 读取图片cv
# def readImage(file):
#     img=cv2.imread(file)
#     text=pytesseract.image_to_string(img,lang='chi_sim')
#     return text

# 读取图片Pillow
# def readImg(file):
#     text =  subprocess.check_output(['tesseract', file, 'stdout', '-l', 'chi_sim'])
#     return text

# 读取PDF
def read_pdf(file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(file, 'rb') as fp:
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return text


if __name__ == '__main__':
    result = read_doc('../resume/研究生个人简历样本.doc')
    print(result)

