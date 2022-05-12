from typing import BinaryIO

import boto3
import variables
import pdf2image
import json


textract = boto3.client('textract', region_name="us-east-1")


class Boleto:
    agencia: str
    codigo: str
    vencimento: str


class Boletocr:
    boleto = Boleto


def readBoleto(file: BinaryIO):
    try:
        # __validateDocument(file)
        # __pdfToImage(file)
        # textractresponse = __callTextract()
        # print(textractresponse)
        __filterResponse()
    except Exception as e:
        print('error - ', e)


def __validateDocument(file: BinaryIO):
    if not file.name.endswith('.pdf'):
        raise Exception('Formato de arquivo precisa ser em PDF.')


def __pdfToImage(file: BinaryIO):
    image = pdf2image.convert_from_bytes(file.read(), poppler_path=variables.poppler)
    image[0].save(variables.imgboleto, 'JPEG')


def __callTextract():
    with open(variables.imgboleto, 'rb') as image:
        response = textract.analyze_expense(
            Document={
                'Bytes': image.read()
            }
        )
        return response


def __filterResponse():
    obj = [[[z for z in y] for y in x['SummaryFields'] if y.get('LabelDetection')] for x in variables.txtctresponse['ExpenseDocuments']]

    for x in obj[0]:
        print(x)
    print(obj)
